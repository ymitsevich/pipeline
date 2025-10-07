import pprint
from pipeline.world import Stage
import requests
from pathlib import Path
import os


class Storage:
    def save(self, stage: Stage) -> None:
        pass


class JsonStorage(Storage):
    def save(self, stage: Stage) -> None:
        with open("stage.json", "w") as f:
            f.write(stage.model_dump_json(indent=2))

    def load(self) -> Stage:
        DATA_DIR = Path(os.getenv("DATA_DIR", "./mock"))
        pprint.pprint(DATA_DIR)

        project_root = Path(__file__).parent.parent.parent
        data_dir = project_root / Path("data")
        output_file = data_dir / "stage.json"

        if not data_dir.exists():
            raise ValueError("Data directory not found")

        with open(output_file, "r") as f:
            return Stage.model_validate_json(f.read())


class HttpStorage(Storage):
    def save(self, stage: Stage) -> None:
        try:
            response = requests.post(
                "https://pipeline.free.beeceptor.com/pipeline", timeout=5
            )
            response.raise_for_status()
            data = response.json()
            if data.get("body") is None or data.get("body") != "success":
                raise ValueError("Failed to save stage")

        except requests.Timeout:
            raise ValueError("Request timed out")
        except requests.ConnectionError:
            raise ValueError("Network problem occurred")
        except requests.HTTPError as e:
            raise ValueError(f"HTTP error: {e.response.status_code}")
        except requests.RequestException as e:
            raise ValueError(f"Something went wrong: {e}")

    def load(self) -> Stage:
        try:
            response = requests.get(
                "https://pipeline.free.beeceptor.com/pipeline", timeout=5
            )
            response.raise_for_status()
            data = response.json()

            return Stage.model_validate(data)
        except requests.Timeout:
            raise ValueError("Request timed out")
        except requests.ConnectionError:
            raise ValueError("Network problem occurred")
        except requests.HTTPError as e:
            raise ValueError(f"HTTP error: {e.response.status_code}")
        except requests.RequestException as e:
            raise ValueError(f"Something went wrong: {e}")
