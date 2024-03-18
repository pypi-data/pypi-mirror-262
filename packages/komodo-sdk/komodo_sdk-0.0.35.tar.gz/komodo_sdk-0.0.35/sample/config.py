from komodo.framework.komodo_config import KomodoConfig


class ApplianceConfig(KomodoConfig):
    def get_serpapi_key(self):
        return self.get_secret("SERPAPI_KEY")
