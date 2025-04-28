from pathlib import Path
import sys
import os
import json

class ConfigLoader:
    @staticmethod
    def get_root_path(marker_file="launcher_config.json") -> str:
        current = Path(__file__).resolve()
        for parent in current.parents:
            if (parent / marker_file).exists():
                if str(parent) not in sys.path:
                    sys.path.append(str(parent))
                return str(parent).replace("\\", "/")
        raise FileNotFoundError(f"Could not find {marker_file} in any parent of {__file__}")

    @staticmethod
    def load_config(filename="launcher_config.json") -> dict:
        root_path = ConfigLoader.get_root_path()
        config_path = os.path.join(root_path, filename)
        with open(config_path, "r") as f:
            return json.load(f)