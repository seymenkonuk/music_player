# ============================================================================
# File:    signup.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit

from dialog.infoDialog import InfoDialog
from dialog.verificationDialog import VerificationDialog
from dialog.warningDialog import WarningDialog

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from main import AppWindow


class SignupScreen(QFrame):
	def __init__(self, mainWindow: 'AppWindow'):
		super().__init__()
		# 
		self.__mainWindow = mainWindow
		# 
		self.__initUI()

	def __initUI(self):
		# Sign Up Title Label
		title = QLabel("Kayıt Ol")
		title.setObjectName("menu_title")
		title.setAlignment(Qt.AlignCenter)
		# Email Input
		email = QLabel("Email")
		self.__email_edit = QLineEdit()
		self.__email_edit.setObjectName("menu_input")
		# Name Input
		name = QLabel("İsim")
		self.__name_edit = QLineEdit()
		self.__name_edit.setObjectName("menu_input")
		# Surname Input
		surname = QLabel("Soyisim")
		self.__surname_edit = QLineEdit()
		self.__surname_edit.setObjectName("menu_input")
		# Password Input
		password = QLabel("Şifre")
		self.__password_edit = QLineEdit()
		self.__password_edit.setObjectName("menu_input")
		self.__password_edit.setEchoMode(QLineEdit.Password)
		# Repassword Input
		repassword = QLabel("Şifre Tekrarı")
		self.__repassword_edit = QLineEdit()
		self.__repassword_edit.setObjectName("menu_input")
		self.__repassword_edit.setEchoMode(QLineEdit.Password)
		# Confirm Button
		confirm = QPushButton()
		confirm.setText("Kayıt Ol")
		confirm.setObjectName("menu_button")
		confirm.clicked.connect(self.__confirm)
		# Login Menu Button
		login = QPushButton()
		login.setText("Giriş Yap")
		login.setObjectName("menu_button")
		login.clicked.connect(self.__logIn)
		# Main Menu Button
		mainMenu = QPushButton()
		mainMenu.setText("Girişe Dön")
		mainMenu.setObjectName("menu_button")
		mainMenu.clicked.connect(self.__returnMainMenu)
		# Layout
		h_box = QHBoxLayout()
		h_box.addWidget(login)
		h_box.addWidget(mainMenu)
		h_box.setSpacing(16)

		v_box = QVBoxLayout()
		v_box.setSpacing(10)

		v_box.addStretch()
		v_box.addWidget(title)
		v_box.addWidget(email)
		v_box.addWidget(self.__email_edit)
		v_box.addWidget(name)
		v_box.addWidget(self.__name_edit)
		v_box.addWidget(surname)
		v_box.addWidget(self.__surname_edit)
		v_box.addWidget(password)
		v_box.addWidget(self.__password_edit)
		v_box.addWidget(repassword)
		v_box.addWidget(self.__repassword_edit)
		v_box.addWidget(confirm)
		v_box.addLayout(h_box)
		v_box.addStretch()

		h_box = QHBoxLayout()
		h_box.addStretch()
		h_box.addLayout(v_box)
		h_box.addStretch()

		self.setLayout(h_box)

	def __logIn(self):
		self.__mainWindow.switchLoginScreen()

	def __returnMainMenu(self):
		self.__mainWindow.switchHomeScreen()

	def __frontend_validation(self):
		if len(self.__email_edit.text()) < 5:
			dialog = WarningDialog(self, "Email adresi 5 karakterden kısa olamaz!")
			dialog.exec_()
			return False

		if len(self.__name_edit.text()) < 2:
			dialog = WarningDialog(self, "İsim alanı 2 karakterden kısa olamaz!")
			dialog.exec_()
			return False

		if len(self.__surname_edit.text()) < 2:
			dialog = WarningDialog(self, "Soyisim alanı 2 karakterden kısa olamaz!")
			dialog.exec_()
			return False

		if len(self.__password_edit.text()) < 5:
			dialog = WarningDialog(self, "Parola alanı 5 karakterden kısa olamaz!")
			dialog.exec_()
			return False

		if self.__password_edit.text() != self.__repassword_edit.text():
			dialog = WarningDialog(self, "Parolalar aynı değil!")
			dialog.exec_()
			return False
		
		return True

	def __confirm(self):
		# Frontend Tarafında Kontrol Yap
		if not self.__frontend_validation():
			return 
		# API'ye İstek Yap
		if not self.__mainWindow.getAuth().signup(self.__email_edit.text(), self.__password_edit.text(), self.__name_edit.text(), self.__surname_edit.text()):
			dialog = WarningDialog(self, self.__mainWindow.getAuth().getErrorMessage())
			dialog.exec_()
			return 
		# Mail ile Gelen Kodu Girmesini Bekle
		dialog = VerificationDialog(self, self.__emailVerify)
		dialog.exec_()

	def __emailVerify(self, code):
		# API'ye İstek Yap (Kodun Doğruluğunu Sorgula)
		if not self.__mainWindow.getAuth().emailVerify(self.__email_edit.text(), code):
			dialog = WarningDialog(self, self.__mainWindow.getAuth().getErrorMessage())
			dialog.exec_()
			return 
		# Kayıt Başarıyla Gerçekleşti
		dialog = InfoDialog(self, "Kayıt Başarılı!")
		dialog.exec_()
		# Menü Değiştir
		self.__mainWindow.switchLoginScreen()
