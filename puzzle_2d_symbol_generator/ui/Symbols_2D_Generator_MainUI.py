# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Symbols_2D_Generator_MainUI.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 648)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lbSymbolsGeneratorTitle = QLabel(self.centralwidget)
        self.lbSymbolsGeneratorTitle.setObjectName(u"lbSymbolsGeneratorTitle")
        font = QFont()
        font.setPointSize(15)
        self.lbSymbolsGeneratorTitle.setFont(font)
        self.lbSymbolsGeneratorTitle.setStyleSheet(u"background-color: rgb(255, 170, 127);\n"
"color: rgb(85, 0, 0);")
        self.lbSymbolsGeneratorTitle.setFrameShape(QFrame.Shape.StyledPanel)
        self.lbSymbolsGeneratorTitle.setFrameShadow(QFrame.Shadow.Raised)
        self.lbSymbolsGeneratorTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lbSymbolsGeneratorTitle, 0, 0, 1, 1)

        self.tabSymbolGenerator = QTabWidget(self.centralwidget)
        self.tabSymbolGenerator.setObjectName(u"tabSymbolGenerator")
        self.tabLeonardoAiGenerator = QWidget()
        self.tabLeonardoAiGenerator.setObjectName(u"tabLeonardoAiGenerator")
        self.gridLayout_3 = QGridLayout(self.tabLeonardoAiGenerator)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gbLeonardoAiGenerator = QGroupBox(self.tabLeonardoAiGenerator)
        self.gbLeonardoAiGenerator.setObjectName(u"gbLeonardoAiGenerator")
        self.gridLayout_2 = QGridLayout(self.gbLeonardoAiGenerator)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.btnGenerate = QPushButton(self.gbLeonardoAiGenerator)
        self.btnGenerate.setObjectName(u"btnGenerate")
        self.btnGenerate.setMinimumSize(QSize(50, 50))

        self.gridLayout_4.addWidget(self.btnGenerate, 3, 0, 1, 1)

        self.gbImageResolution = QGroupBox(self.gbLeonardoAiGenerator)
        self.gbImageResolution.setObjectName(u"gbImageResolution")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbImageResolution.sizePolicy().hasHeightForWidth())
        self.gbImageResolution.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QVBoxLayout(self.gbImageResolution)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.cbbImageResolution = QComboBox(self.gbImageResolution)
        self.cbbImageResolution.setObjectName(u"cbbImageResolution")

        self.verticalLayout_4.addWidget(self.cbbImageResolution)


        self.gridLayout_4.addWidget(self.gbImageResolution, 1, 0, 1, 1)

        self.gbModelPreset = QGroupBox(self.gbLeonardoAiGenerator)
        self.gbModelPreset.setObjectName(u"gbModelPreset")
        sizePolicy.setHeightForWidth(self.gbModelPreset.sizePolicy().hasHeightForWidth())
        self.gbModelPreset.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.gbModelPreset)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.cbbModelPreset = QComboBox(self.gbModelPreset)
        self.cbbModelPreset.setObjectName(u"cbbModelPreset")

        self.verticalLayout_3.addWidget(self.cbbModelPreset)

        self.lbModelPresetThumbnail = QLabel(self.gbModelPreset)
        self.lbModelPresetThumbnail.setObjectName(u"lbModelPresetThumbnail")
        self.lbModelPresetThumbnail.setMinimumSize(QSize(128, 128))
        self.lbModelPresetThumbnail.setMaximumSize(QSize(128, 128))
        self.lbModelPresetThumbnail.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.lbModelPresetThumbnail)


        self.gridLayout_4.addWidget(self.gbModelPreset, 0, 0, 1, 1)

        self.gbNumberOfImages = QGroupBox(self.gbLeonardoAiGenerator)
        self.gbNumberOfImages.setObjectName(u"gbNumberOfImages")
        sizePolicy.setHeightForWidth(self.gbNumberOfImages.sizePolicy().hasHeightForWidth())
        self.gbNumberOfImages.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.gbNumberOfImages)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.spbNumberOfImages = QSpinBox(self.gbNumberOfImages)
        self.spbNumberOfImages.setObjectName(u"spbNumberOfImages")

        self.verticalLayout_6.addWidget(self.spbNumberOfImages)


        self.gridLayout_4.addWidget(self.gbNumberOfImages, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer, 4, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_4, 3, 0, 2, 1)

        self.lbPrompt = QLabel(self.gbLeonardoAiGenerator)
        self.lbPrompt.setObjectName(u"lbPrompt")

        self.gridLayout_2.addWidget(self.lbPrompt, 2, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btnDownloadFromGoogle = QPushButton(self.gbLeonardoAiGenerator)
        self.btnDownloadFromGoogle.setObjectName(u"btnDownloadFromGoogle")
        self.btnDownloadFromGoogle.setMinimumSize(QSize(50, 50))

        self.verticalLayout.addWidget(self.btnDownloadFromGoogle)

        self.btnAutoTag = QPushButton(self.gbLeonardoAiGenerator)
        self.btnAutoTag.setObjectName(u"btnAutoTag")
        self.btnAutoTag.setMinimumSize(QSize(50, 50))

        self.verticalLayout.addWidget(self.btnAutoTag)

        self.btnTag = QPushButton(self.gbLeonardoAiGenerator)
        self.btnTag.setObjectName(u"btnTag")
        self.btnTag.setMinimumSize(QSize(50, 50))

        self.verticalLayout.addWidget(self.btnTag)

        self.btnAutoSlice = QPushButton(self.gbLeonardoAiGenerator)
        self.btnAutoSlice.setObjectName(u"btnAutoSlice")
        self.btnAutoSlice.setMinimumSize(QSize(50, 50))

        self.verticalLayout.addWidget(self.btnAutoSlice)


        self.gridLayout_2.addLayout(self.verticalLayout, 3, 3, 1, 1)

        self.lbFolder = QLabel(self.gbLeonardoAiGenerator)
        self.lbFolder.setObjectName(u"lbFolder")

        self.gridLayout_2.addWidget(self.lbFolder, 0, 0, 1, 1)

        self.lbTagSearch = QLabel(self.gbLeonardoAiGenerator)
        self.lbTagSearch.setObjectName(u"lbTagSearch")

        self.gridLayout_2.addWidget(self.lbTagSearch, 1, 0, 1, 1)

        self.lstDataset = QListWidget(self.gbLeonardoAiGenerator)
        self.lstDataset.setObjectName(u"lstDataset")
        self.lstDataset.setStyleSheet(u"")
        self.lstDataset.setFrameShape(QFrame.Shape.Panel)
        self.lstDataset.setFrameShadow(QFrame.Shadow.Plain)

        self.gridLayout_2.addWidget(self.lstDataset, 3, 1, 1, 1)

        self.btnFilter = QPushButton(self.gbLeonardoAiGenerator)
        self.btnFilter.setObjectName(u"btnFilter")

        self.gridLayout_2.addWidget(self.btnFilter, 1, 3, 1, 1)

        self.txtePrompt = QTextEdit(self.gbLeonardoAiGenerator)
        self.txtePrompt.setObjectName(u"txtePrompt")
        self.txtePrompt.setFrameShape(QFrame.Shape.Panel)

        self.gridLayout_2.addWidget(self.txtePrompt, 2, 1, 1, 2)

        self.widgetTagArea = QWidget(self.gbLeonardoAiGenerator)
        self.widgetTagArea.setObjectName(u"widgetTagArea")
        self.widgetTagArea.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.widgetTagArea)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_2.addWidget(self.widgetTagArea, 1, 1, 1, 2)

        self.cbbDatasetType = QComboBox(self.gbLeonardoAiGenerator)
        self.cbbDatasetType.setObjectName(u"cbbDatasetType")
        self.cbbDatasetType.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.cbbDatasetType, 0, 1, 1, 2)


        self.gridLayout_3.addWidget(self.gbLeonardoAiGenerator, 0, 0, 1, 1)

        self.tabSymbolGenerator.addTab(self.tabLeonardoAiGenerator, "")
        self.tabDataset = QWidget()
        self.tabDataset.setObjectName(u"tabDataset")
        self.gridLayout_6 = QGridLayout(self.tabDataset)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gbDataset = QGroupBox(self.tabDataset)
        self.gbDataset.setObjectName(u"gbDataset")

        self.gridLayout_6.addWidget(self.gbDataset, 0, 0, 1, 1)

        self.tabSymbolGenerator.addTab(self.tabDataset, "")

        self.gridLayout.addWidget(self.tabSymbolGenerator, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabSymbolGenerator.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.lbSymbolsGeneratorTitle.setText(QCoreApplication.translate("MainWindow", u"2D Symbols Generator", None))
        self.gbLeonardoAiGenerator.setTitle(QCoreApplication.translate("MainWindow", u"Dataset", None))
        self.btnGenerate.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.gbImageResolution.setTitle(QCoreApplication.translate("MainWindow", u"Image Resolution", None))
        self.gbModelPreset.setTitle(QCoreApplication.translate("MainWindow", u"Model/Preset", None))
        self.lbModelPresetThumbnail.setText("")
        self.gbNumberOfImages.setTitle(QCoreApplication.translate("MainWindow", u"Number of Images", None))
        self.lbPrompt.setText(QCoreApplication.translate("MainWindow", u"Prompt", None))
        self.btnDownloadFromGoogle.setText(QCoreApplication.translate("MainWindow", u"Download ref\n"
" from Google", None))
        self.btnAutoTag.setText(QCoreApplication.translate("MainWindow", u"Auto Tag", None))
        self.btnTag.setText(QCoreApplication.translate("MainWindow", u"Manual Tag", None))
        self.btnAutoSlice.setText(QCoreApplication.translate("MainWindow", u"Auto Slice", None))
        self.lbFolder.setText(QCoreApplication.translate("MainWindow", u"Folder", None))
        self.lbTagSearch.setText(QCoreApplication.translate("MainWindow", u"Tag Search", None))
        self.btnFilter.setText(QCoreApplication.translate("MainWindow", u"Filter Tag", None))
        self.tabSymbolGenerator.setTabText(self.tabSymbolGenerator.indexOf(self.tabLeonardoAiGenerator), QCoreApplication.translate("MainWindow", u"Leonardo AI Generator", None))
        self.gbDataset.setTitle(QCoreApplication.translate("MainWindow", u"Dataset", None))
        self.tabSymbolGenerator.setTabText(self.tabSymbolGenerator.indexOf(self.tabDataset), QCoreApplication.translate("MainWindow", u"Tab 2", None))
    # retranslateUi

