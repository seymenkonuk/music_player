#!/usr/bin/env python3

# ============================================================================
# File:    main.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

import os
import sys

from string import Template

from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QMessageBox

from helper.auth import Auth
from helper.database import DatabaseControl

from screen.home import HomeScreen
from screen.login import LoginScreen
from screen.music import MusicScreen
from screen.signup import SignupScreen

from dialog.warningDialog import WarningDialog

from config import ENV_PATH, ICON_PATH, STYLE_PATH, SESSION_PATH

from dotenv import load_dotenv

load_dotenv(dotenv_path=ENV_PATH)

isDarkTheme = os.getenv("THEME", "light") == "dark"


class AppWindow(QWidget):
	def __init__(self):
		super().__init__()
		# 
		self.__auth = Auth()
		self.__database = DatabaseControl(self.__auth)
		# 
		self.__windowSettings()
		self.__initUI()
		# 
		self.__controlSession()
		# Ekranda Göster
		self.show()

	def __windowSettings(self):
		self.setObjectName("app_background")
		self.setWindowTitle("Müzik Çalar")
		self.setWindowIcon(QtGui.QIcon(ICON_PATH))
		self.setGeometry(100, 100, 1000, 625)
		self.setMinimumSize(1000, 500)

	def __initUI(self):
		# QSS dosyasını Oku ve Uygula
		with open(STYLE_PATH, "r", encoding="utf-8") as file:
			template = Template(file.read())
		style = template.substitute(
			colorBackgroundDark="#1E1E2F" if isDarkTheme else "#C8CED4",
			colorBackgroundLight="#2A2A3C" if isDarkTheme else "#DCE1E6",

			colorButton="#2A2A3C" if isDarkTheme else "#DCE1E6",
			colorButtonHover="#3A3A4D" if isDarkTheme else "#BAC1C7",

			colorTextLink="#A384FF" if isDarkTheme else "#6A4C93",
			colorTextPrimary="#E0E0E0" if isDarkTheme else "#1C1C1C",
			colorTextSecondary="#9A9AB0" if isDarkTheme else "#4B5056",
		)
		self.setStyleSheet(style)
		# Layout
		self.__v_box = QVBoxLayout()
		self.__v_box.setContentsMargins(0,0,0,0)
		self.__v_box.addWidget(HomeScreen(self))
		self.setLayout(self.__v_box)

	def getAuth(self):
		return self.__auth
	
	def getDatabase(self):
		return self.__database

	def __changeScreen(self, newScreen: QWidget):
		# Eski Ekranı Sil
		item = self.__v_box.takeAt(0)
		item.widget().deleteLater()
		# Yeni Ekranı Ekle
		self.__v_box.addWidget(newScreen)

	def switchHomeScreen(self):
		self.__changeScreen(HomeScreen(self))

	def switchLoginScreen(self):
		self.__changeScreen(LoginScreen(self))

	def switchSignupScreen(self):
		self.__changeScreen(SignupScreen(self))

	def switchMusicScreen(self):
		self.__changeScreen(MusicScreen(self))

	def logout(self):
		self.__auth.logout()
		self.switchHomeScreen()

	def closeEvent(self, event):
		# Hemen Çıkmasını Engelle
		reply = QMessageBox.question(
			self,
			"Çıkış",
			"Çıkmak istediğinize emin misiniz?",
			QMessageBox.Yes | QMessageBox.No,
			QMessageBox.No
		)
		# Eğer Çıkmak İstediğine Eminse
		if reply == QMessageBox.Yes:
			# ve Beni Hatırla Seçili Değilse, API'ye Çıkış Yaptığını Bildir
			if not self.__auth.isRememberMeChecked():
				self.__auth.logout()
			event.accept()
		else:
			event.ignore()

	def __controlSession(self):
		try:
			# Token'ı Oku
			with open(SESSION_PATH, "r", encoding="utf-8") as file:
				token = file.read()
			# API'ye İstek At (Token ile Giriş Yap)
			if not self.__auth.loginWithToken(token):
				self.__deleteSession()
				dialog = WarningDialog(self, self.__auth.getErrorMessage())
				dialog.exec_()
				return 
			# Giriş Başarılı
			self.switchMusicScreen()

		except FileNotFoundError:
			pass

	def __deleteSession(self):
		if os.path.exists(SESSION_PATH):
			os.remove(SESSION_PATH)

if __name__ == '__main__':	
	app = QApplication(sys.argv)
	QApplication.setFont(QFont("Calibri", 10))
	appWindow = AppWindow()
	sys.exit(app.exec_())
