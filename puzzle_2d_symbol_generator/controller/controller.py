from PySide6.QtWidgets import QMainWindow
from puzzle_2d_symbol_generator.function.symbol_2d_generator_function import Symbol2DGeneratorFunction
from puzzle_2d_symbol_generator.ui.Symbols_2D_Generator_MainUI import Ui_MainWindow
from puzzle_2d_symbol_generator.ui.Symbols_2D_Tag_Bar import Symbols_2D_Tag_Bar

class Symbol2DGeneratorController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = None
        self.model = None
        self.tag_bar = None
        self.initialize_ui()
        self.initialize_model()
        self.setup_connections()

    def initialize_ui(self):
        # Instantiate the view
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tag_bar = Symbols_2D_Tag_Bar()

    def initialize_model(self):
        # Instantiate the model
        self.model = Symbol2DGeneratorFunction()

    def setup_connections(self):
        self.ui.btnFilter.clicked.connect(self.auto_generate_captions)
        self.ui.widgetTagArea.layout().addWidget(self.tag_bar)

    def download_on_google(self):
        self.model.search_on_google()

    def delete_irrelevant_images(self):
        self.model.delete_irrelevant_images()

    def auto_generate_captions(self):
        self.model.auto_generate_captions()

    def download_and_delete_irrelevant_images(self):
        self.download_on_google()
        self.delete_irrelevant_images()