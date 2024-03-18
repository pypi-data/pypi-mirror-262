import os
from pathlib import Path


class KomodoConfig:

    def data_dir(self) -> Path:
        path = os.getenv("KOMODO_DATA_DIR", "/data/komodo")
        if not os.path.exists(path):
            if os.path.exists("./data/komodo"):
                path = "./data/komodo"

        if not os.path.exists(path):
            raise Exception("Default data directory not found. Please set KOMODO_DATA_DIR environment variable.")

        return Path(path)

    def get_secret(self, name) -> str:
        if name not in os.environ:
            raise Exception(f"Environment variable {name} not found.")
        return os.getenv(name)
