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
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
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

        self.tabDataset = QTabWidget(self.centralwidget)
        self.tabDataset.setObjectName(u"tabDataset")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_3 = QGridLayout(self.tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.datasetGroupBox = QGroupBox(self.tab)
        self.datasetGroupBox.setObjectName(u"datasetGroupBox")
        self.gridLayout_2 = QGridLayout(self.datasetGroupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btnAutoTag = QPushButton(self.datasetGroupBox)
        self.btnAutoTag.setObjectName(u"btnAutoTag")
        self.btnAutoTag.setMinimumSize(QSize(50, 50))

        self.verticalLayout.addWidget(self.btnAutoTag)

        self.btnTag = QPushButton(self.datasetGroupBox)
        self.btnTag.setObjectName(u"btnTag")
        self.btnTag.setMinimumSize(QSize(50, 50))

        self.verticalLayout.addWidget(self.btnTag)


        self.gridLayout_2.addLayout(self.verticalLayout, 3, 1, 1, 1)

        self.lstDataset = QListWidget(self.datasetGroupBox)
        self.lstDataset.setObjectName(u"lstDataset")

        self.gridLayout_2.addWidget(self.lstDataset, 3, 0, 1, 1)

        self.cbbDatasetType = QComboBox(self.datasetGroupBox)
        self.cbbDatasetType.setObjectName(u"cbbDatasetType")

        self.gridLayout_2.addWidget(self.cbbDatasetType, 0, 0, 1, 1)

        self.btnFilter = QPushButton(self.datasetGroupBox)
        self.btnFilter.setObjectName(u"btnFilter")

        self.gridLayout_2.addWidget(self.btnFilter, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 4, 0, 1, 1)

        self.widgetTagArea = QWidget(self.datasetGroupBox)
        self.widgetTagArea.setObjectName(u"widgetTagArea")
        self.verticalLayout_2 = QVBoxLayout(self.widgetTagArea)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.gridLayout_2.addWidget(self.widgetTagArea, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.datasetGroupBox, 0, 0, 1, 1)

        self.tabDataset.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabDataset.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabDataset, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabDataset.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.lbSymbolsGeneratorTitle.setText(QCoreApplication.translate("MainWindow", u"2D Symbols Generator", None))
        self.datasetGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Dataset", None))
        self.btnAutoTag.setText(QCoreApplication.translate("MainWindow", u"Auto Tag", None))
        self.btnTag.setText(QCoreApplication.translate("MainWindow", u"Manual Tag", None))
        self.btnFilter.setText(QCoreApplication.translate("MainWindow", u"Filter Tag", None))
        self.tabDataset.setTabText(self.tabDataset.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Dataset", None))
        self.tabDataset.setTabText(self.tabDataset.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
    # retranslateUi

