from launch.base_launcher import BaseLauncher
from general.config_loader.config_loader import ConfigLoader
import os
import ctypes
from ctypes.wintypes import MAX_PATH
import winreg

class LauncherFunction(BaseLauncher):
    def __init__(self):
        super().__init__()

        self.root_path = ConfigLoader.get_root_path()
        config = ConfigLoader.load_config()
        self.config = config["maya"]
        self.common = config["common"]

        self.versions = self.config["versions"]
        self.library = self.config["library"]
        self.exe_subpath = self.config["exe_subpath"]
        self.icon_keyword = self.config["icon_keyword"]
        self.registry_key_template = self.config["registry_key_template"]
        self.registry_value = self.config["registry_value"]
        self.env_var = self.common["root_env_var"]
        self.external_modules = os.path.join(self.root_path, self.common["external_modules_path"])

    def get_open_command_line(self, exe_path):
        return [
            exe_path,
            "-c",
            f"python(\"import sys; sys.path.append('{self.root_path}'); "
            f"sys.path.append('{self.external_modules}'); "
            f"from {self.library} import startup; startup.main()\")"
        ]

    def save_root_to_maya_env(self, version):
        buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
        if ctypes.windll.shell32.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
            user_docs = buf.value.replace("\\", "/")
            env_path = os.path.join(user_docs, "maya", version, "Maya.env")
            os.makedirs(os.path.dirname(env_path), exist_ok=True)

            with open(env_path, "a+") as f:
                f.seek(0)
                lines = f.readlines()
                if self.env_var not in "".join(lines):
                    f.write(f"\n{self.env_var} = {self.root_path}\n")

    def main(self):
        result = {}
        for version in self.versions:
            reg_key = self.registry_key_template.format(version=version)
            location = self.get_installed_location(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY, reg_key, self.registry_value)
            if not location:
                continue

            exe_path = os.path.join(location, self.exe_subpath)
            if not os.path.isfile(exe_path):
                continue

            icon = self.get_icon_path(location, self.icon_keyword)
            cmd = self.get_open_command_line(exe_path)
            self.save_root_to_maya_env(version)
            result[f"Maya {version}"] = [location, icon, exe_path, self.library, cmd]
        return result