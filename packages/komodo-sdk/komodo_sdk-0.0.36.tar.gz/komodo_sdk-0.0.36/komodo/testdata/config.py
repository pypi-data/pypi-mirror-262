import os
from pathlib import Path

from komodo.framework.komodo_config import KomodoConfig


class TestConfig(KomodoConfig):
    PATH = os.path.dirname(__file__)
    TEST_MONGO_URL = "mongodb://root:example@localhost:27017/"

    def data_dir(self) -> Path:
        return Path(self.PATH)

    def get_secret(self, name) -> str:
        if name == 'SERP_API_KEY':
            return os.getenv('SERP_API_KEY', '')

        if name == 'TAVILY_API_KEY':
            return os.getenv('TAVILY_API_KEY', '')

        if name == 'MONGO_URL':
            return os.getenv('MONGO_URL', self.TEST_MONGO_URL)

    @classmethod
    def path(cls, relative_path=""):
        return TestConfig().data_dir() / relative_path

    @classmethod
    def get_mongo_connection_string(cls):
        return TestConfig().get_secret('MONGO_URL')

    @classmethod
    def get_serp_api_key(cls):
        return TestConfig().get_secret('SERP_API_KEY')


if __name__ == "__main__":
    print(TestConfig.PATH)
    print(TestConfig.path())
