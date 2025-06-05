from PySide6.QtWidgets import QWidget, QListWidgetItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsScene
from puzzle_2d_symbol_generator.ui.Symbols_2D_View import Ui_Form

class Symbols_2D_Custom_View(QWidget, Ui_Form):
    def __init__(self, image_path: str, tag_text: str):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Setup image
        pixmap = QPixmap(image_path)
        scene = QGraphicsScene()
        scene.addPixmap(pixmap)
        self.ui.graphicsImage.setScene(scene)
        self.ui.graphicsImage.fitInView(scene.itemsBoundingRect(), Qt.KeepAspectRatio)

        # Setup tag text
        self.ui.txtEditImageTag.setReadOnly(True)
        self.ui.txtEditImageTag.setPlainText(tag_text)