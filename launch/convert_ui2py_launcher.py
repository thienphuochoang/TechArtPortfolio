import os
import json
from general.modules_importer.modules_manager import ModulesManager
from launch.base_launcher import BaseLauncher
from general.config_loader.config_loader import ConfigLoader

class LauncherFunction(BaseLauncher):
    def __init__(self):
        super().__init__()

        self.root_path = ConfigLoader.get_root_path()
        config_path = os.path.join(self.root_path, "launcher_config.json")
        with open(config_path, "r") as f:
            config = json.load(f)["uiconverter"]

        self.name = config["name"]
        self.library = config["library"]
        self.icon_path = os.path.join(self.root_path, config["icon_path"]).replace("\\", "/")
        self.pyside2uic = os.path.join(self.root_path, config["script_path"]).replace("\\", "/")
        self.file_type = config["file_type"]

    def get_display_icon(self) -> str:
        return self.icon_path

    def search_files(self, start_dir: str, file_type: str):
        ui_files = []
        for cur_path, _, files in os.walk(start_dir):
            for f in files:
                if f.endswith(file_type):
                    ui_files.append(os.path.join(cur_path, f))
        return ui_files

    def build_command(self, ui_file: str):
        py_file = ui_file[:-3] + ".py"
        cmd_line = [
            self.pyside2uic,
            ui_file.replace("\\", "/"),
            "-o",
            py_file.replace("\\", "/")
        ]
        return cmd_line

    def convert(self):
        ui_files = self.search_files(self.root_path, self.file_type)
        return [self.build_command(ui) for ui in ui_files]

    def main(self):
        command_lines = self.convert()
        return {
            self.name: [
                "",                         # No install location needed
                self.get_display_icon(),   # Icon
                "",                         # No exe path
                self.library,              # Library module
                command_lines              # Command lines
            ]
        }

    def get_open_command_line(self, exe_path: str) -> list[str]:
        # Not applicable for UI converter
        return []