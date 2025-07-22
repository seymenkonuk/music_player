# ============================================================================
# File:    musicView.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from dialog.infoDialog import InfoDialog
from dialog.createPlaylist import CreatePlaylistDialog

from config import ADD_ICON_PATH, DELETE_ICON_PATH

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from screen.music import MusicScreen


class MusicView(QFrame):
	def __init__(self, song, playlistName, image, mainScreen: 'MusicScreen'):
		super().__init__()
		# 
		self.__mainScreen = mainScreen
		# 
		self.__song = song
		self.__playlistName = playlistName
		self.__image = image
		# 
		self.__initUI()

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.__mainScreen.playMusic(self.__song, self.__mainScreen.getViewedList())

	def __initUI(self):
		self.setObjectName("music_view")
		# Music Image
		icon = QLabel()
		icon.setPixmap(QPixmap(self.__image).scaled(40, 40))
		icon.setFixedWidth(40)
		# 
		self.__addList = QPushButton()
		self.__addList.setObjectName("transparent_button")
		self.__addList.setIcon(QIcon(ADD_ICON_PATH))
		self.__addList.setFixedWidth(40)
		self.__addList.clicked.connect(self.__add)
		self.__addList.hide()
		# 
		if self.__playlistName != "":
			self.__removeList = QPushButton()
			self.__removeList.setObjectName("transparent_button")
			self.__removeList.setIcon(QIcon(DELETE_ICON_PATH))
			self.__removeList.setFixedWidth(40)
			self.__removeList.clicked.connect(self.__remove)
			self.__removeList.hide()
		# Music Name
		musicname = QLabel(self.__song["music_name"])
		musicname.setObjectName("primary-color")
		# Artist name
		musicartist = QLabel(self.__song["artist_name"])
		musicartist.setObjectName("secondary-color")
		# Layout
		v_box = QVBoxLayout()
		v_box.addWidget(musicname)
		v_box.addWidget(musicartist)

		h_box = QHBoxLayout()
		h_box.addWidget(icon)
		h_box.addLayout(v_box)
		h_box.addWidget(self.__addList)
		if self.__playlistName != "":
			h_box.addWidget(self.__removeList)

		self.setLayout(h_box)

	def enterEvent(self, a0):
		self.__addList.show()
		if self.__playlistName != "":
			self.__removeList.show()
		return super().enterEvent(a0)

	def leaveEvent(self, a0):
		self.__addList.hide()
		if self.__playlistName != "":
			self.__removeList.hide()
		return super().leaveEvent(a0)

	def __add(self):
		dialog = CreatePlaylistDialog(self, self.__successAdd)
		dialog.exec_()

	def __successAdd(self, playlistName):
		self.__mainScreen.addPlaylist(playlistName, self.__song["music_url"])
		dialog = InfoDialog(self, "Oynatma Listesine Başarıyla Eklendi!")
		dialog.exec_()

	def __remove(self):
		if self.__playlistName == "":
			return
		self.__mainScreen.deleteSongFromPlaylist(self.__playlistName, self.__song["music_url"])
