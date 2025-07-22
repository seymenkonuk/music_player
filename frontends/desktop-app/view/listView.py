# ============================================================================
# File:    listView.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from config import DELETE_ICON_PATH

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from screen.music import MusicScreen


class ListView(QFrame):
	def __init__(self, playlistName, image, mainScreen: 'MusicScreen'):
		super().__init__()
		# 
		self.__mainScreen = mainScreen
		# 
		self.__playlistName = playlistName
		self.__image = image
		# 
		self.__initUI()

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.__mainScreen.updateHeaderBar(f"Oynatma Listeleri > {self.__playlistName}")
			songlist = self.__mainScreen.getPlaylistSong(self.__playlistName)
			self.__mainScreen.updateListBarWithSonglist(songlist, self.__playlistName)

	def __initUI(self):
		self.setObjectName("list_view")
		musicCount = self.__mainScreen.getPlaylistSongCount(self.__playlistName)
		# Playlist Image
		icon = QLabel()
		icon.setPixmap(QPixmap(self.__image).scaled(40, 40))
		icon.setFixedWidth(40)
		# Delete List Button
		self.__deleteList = QPushButton()
		self.__deleteList.setObjectName("transparent_button")
		self.__deleteList.setIcon(QIcon(DELETE_ICON_PATH))
		self.__deleteList.setFixedWidth(40)
		self.__deleteList.clicked.connect(self.__delete)
		self.__deleteList.hide()
		# Playlist Name
		playlistNameLabel = QLabel(self.__playlistName)
		playlistNameLabel.setObjectName("primary-color")
		# Music Count
		musicCountLabel = QLabel(f"{musicCount} adet şarkı bulundu")
		musicCountLabel.setObjectName("secondary-color")
		# Layout
		v_box = QVBoxLayout()
		v_box.addWidget(playlistNameLabel)
		v_box.addWidget(musicCountLabel)

		h_box = QHBoxLayout()
		h_box.addWidget(icon)
		h_box.addLayout(v_box)
		h_box.addWidget(self.__deleteList)

		self.setLayout(h_box)

	def enterEvent(self, a0):
		self.__deleteList.show()
		return super().enterEvent(a0)

	def leaveEvent(self, a0):
		self.__deleteList.hide()
		return super().leaveEvent(a0)

	def __delete(self):
		self.__mainScreen.deletePlaylist(self.__playlistName)
