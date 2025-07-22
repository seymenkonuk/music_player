# ============================================================================
# File:    artistView.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from screen.music import MusicScreen


class ArtistView(QFrame):
	def __init__(self, artistName, image, mainScreen: 'MusicScreen'):
		super().__init__()
		# 
		self.__mainScreen = mainScreen
		# 
		self.__artistName = artistName
		self.__image = image
		# 
		self.__initUI()

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.__mainScreen.updateHeaderBar(f"Sanatçılar > {self.__artistName}")
			songlist = self.__mainScreen.getArtistSong(self.__artistName)
			self.__mainScreen.updateListBarWithSonglist(songlist)

	def __initUI(self):
		self.setObjectName("artist_view")
		musicCount = self.__mainScreen.getArtistSongCount(self.__artistName)
		# Artist Image
		icon = QLabel()
		icon.setPixmap(QPixmap(self.__image).scaled(40, 40))
		icon.setFixedWidth(40)
		# Artist Name
		artistNameLabel = QLabel(self.__artistName)
		artistNameLabel.setObjectName("primary-color")
		# Music Count
		musicCountLabel = QLabel(f"{musicCount} adet şarkı bulundu")
		musicCountLabel.setObjectName("secondary-color")
		# Layout
		v_box = QVBoxLayout()
		v_box.addWidget(artistNameLabel)
		v_box.addWidget(musicCountLabel)

		h_box = QHBoxLayout()
		h_box.addWidget(icon)
		h_box.addLayout(v_box)

		self.setLayout(h_box)
