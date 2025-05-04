from PySide6 import QtWidgets
from puzzle_2d_symbol_generator.ui.Symbols_2D_Tag import Ui_widgetTag

class Symbols_2D_Custom_Tag(QtWidgets.QWidget, Ui_widgetTag):
	def __init__(self, text, on_close):
		super(Symbols_2D_Custom_Tag, self).__init__()
		self.setupUi(self)
		self.text = text
		self.on_close = on_close

		self.lbTag.setText(text)
		self.btnRemove.clicked.connect(lambda: self.on_close(self))
