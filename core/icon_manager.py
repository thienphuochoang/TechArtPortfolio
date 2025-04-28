from dataclasses import dataclass
import os

class IconManager:
    @dataclass(frozen=True)
    class IconPaths:
        main_icon: str
        exit_icon: str
        welcome_icon: str

    @staticmethod
    def get_icons(root_path: str) -> "IconManager.IconPaths":
        return IconManager.IconPaths(
            main_icon=os.path.join(root_path, "lib/icon/SystemTray.png"),
            exit_icon=os.path.join(root_path, "lib/icon/exit.jpg"),
            welcome_icon=os.path.join(root_path, "lib/icon/welcome.jpg")
        )