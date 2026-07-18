"""Small helpers for reading service configuration from a file + environment.

Values are looked up in the config file first, then the process environment.
"""
import os


def _load_file(path):
    settings = {}
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, value = line.partition("=")
            settings[key.strip()] = value
    return settings


class Config:
    def __init__(self, path="config.env"):
        self._file = _load_file(path) if os.path.exists(path) else {}

    def _raw(self, key):
        # File wins, then fall back to the environment.
        if key in self._file:
            return self._file[key]
        return os.environ.get(key)

    def get(self, key, default=None):
        value = self._raw(key)
        return value if value is not None else default

    def get_bool(self, key, default=False):
        value = self._raw(key)
        if value is None:
            return default
        return bool(value)

    def get_int(self, key, default=0):
        value = self._raw(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default

    def get_list(self, key, default=None):
        value = self._raw(key)
        if not value:
            return default or []
        return value.split(",")
