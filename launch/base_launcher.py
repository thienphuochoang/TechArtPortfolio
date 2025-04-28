import os
import sys
import winreg
from abc import ABC, abstractmethod
from typing import Optional


class BaseLauncher(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def main(self):
        pass

    @abstractmethod
    def get_open_command_line(self, exe_path: str) -> list[str]:
        """Return the command line list to launch the tool."""
        pass

    def get_installed_location(self, hive, flag, key_path: str, value_name: str) -> Optional[str]:
        try:
            with winreg.OpenKey(winreg.ConnectRegistry(None, hive), key_path, 0, winreg.KEY_READ | flag) as aKey:
                location, _ = winreg.QueryValueEx(aKey, value_name)
                return location.replace("\\", "/")
        except FileNotFoundError:
            return None

    def get_icon_path(self, base_path: str, keyword: str) -> Optional[str]:
        icon_dir = os.path.join(base_path, "icons")
        for file in os.listdir(icon_dir):
            if keyword in file.lower():
                return os.path.join(icon_dir, file).replace("\\", "/")
        return None
