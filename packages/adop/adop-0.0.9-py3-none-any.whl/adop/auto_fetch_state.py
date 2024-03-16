import configparser
import pathlib
from hashlib import sha256


class State:
    """
    Caches the auto fetch state to disk.
    """

    def __init__(self, cache_root_name: str):
        cache_root = pathlib.Path.cwd().joinpath(cache_root_name)
        cache_root.mkdir(parents=True, exist_ok=True)
        config = configparser.ConfigParser()
        config_file_path = cache_root.joinpath("autofetchstate.ini")
        if config_file_path.exists():
            config.read_string(config_file_path.read_text())
        self.config = config
        self.config_file_path = config_file_path

    def get(self, source: str) -> str:
        "Returns the shasum of the latest update"
        if self.config.has_section(source):
            return self.config.get(source, "last_update")

    def update(self, source: str, updated: str):
        "Set the given shasum as the latest update"
        if not self.config.has_section(source):
            self.config.add_section(source)
        self.config.set(source, "last_update", updated)

    def store(self):
        "Write the changes to disk."
        with self.config_file_path.open(mode="w") as f:
            self.config.write(f)

    @staticmethod
    def make(bin_data: bytes) -> str:
        """
        Returns a hash value for the binary data
        """
        return sha256(bin_data).hexdigest()
