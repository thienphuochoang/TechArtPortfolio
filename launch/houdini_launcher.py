import os
import winreg
from general.config_loader.config_loader import ConfigLoader
from launch.base_launcher import BaseLauncher


class LauncherFunction(BaseLauncher):
    def __init__(self):
        super().__init__()

        config = ConfigLoader.load_config()
        self.config = config["houdini"]

        self.library = self.config["library"]
        self.registry_base_key = self.config["registry_base_key"]
        self.registry_value_install_path = self.config["registry_value_install_path"]
        self.registry_value_version = self.config["registry_value_version"]
        self.exe_subpath = self.config["exe_subpath"]
        self.icon_subdir = self.config["icon_subdir"]
        self.icon_filename = self.config["icon_filename"]

    def get_installed_versions(self):
        install_dict = {}
        try:
            base = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                self.registry_base_key,
                0,
                winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
            )
            for i in range(winreg.QueryInfoKey(base)[0]):
                try:
                    subkey_name = winreg.EnumKey(base, i)
                    subkey = winreg.OpenKey(base, subkey_name)
                    install_path = winreg.QueryValueEx(subkey, self.registry_value_install_path)[0].replace("\\", "/")
                    version = winreg.QueryValueEx(subkey, self.registry_value_version)[0]
                    install_dict[install_path] = version
                except Exception:
                    continue
        except FileNotFoundError:
            pass
        return install_dict

    def get_display_icon(self, install_path: str) -> str | None:
        icon_dir = os.path.join(install_path, self.icon_subdir)
        if not os.path.isdir(icon_dir):
            return None
        for file in os.listdir(icon_dir):
            if file.lower() == self.icon_filename.lower():
                return os.path.join(icon_dir, file).replace("\\", "/")
        return None

    def get_exe_path(self, install_path: str) -> str | None:
        exe_path = os.path.join(install_path, self.exe_subpath).replace("\\", "/")
        return exe_path if os.path.isfile(exe_path) else None

    def get_library(self) -> str:
        return self.library

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
            info_dict[f"Houdini FX {version}"] = [install_path, icon, exe, self.library, command]
        return info_dict