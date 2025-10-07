import logging
import pprint
import pandas as pd

from dotenv import load_dotenv
from pipeline.database import User, get_session
from pipeline.world import generate_random_world
from pipeline.drawer import draw
from pipeline.storage import HttpStorage, JsonStorage
from pipeline.logger import get_json_logger, get_plain_text_logger
from scripts.learn_sqlalchemy import insert_sample_data
from scripts.setup_db import init_db


def process()->None:
    df = pd.read_csv('data/raw_plays.csv', parse_dates=['timestamp'])
    pprint.pprint(df)    

    # Combine genre and date filters
    genre_filter = df['genre'].isin(['edm', 'rap', 'hip_hop'])
    date_filter = df['timestamp'] < '2025-09-29'
    modern_music_mask = date_filter & genre_filter
    
    modern_music = df[modern_music_mask]
    print('modern_music')
    filtered_columns = ['timestamp', 'genre', 'track_name']
    modern_music = modern_music[filtered_columns]
    pprint.pprint(modern_music)
    modern_music.to_csv('data/modern_music.csv', index=False)



def dungeon() -> None:

    storage = JsonStorage()

    logger.info("Pipeline starting")

    try:
        stage = storage.load()
        logger.info("Stage loaded from storage")
        stage = generate_random_world()
        logger.info("Random world generated")
    except ValueError as e:
        logger.exception(
            "Error during running stage", extra={"error_type": "ValueError"}
        )

        exit(1)

    draw(stage)
    logger.info("Stage drawn successfully")

    storage.save(stage)


logger = get_json_logger(__name__)
load_dotenv()

session = get_session()
data = session.query(User).all()
pprint.pprint(data)

# process()