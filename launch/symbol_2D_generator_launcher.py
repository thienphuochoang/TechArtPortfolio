import os
import sys
import importlib
from PySide6.QtWidgets import QApplication, QMainWindow
from launch.base_launcher import BaseLauncher
from general.config_loader.config_loader import ConfigLoader


class LauncherFunction(BaseLauncher):
    def __init__(self):
        super().__init__()
        self.root_path = ConfigLoader.get_root_path()
        config = ConfigLoader.load_config()
        ui_config = config["symbols_2d_generator"]

        self.name = ui_config["name"]
        self.library = ui_config["library"]  # e.g., "lib.ui.2D_Symbols_Generator_MainUI"
        self.ui_class_name = ui_config["ui_class"]  # e.g., "Ui_MainWindow"
        self.icon_path = os.path.join(self.root_path, ui_config["icon_path"]).replace("\\", "/")

    def get_display_icon(self) -> str:
        return self.icon_path

    def get_open_command_line(self, exe_path: str = "") -> list[str]:
        return [self.library, self.ui_class_name]

    def launch_ui(self):
        """Create and display the UI using imported Ui_MainWindow."""
        try:
            module = importlib.import_module(self.library)
            UiClass = getattr(module, self.ui_class_name)

            app = QApplication.instance()
            if not app:
                app = QApplication(sys.argv)

            # Prevent closing the whole tray system
            app.setQuitOnLastWindowClosed(False)

            # Store references as instance attributes
            self.window = QMainWindow()
            self.ui = UiClass()
            self.ui.setupUi(self.window)
            self.window.show()

            # Do not call sys.exit() in a plugin/tray context
            # App event loop already running in main process
            # Only call app.exec() if you're testing in isolation
            if not QApplication.instance().thread().isRunning():
                app.exec()

        except Exception as e:
            print(f"[Error] Failed to launch UI: {e}")
            import traceback
            traceback.print_exc()

    def main(self) -> dict:
        return {
            self.name: [
                "",
                self.get_display_icon(),
                "",
                self.library,
                self.get_open_command_line()
            ]
        }