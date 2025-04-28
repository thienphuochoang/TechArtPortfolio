import os
import winreg
from general.config_loader.config_loader import ConfigLoader
from launch.base_launcher import BaseLauncher


class LauncherFunction(BaseLauncher):
    def __init__(self):
        super().__init__()

        config = ConfigLoader.load_config()["substance_designer"]
        self.library = config["library"]
        self.registry_key = config["registry_key"]
        self.search_keyword = config["search_keyword"]
        self.value_install = config["registry_value_install_path"]
        self.value_name = config["registry_value_display_name"]
        self.value_version = config["registry_value_version"]
        self.exe_filename = config["exe_filename"]
        self.icon_subpath = config["icon_subpath"]

    def get_installed_versions(self) -> dict:
        results = {}
        try:
            base = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.registry_key, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            for i in range(winreg.QueryInfoKey(base)[0]):
                try:
                    subkey_name = winreg.EnumKey(base, i)
                    subkey = winreg.OpenKey(base, subkey_name)

                    display_name = winreg.QueryValueEx(subkey, self.value_name)[0]
                    if self.search_keyword.lower() not in display_name.lower():
                        continue

                    path = winreg.QueryValueEx(subkey, self.value_install)[0].replace("\\", "/")
                    version = winreg.QueryValueEx(subkey, self.value_version)[0]
                    results[path] = version
                except (FileNotFoundError, OSError):
                    continue
        except FileNotFoundError:
            pass
        return results

    def get_exe_path(self, install_path: str) -> str | None:
        exe_path = os.path.join(install_path, self.exe_filename).replace("\\", "/")
        return exe_path if os.path.isfile(exe_path) else None

    def get_display_icon(self, install_path: str) -> str | None:
        icon_path = os.path.join(install_path, self.icon_subpath).replace("\\", "/")
        return icon_path if os.path.isfile(icon_path) else None

    def get_open_command_line(self, exe_path: str) -> list[str]:
        return [exe_path]

    def main(self) -> dict:
        info_dict = {}
        for install_path, version in self.get_installed_versions().items():
            exe = self.get_exe_path(install_path)
            if not exe:
                continue

            icon = self.get_display_icon(install_path)
            command = self.get_open_command_line(exe)

            info_dict[f"Substance Designer {version}"] = [
                install_path,
                icon,
                exe,
                self.library,
                command
            ]
        return info_dict