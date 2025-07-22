# ============================================================================
# File:    login.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QLineEdit

from dialog.infoDialog import InfoDialog
from dialog.newPassword import NewPasswordDialog
from dialog.verificationDialog import VerificationDialog
from dialog.warningDialog import WarningDialog

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from main import AppWindow


class LoginScreen(QFrame):
	def __init__(self, mainWindow: 'AppWindow'):
		super().__init__()
		# 
		self.__mainWindow = mainWindow
		# 
		self.__initUI()

	def __initUI(self):
		# Login Title Label
		title = QLabel("Giriş Yap")
		title.setObjectName("menu_title")
		title.setAlignment(Qt.AlignCenter)
		# Email Input
		email = QLabel("Email")
		self.__email_edit = QLineEdit()
		self.__email_edit.setObjectName("menu_input")
		# Password Input
		password = QLabel("Şifre")
		self.__password_edit = QLineEdit()
		self.__password_edit.setObjectName("menu_input")
		self.__password_edit.setEchoMode(QLineEdit.Password)
		# Remember Me CheckBox
		self.__rememberme = QCheckBox()
		self.__rememberme.setObjectName("remember_me")
		self.__rememberme.setText("Beni Hatırla")
		# Reset Password Button
		reset = QPushButton()
		reset.setObjectName("clickable_label")
		reset.setText("Şifremi Unuttum")
		reset.clicked.connect(self.__resetPasswordRequest)
		# Confirm Button
		confirm = QPushButton()
		confirm.setText("Giriş Yap")
		confirm.setObjectName("menu_button")
		confirm.clicked.connect(self.__confirm)
		# Sign Up Menu Button
		signUp = QPushButton()
		signUp.setText("Kayıt Ol")
		signUp.setObjectName("menu_button")
		signUp.clicked.connect(self.__signUp)
		# Main Menu Button
		mainMenu = QPushButton()
		mainMenu.setText("Girişe Dön")
		mainMenu.setObjectName("menu_button")
		mainMenu.clicked.connect(self.__returnMainMenu)
		# Layout
		h_box = QHBoxLayout()
		h_box.addWidget(self.__rememberme)
		h_box.addStretch()
		h_box.addWidget(reset)
		h_box.setContentsMargins(0,0,0,16)

		h_box2 = QHBoxLayout()
		h_box2.addWidget(signUp)
		h_box2.addWidget(mainMenu)
		h_box2.setSpacing(16)

		v_box = QVBoxLayout()
		v_box.setSpacing(10)

		v_box.addStretch()
		v_box.addWidget(title)
		v_box.addWidget(email)
		v_box.addWidget(self.__email_edit)
		v_box.addWidget(password)
		v_box.addWidget(self.__password_edit)
		v_box.addLayout(h_box)
		v_box.addWidget(confirm)
		v_box.addLayout(h_box2)
		v_box.addStretch()

		h_box = QHBoxLayout()
		h_box.addStretch()
		h_box.addLayout(v_box)
		h_box.addStretch()

		self.setLayout(h_box)

	def __signUp(self):
		self.__mainWindow.switchSignupScreen()

	def __returnMainMenu(self):
		self.__mainWindow.switchHomeScreen()

	def __frontend_validation(self):
		if len(self.__email_edit.text()) < 5:
			dialog = WarningDialog(self, "Email adresi 5 karakterden kısa olamaz!")
			dialog.exec_()
			return False

		if len(self.__password_edit.text()) < 5:
			dialog = WarningDialog(self, "Parola alanı 5 karakterden kısa olamaz!")
			dialog.exec_()
			return False

		return True

	def __confirm(self):
		# Frontend Tarafında Kontrol Yap
		if not self.__frontend_validation():
			return 
		# API'ye İstek Yap
		if not self.__mainWindow.getAuth().login(self.__email_edit.text(), self.__password_edit.text(), self.__rememberme.isChecked()):
			dialog = WarningDialog(self, self.__mainWindow.getAuth().getErrorMessage())
			dialog.exec_()
			return 
		# Giriş başarılı
		self.__mainWindow.switchMusicScreen()

	def __resetPasswordRequest(self):
		# API'ye İstek Yap (Email'in Doğruluğunu Sorgula)
		if not self.__mainWindow.getAuth().resetPasswordRequest(self.__email_edit.text()):
			dialog = WarningDialog(self, self.__mainWindow.getAuth().getErrorMessage())
			dialog.exec_()
			return 
		# Mail ile Gelen Kodu Girmesini Bekle
		dialog = VerificationDialog(self, self.__resetPasswordVerify)
		dialog.exec_()

	def __resetPasswordVerify(self, code):
		# API'ye İstek Yap (Kodun Doğruluğunu Sorgula)
		if not self.__mainWindow.getAuth().resetPasswordVerify(self.__email_edit.text(), code):
			dialog = WarningDialog(self, self.__mainWindow.getAuth().getErrorMessage())
			dialog.exec_()
			return
		# Doğru Kod Girildiyse Yeni Şifreyi İste ve Değiştir
		self.__code = code
		dialog = NewPasswordDialog(self, self.__resetPassword)
		dialog.exec_()

	def __resetPassword(self, newPassword):
		# API'ye İstek Yap (Yeni Parolayı Gönder)
		if not self.__mainWindow.getAuth().resetPassword(self.__email_edit.text(), self.__code, newPassword):
			dialog = WarningDialog(self, self.__mainWindow.getAuth().getErrorMessage())
			dialog.exec_()
			return
		# Parola Değişikliği Gerçekleşti
		dialog = InfoDialog(self, "Şifre Değişikliği Başarılı!")
		dialog.exec_()
		# Menü Değiştir
		self.__mainWindow.switchLoginScreen()
