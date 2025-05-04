# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Symbols_2D_Tag.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_widgetTag(object):
    def setupUi(self, widgetTag):
        if not widgetTag.objectName():
            widgetTag.setObjectName(u"widgetTag")
        widgetTag.resize(170, 38)
        widgetTag.setStyleSheet(u"background-color: rgb(185, 185, 185);\n"
"border-radius: 6px;")
        self.horizontalLayout = QHBoxLayout(widgetTag)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, -1, -1)
        self.lbTag = QLabel(widgetTag)
        self.lbTag.setObjectName(u"lbTag")
        self.lbTag.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.horizontalLayout.addWidget(self.lbTag)

        self.btnRemove = QPushButton(widgetTag)
        self.btnRemove.setObjectName(u"btnRemove")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRemove.sizePolicy().hasHeightForWidth())
        self.btnRemove.setSizePolicy(sizePolicy)
        self.btnRemove.setMinimumSize(QSize(20, 20))
        self.btnRemove.setMaximumSize(QSize(20, 20))
        self.btnRemove.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"background-color: white;\n"
"font: 700 9pt \"Segoe UI\";\n"
"border: 1px solid black;\n"
"border-radius: 4px;\n"
"padding: 1px;")

        self.horizontalLayout.addWidget(self.btnRemove)


        self.retranslateUi(widgetTag)

        QMetaObject.connectSlotsByName(widgetTag)
    # setupUi

    def retranslateUi(self, widgetTag):
        widgetTag.setWindowTitle(QCoreApplication.translate("widgetTag", u"Widget Tag", None))
        self.lbTag.setText(QCoreApplication.translate("widgetTag", u"tag content", None))
        self.btnRemove.setText(QCoreApplication.translate("widgetTag", u"x", None))
    # retranslateUi

