from PySide6.QtWidgets import QWidget, QLineEdit, QScrollArea, QVBoxLayout
from PySide6.QtCore import QTimer
from puzzle_2d_symbol_generator.ui.Symbols_2D_Tag_Layout import Symbols_2D_Tag_Layout
from puzzle_2d_symbol_generator.ui.Symbols_2D_Custom_Tag import Symbols_2D_Custom_Tag

class Symbols_2D_Tag_Bar(QWidget):
    def __init__(self):
        super().__init__()
        self.tags = []

        self.flow_layout = Symbols_2D_Tag_Layout()
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter tag...")
        self.line_edit.returnPressed.connect(self.handle_input)

        self.flow_layout.addWidget(self.line_edit)

        self.container = QWidget()
        self.container.setLayout(self.flow_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.container)
        scroll.setStyleSheet("border: 1px solid lightgray; border-radius: 5px;")

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

    def handle_input(self):
        text = self.line_edit.text().strip()
        if text and text not in self.tags:
            self.add_tag(text)
        self.line_edit.clear()

    def add_tag(self, text):
        tag_widget = Symbols_2D_Custom_Tag(text, self.remove_tag)
        self.tags.append(text)
        self.flow_layout.removeWidget(self.line_edit)
        self.flow_layout.addWidget(tag_widget)
        self.flow_layout.addWidget(self.line_edit)
        self.force_scroll_to_bottom()

    def remove_tag(self, tag_widget):
        self.flow_layout.removeWidget(tag_widget)
        tag_widget.deleteLater()
        self.tags.remove(tag_widget.text)

    def force_scroll_to_bottom(self):
        scroll_area = self.findChild(QScrollArea)
        if scroll_area:
            QTimer.singleShot(0, lambda: scroll_area.ensureWidgetVisible(self.line_edit))
