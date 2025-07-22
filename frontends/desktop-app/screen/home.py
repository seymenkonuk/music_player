# ============================================================================
# File:    home.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from main import AppWindow


class HomeScreen(QFrame):
	def __init__(self, mainWindow: 'AppWindow'):
		super().__init__()
		# 
		self.__mainWindow = mainWindow
		# 
		self.__initUI()

	def __initUI(self):
		# App Name Label
		title = QLabel("Müzik Çalar")
		title.setObjectName("menu_title")
		title.setAlignment(Qt.AlignCenter)
		# Login Button
		login = QPushButton()
		login.setText("Giriş Yap")
		login.setObjectName("menu_button")
		login.clicked.connect(self.__login)
		# Signup Button
		signup = QPushButton()
		signup.setText("Kayıt Ol")
		signup.setObjectName("menu_button")
		signup.clicked.connect(self.__signUp)
		# Guest Button
		guest = QPushButton()
		guest.setText("Misafir Olarak Devam Et")
		guest.setObjectName("menu_button")
		guest.clicked.connect(self.__continueAsGuest)
		# Layout
		v_box = QVBoxLayout()
		v_box.setSpacing(10)

		v_box.addStretch()
		v_box.addWidget(title)
		v_box.addWidget(login)
		v_box.addWidget(signup)
		v_box.addWidget(guest)
		v_box.addStretch()

		h_box = QHBoxLayout()
		h_box.addStretch()
		h_box.addLayout(v_box)
		h_box.addStretch()

		self.setLayout(h_box)

	def __login(self):
		self.__mainWindow.switchLoginScreen()

	def __signUp(self):
		self.__mainWindow.switchSignupScreen()

	def __continueAsGuest(self):
		self.__mainWindow.switchMusicScreen()
