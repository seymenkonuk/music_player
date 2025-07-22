# ============================================================================
# File:    sidebar.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from screen.music import MusicScreen


class SidebarWidget(QFrame):

	def __init__(self, mainScreen: 'MusicScreen'):
		super().__init__()
		# 
		self.__mainScreen = mainScreen
		# 
		self.__defaultMenu = None
		# 
		self.__windowSettings()
		self.__initUI()

	def __windowSettings(self):
		self.setObjectName("sidebar")

	def __initUI(self):
		v_box = QVBoxLayout()
		v_box.setContentsMargins(10, 10, 10, 10)
		v_box.setSpacing(20)

		for menu in self.__getMenuList():
			menu_v_box = QVBoxLayout()
			menu_v_box.setContentsMargins(0,0,0,0)
			menu_v_box.setSpacing(10)
			for i in range(len(menu)):
				item = None
				if i == 0:
					item = QLabel()
					item.setObjectName("sidebar_title")
				else:
					item = QPushButton()
					item.setObjectName("sidebar_item")
					item.clicked.connect(self.__clickedItem)

				item.setText(menu[i][1])
				menu_v_box.addWidget(item)

				# Default Menu'ye Tıkla
				if len(menu[i]) == 3:
					self.__defaultMenu = item

				if i == 0:
					divider = QLabel()
					divider.setFixedHeight(1)
					divider.setObjectName("sidebar_divider")
					menu_v_box.addWidget(divider)

			widget = QFrame()
			widget.setObjectName("sidebar_menu")
			widget.setLayout(menu_v_box)
			v_box.addWidget(widget)

		v_box.addStretch()
		self.setLayout(v_box)

	def __getMenuList(self):
		if self.__mainScreen.isLoggedIn():
			return self.__getLoggedInMenuList()
		else:
			return self.__getGuestMenuList()

	def __getGuestMenuList(self):
		return [
			[
				["", f"Misafir!"],
				["assets/favicon.png", f"Çıkış Yap"],
			],
			[
				["assets/favicon.png", "Şarkılar"],
				["assets/favicon.png", "Tüm Şarkılar", "default"],
				["assets/favicon.png", "Son Eklenen"],
			],
			[
				["assets/favicon.png", "Sana Özel"],
				["assets/favicon.png", "Beğendiklerin"],
				["assets/favicon.png", "En Çok Dinlediklerin"],
				["assets/favicon.png", "Son Oynatılan"],
			],
			[
				["assets/favicon.png", "Listeler"],
				["assets/favicon.png", "Sanatçılar"],
				["assets/favicon.png", "Oynatma Listeleri"],
			],
		]

	def __getLoggedInMenuList(self):
		return [
			[
				["", f"Hoş Geldin {self.__mainScreen.getAuthName()}!"],
				["assets/favicon.png", f"Çıkış Yap"],
			],
			[
				["assets/favicon.png", "Şarkılar"],
				["assets/favicon.png", "Tüm Şarkılar", "default"],
				["assets/favicon.png", "Son Eklenen"],
			],
			[
				["assets/favicon.png", "Sana Özel"],
				["assets/favicon.png", "Beğendiklerin"],
				["assets/favicon.png", "En Çok Dinlediklerin"],
				["assets/favicon.png", "Son Oynatılan"],
			],
			[
				["assets/favicon.png", "Listeler"],
				["assets/favicon.png", "Sanatçılar"],
				["assets/favicon.png", "Oynatma Listeleri"],
			],
		]

	def __clickedItem(self):
		self.__mainScreen.clickedItem(self.sender().text())

	def getDefaultMenu(self):
		return self.__defaultMenu
