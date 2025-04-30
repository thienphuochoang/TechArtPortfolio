import sys
import getpass
from PySide6 import QtWidgets, QtGui
from core.icon_manager import IconManager
from core.tray_system import TraySystem
from general.config_loader.config_loader import ConfigLoader

if __name__ == '__main__':
    root_path = ConfigLoader.get_root_path()
    sys.path.append(root_path)

    app = QtWidgets.QApplication(sys.argv)

    # use static method to get icons
    icons = IconManager.get_icons(root_path)

    tray = TraySystem(icons, root_path)
    tray.show()
    tray.showMessage(
        "PUZZLE Tool Collection",
        f"Hello {getpass.getuser()}. Hope you have a great day!",
        QtGui.QIcon(icons.welcome_icon)
    )
    sys.exit(app.exec())