import os
import winreg
from launch.base_launcher import BaseLauncher
from general.config_loader.config_loader import ConfigLoader

class LauncherFunction(BaseLauncher):
    def __init__(self):
        super().__init__()

        self.root_path = ConfigLoader.get_root_path()
        config = ConfigLoader.load_config()
        self.config = config["3dsmax"]
        self.common = config["common"]

        self.version_map = self.config["version_map"]
        self.library = self.config["library"]
        self.exe_filename = self.config["exe_filename"]
        self.icon_keyword = self.config["icon_keyword"]
        self.registry_key_template = self.config["registry_key_template"]
        self.registry_value = self.config["registry_value"]

    def get_open_command_line(self, exe_path: str) -> list[str]:
        # 3dsMax startup script path
        startup_script = os.path.join(self.root_path, self.library, "startup.py").replace("\\", "/")
        return [exe_path, "-U", "PythonHost", startup_script]

    def main(self):
        result = {}
        for registry_version, display_version in self.version_map.items():
            # Format registry key path
            reg_key = self.registry_key_template.format(version=registry_version)

            install_path = self.get_installed_location(
                hive=winreg.HKEY_LOCAL_MACHINE,
                flag=winreg.KEY_WOW64_64KEY,
                key_path=reg_key,
                value_name=self.registry_value
            )

            if not install_path:
                continue

            exe_path = os.path.join(install_path, self.exe_filename).replace("\\", "/")
            if not os.path.isfile(exe_path):
                continue

            icon = self.get_icon_path(install_path, self.icon_keyword)
            cmd = self.get_open_command_line(exe_path)

            result[f"3DSMax {display_version}"] = [install_path, icon, exe_path, self.library, cmd]

        return result