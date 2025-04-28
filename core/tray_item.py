from PySide6 import QtWidgets, QtGui
import subprocess
from dataclasses import dataclass
from typing import Optional

class TrayItem(QtWidgets.QWidgetAction):
    @dataclass
    class ToolInfo:
        name: str
        icon_path: str
        exe_path: str
        lib: str
        command: list
        launcher: Optional[object] = None

    def __init__(self, tool:ToolInfo, parent=None):
        super().__init__(parent)
        self.tool = tool

        self.setText(tool.name)
        self.setIcon(QtGui.QIcon(tool.icon_path))
        self.triggered.connect(self.start)

    def start(self):
        try:
            if self.tool.launcher and hasattr(self.tool.launcher, "launch_ui"):
                self.tool.launcher.launch_ui()
                return

            # Fallback to command-line
            if isinstance(self.tool.command[0], list):
                for cmd in self.tool.command:
                    subprocess.call(cmd)
            else:
                subprocess.Popen(self.tool.command)

        except Exception as e:
            print(f"Error running {self.tool.name}: {e}")
            try:
                subprocess.Popen(self.tool.exe_path)
            except Exception as fallback_error:
                print(f"Fallback launch failed: {fallback_error}")