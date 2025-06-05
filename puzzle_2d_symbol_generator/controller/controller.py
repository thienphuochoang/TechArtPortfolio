from PySide6.QtWidgets import QMainWindow, QListWidgetItem
from PySide6.QtGui import QPixmap, QImage
from puzzle_2d_symbol_generator.function.symbol_2d_generator_function import Symbol2DGeneratorFunction
from puzzle_2d_symbol_generator.ui.Symbols_2D_Generator_MainUI import Ui_MainWindow
from puzzle_2d_symbol_generator.ui.Symbols_2D_Tag_Bar import Symbols_2D_Tag_Bar
from puzzle_2d_symbol_generator.ui.Symbols_2D_Custom_View import Symbols_2D_Custom_View
import os
import requests

class Symbol2DGeneratorController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = None
        self.model = None
        self.tag_bar = None
        self.initialize_model()
        self.initialize_ui()
        self.setup_connections()

    def initialize_ui(self):
        # Instantiate the view
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tag_bar = Symbols_2D_Tag_Bar()
        self.load_dataset_types()
        self.update_model_drop_down_list()
        self.ui.cbbModelPreset.currentIndexChanged.connect(self.on_model_selected)
        self.update_dataset()

    def initialize_model(self):
        # Instantiate the model
        self.model = Symbol2DGeneratorFunction()

    def setup_connections(self):
        self.ui.btnFilter.clicked.connect(self.generate_image)
        self.ui.widgetTagArea.layout().addWidget(self.tag_bar)
        self.ui.btnAutoTag.clicked.connect(self.auto_generate_captions)
        self.ui.btnAutoSlice.clicked.connect(self.auto_slice)

    def download_on_google(self):
        self.model.search_on_google()

    def generate_image(self):
        #asyncio.run(self.model.generate_image())
        self.model.list_styles_for_model()

    def delete_irrelevant_images(self):
        self.model.delete_irrelevant_images()

    def auto_generate_captions(self):
        self.model.auto_generate_captions(self.ui.cbbDatasetType.currentText())

    def download_and_delete_irrelevant_images(self):
        self.download_on_google()
        self.delete_irrelevant_images()

    def auto_slice(self):
        self.model.slice_with_sam()

    def load_dataset_types(self):
        dataset_folders = self.model.get_dataset_folders()
        if dataset_folders:
            self.ui.cbbDatasetType.clear()
            self.ui.cbbDatasetType.addItems(dataset_folders)
            self.ui.cbbDatasetType.setCurrentIndex(0)
        else:
            print("No dataset folders found.")

    def update_model_drop_down_list(self):
        self.ui.cbbModelPreset.clear()
        for model in self.model.models_data:
            self.ui.cbbModelPreset.addItem(model["name"], model)

        self.ui.cbbModelPreset.setCurrentIndex(0)
        self.on_model_selected(0)

    def set_model_thumbnail(self, model):
        url = model.get("url")
        if not url:
            self.ui.lbModelPresetThumbnail.clear()
            return

        try:
            response = requests.get(url)
            response.raise_for_status()

            image = QImage()
            image.loadFromData(response.content)
            pixmap = QPixmap.fromImage(image)

            self.ui.lbModelPresetThumbnail.setPixmap(pixmap)
            self.ui.lbModelPresetThumbnail.setScaledContents(True)  # Scales to fit
        except Exception as e:
            print(f"Error loading thumbnail: {e}")
            self.ui.lbModelPresetThumbnail.clear()

    def on_model_selected(self, index):
        model = self.ui.cbbModelPreset.itemData(index)
        if model:
            self.set_model_thumbnail(model)

    def update_dataset(self, folder_path: str):
        self.ui.lstDataset.clear()
        image_exts = (".png", ".jpg", ".jpeg")

        for filename in sorted(os.listdir(folder_path)):
            if filename.lower().endswith(image_exts):
                image_path = os.path.join(folder_path, filename)
                tag_path = os.path.splitext(image_path)[0] + ".tag"

                # Load tag text
                tag_text = ""
                if os.path.exists(tag_path):
                    with open(tag_path, "r", encoding="utf-8") as f:
                        tag_text = f.read().strip()

                # Create custom UI item
                widget_item = Symbols_2D_Custom_View(image_path, tag_text)
                list_item = QListWidgetItem()
                list_item.setSizeHint(widget_item.sizeHint())

                # Add to QListWidget
                self.ui.lstDataset.addItem(list_item)
                self.ui.lstDataset.setItemWidget(list_item, widget_item)
