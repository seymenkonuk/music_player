# ============================================================================
# File:    newPassword.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit

from dialog.infoDialog import InfoDialog

from config import VERIFICATION_ICON_PATH


class NewPasswordDialog(QDialog):
	def __init__(self, parent: QWidget, callback):
		super().__init__(parent)
		# 
		self.__callback = callback
		# 300 saniye içinde kod girilmezse kapansın
		QTimer.singleShot(300000, self.__timeoutTimer)
		# 
		self.__initUI()

	def __initUI(self):
		# Title
		self.setWindowTitle("ŞİFRE DEĞİŞTİR!")
		self.setWindowIcon(QtGui.QIcon(VERIFICATION_ICON_PATH))
		self.setMinimumWidth(300)
		# Label
		title = QLabel("\n" + "Yeni şifrenizi giriniz:" + "\n")
		title.setAlignment(Qt.AlignCenter)
		# New Password Input
		self.__password = QLineEdit()
		self.__password.setEchoMode(QLineEdit.Password)
		self.__password.setObjectName("menu_input")
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
		v_box.addWidget(self.__password)
		v_box.addLayout(h_box)

		self.setLayout(v_box)

	def __confirm(self):
		self.__callback(self.__password.text())
		self.close()

	def __timeoutTimer(self):
		dialog = InfoDialog(self, "Zaman Doldu!")
		dialog.exec_()
		self.close()
