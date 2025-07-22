# ============================================================================
# File:    verificationDialog.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit

from dialog.infoDialog import InfoDialog

from config import VERIFICATION_ICON_PATH


class VerificationDialog(QDialog):
	def __init__(self, parent: QWidget, callback):
		super().__init__(parent)
		# 
		self.__callback = callback
		# 180 saniye içinde kod girilmezse kapansın
		QTimer.singleShot(180000, self.__timeoutTimer)
		# 
		self.__initUI()

	def __initUI(self):
		# Title
		self.setWindowTitle("DOĞRULAMA!")
		self.setWindowIcon(QtGui.QIcon(VERIFICATION_ICON_PATH))
		self.setMinimumWidth(300)
		# Label
		title = QLabel("\n" + "Doğrulama kodunu giriniz:" + "\n")
		title.setAlignment(Qt.AlignCenter)
		# Code Input
		self.__code = QLineEdit()
		self.__code.setObjectName("menu_input")
		# Ok Button
		ok = QPushButton()
		ok.setText("Tamam")
		ok.clicked.connect(self.__confirm)
		ok.setObjectName("menu_button")
		# Cancel Button
		cancel = QPushButton()
		cancel.setText("İptal")
		cancel.clicked.connect(self.close)
		cancel.setObjectName("menu_button")
		# Layout
		h_box = QHBoxLayout()
		h_box.addWidget(cancel)
		h_box.addWidget(ok)

		v_box = QVBoxLayout()
		v_box.addWidget(title)
		v_box.addWidget(self.__code)
		v_box.addLayout(h_box)

		self.setLayout(v_box)

	def __confirm(self):
		self.__callback(self.__code.text())
		self.close()

	def __timeoutTimer(self):
		dialog = InfoDialog(self, "Zaman Doldu!")
		dialog.exec_()
		self.close()
