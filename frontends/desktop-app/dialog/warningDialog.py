# ============================================================================
# File:    warningDialog.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QLabel, QPushButton

from config import WARNING_ICON_PATH


class WarningDialog(QDialog):
	def __init__(self, parent: QWidget, title: str):
		super().__init__(parent)
		# 
		self.__title = title
		# 
		self.__initUI()

	def __initUI(self):
		# Title
		self.setWindowTitle("HATA!")
		self.setWindowIcon(QtGui.QIcon(WARNING_ICON_PATH))
		self.setMinimumWidth(300)
		# Label
		title = QLabel("\n" + self.__title + "\n")
		title.setAlignment(Qt.AlignCenter)
		# Ok Button
		ok = QPushButton()
		ok.setText("Tamam")
		ok.clicked.connect(self.close)
		ok.setObjectName("menu_button")
		# Layout
		v_box = QVBoxLayout()
		v_box.addWidget(title)
		v_box.addWidget(ok)
		self.setLayout(v_box)
