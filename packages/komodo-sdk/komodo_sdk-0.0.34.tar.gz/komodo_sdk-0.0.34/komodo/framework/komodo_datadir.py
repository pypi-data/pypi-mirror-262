import os
from pathlib import Path

from komodo.shared.utils.pathutils import find_nearest_parent_containing


def default_data_directory(normalize=False):
    # in docker containers this directory will be mounted and serve as the data directory
    data_directory = os.getenv("KOMODO_DATA_DIRECTORY", "/data/komodo")
    if not os.path.exists(data_directory):
        if os.path.exists("./data/komodo"):
            data_directory = "./data/komodo"
        else:
            path = find_nearest_parent_containing("data")
            if path:
                data_directory = path / "data"
            else:
                data_directory = Path(os.getcwd()) / "data"

    return os.path.normpath(data_directory) if normalize else data_directory


if __name__ == "__main__":
    print(default_data_directory())
