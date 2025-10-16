import argparse
import logging
import pprint
from typing import Dict, Optional

from dotenv import load_dotenv
from pipeline.clients import ListenBrainzClient, MusicBrainzClient
from pipeline.config import load_config
from pipeline.enrichment import ListenEnricher
from pipeline.logger import get_json_logger, get_plain_text_logger
from pipeline.persistence import DataWarehouseWriter
from pipeline.services import IngestionService, PlaybackCursorProvider


def process(full_resync: bool = False) -> None:
    print("processing...")
    config = load_config()
    listen_client = ListenBrainzClient(
        user=config.listenbrainz.user,
        count=config.listenbrainz.fetch_count,
        logger=logger,
    )
    music_client = MusicBrainzClient(logger=logger)
    enricher = ListenEnricher(music_client=music_client, logger=logger)
    warehouse_writer = DataWarehouseWriter(logger=logger)
    cursor_provider = PlaybackCursorProvider(logger=logger)
    ingestion_service = IngestionService(
        listen_client=listen_client,
        cursor_provider=cursor_provider,
        logger=logger,
    )

    if full_resync:
        logger.info("Full resync requested", extra={"event": "ingest.full_resync"})

    result = ingestion_service.fetch(full_resync=full_resync)
    listens_df = result.listens
    if listens_df.empty:
        print("no listens found")
        logger.info(
            "No new listens ingested",
            extra={
                "event": "ingest.no_new_listens",
                "new_listens": 0,
                "last_ts": result.cursor_used,
            },
        )
        return

    enriched = enricher.enrich(listens_df)
    warehouse_writer.persist(enriched)
    counts = {key: int(len(value)) for key, value in enriched.items()}
    logger.info(
        "Ingested listens persisted",
        extra={
            "event": "ingest.persisted",
            **{f"{key}_count": count for key, count in counts.items()},
        },
    )
    _emit_ingestion_metrics(
        fetched=int(len(listens_df)),
        cursor_used=result.cursor_used,
        full_resync=full_resync,
        counts=counts,
    )


def _emit_ingestion_metrics(
    *,
    fetched: int,
    cursor_used: Optional[int],
    full_resync: bool,
    counts: Dict[str, int],
) -> None:
    logger.info(
        "Ingestion metrics",
        extra={
            "event": "metrics.ingestion",
            "fetched": fetched,
            "cursor_used": cursor_used,
            "full_resync": full_resync,
            **{f"persisted_{key}": value for key, value in counts.items()},
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline main entrypoint")
    parser.add_argument(
        "--full-resync",
        action="store_true",
        help="Ignore existing plays and fetch all listens from ListenBrainz",
    )
    args = parser.parse_args()

    load_dotenv()
    process(full_resync=args.full_resync)


logger = get_json_logger(__name__)

# session = get_session()
# data = session.query(User).all()
# pprint.pprint(data)

if __name__ == "__main__":
    main()
