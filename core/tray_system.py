from PySide6 import QtWidgets, QtGui
from general.config_loader.config_loader import ConfigLoader
from general.modules_importer.modules_manager import ModulesManager
from core.tray_item import TrayItem
import os

class TraySystem(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon_manager, root_path, parent=None):
        super().__init__(QtGui.QIcon(icon_manager.main_icon), parent)
        self.setToolTip("PUZZLE Tool Collection")
        self.menu = QtWidgets.QMenu(parent)
        self.root_path = root_path

        try:
            config = ConfigLoader.load_config()
            self.ui_style = config.get("common", {}).get("ui_style_sheet", "")
        except Exception as e:
            print("[TraySystem] config load failed:", e)
            self.ui_style = ""

        self.load_tools(icon_manager, self.root_path)
        self.menu.addSeparator()

        exit_action = self.menu.addAction("Exit")
        exit_action.setIcon(QtGui.QIcon(icon_manager.exit_icon))
        exit_action.triggered.connect(lambda: QtWidgets.QApplication.quit())
        self.setContextMenu(self.menu)
        self.activated.connect(self.show_menu)

    def getCustomStyle(self) -> str:
        style_path = os.path.join(self.root_path, self.ui_style).replace("\\", "/")
        return style_path

    def show_menu(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.contextMenu().popup(QtGui.QCursor.pos())

    def load_tools(self, icon_manager, root_path):
        try:
            modules = ModulesManager.import_modules_from_folder(
                root_path=root_path,
                subfolder="launch",
                prefix="launch"
            )
        except Exception as e:
            print("[TraySystem] failed to import modules:", e)
            return

        for mod in modules:
            if not hasattr(mod, "LauncherFunction"):
                print(f"[Warning] Module {mod.__name__} does not define 'LauncherFunction'")
                continue

            try:
                launcher = mod.LauncherFunction()
                info = launcher.main()
            except Exception as e:
                print(f"[TraySystem] launcher {mod.__name__} failed:", e)
                continue

            for name, data in info.items():
                tool_info = TrayItem.ToolInfo(
                    name=name,
                    icon_path=data[1],
                    exe_path=data[2],
                    lib=data[3],
                    command=data[4],
                    launcher=launcher
                )
                item = TrayItem(tool=tool_info, parent=self.menu)
                self.menu.addAction(item)
