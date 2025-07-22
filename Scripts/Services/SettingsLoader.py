import json
import os

class SettingsLoader:
    _data = {}

    @classmethod
    def load(self, file_path="settings.json"):
        full_path = os.path.join(os.getcwd(), file_path)

        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"Settings file not found: {full_path}")

        with open(full_path, 'r', encoding='utf-8') as f:
            self._data = json.load(f)

    @classmethod
    def get(self, key_path, default=None):
        keys = key_path.split(".")
        val = self._data

        for key in keys:
            if isinstance(val, dict) and key in val:
                val = val[key]
            else:
                return default
        return val
