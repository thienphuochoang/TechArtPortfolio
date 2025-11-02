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
        print("[ConfigLoader] looking for config at:", config_path)

        try:
            with open(config_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("[ConfigLoader] file not found:", config_path)
            return {}
        except json.JSONDecodeError as e:
            print("[ConfigLoader] JSON error:", e)
            return {}

        # if we get here, we loaded something
        print("[ConfigLoader] loaded config")
        # optional: show top-level keys
        print("[ConfigLoader] keys:", list(data.keys()))
        return data