# ============================================================================
# File:    listBar.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

from view.musicView import MusicView
from view.artistView import ArtistView
from view.listView import ListView

from PyQt5.QtWidgets import QFrame, QVBoxLayout

from config import MUSIC_ICON_PATH, ARTIST_ICON_PATH, PLAYLIST_ICON_PATH

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from screen.music import MusicScreen


class ListMusicWidget(QFrame):
	def __init__(self, mainScreen: 'MusicScreen'):
		super().__init__()
		# 
		self.__viewedList = []
		self.__activeSongIndex = -1
		# 
		self.__mainScreen = mainScreen
		# 
		self.__initUI()

	def getViewedList(self):
		return self.__viewedList

	def __initUI(self):
		self.setObjectName("list_bar")
		# Layout
		self.__v_box = QVBoxLayout()
		self.__v_box.addStretch()
		self.setLayout(self.__v_box)

	def __cleanList(self):
		while self.__v_box.count() > 1:
			item = self.__v_box.takeAt(0)
			item.widget().deleteLater()

	def __changeObjectName(self, widget, new_object_name):
		widget.setObjectName(new_object_name)
		widget.style().unpolish(widget)
		widget.style().polish(widget)
		widget.update()		

	def activeSong(self, song):
		# Eski Aktif Müziğin Arkaplanını Düzelt
		if self.__activeSongIndex != -1:
			self.__changeObjectName(self.__v_box.itemAt(self.__activeSongIndex).widget(), "music_view")
		# Yeni Aktif Müziğin Arkaplanını İşaretle
		if song in self.__viewedList:
			self.__activeSongIndex = self.__viewedList.index(song)
			self.__changeObjectName(self.__v_box.itemAt(self.__activeSongIndex).widget(), "active_music_view")
			self.__mainScreen.toScroll(self.__v_box.itemAt(self.__activeSongIndex).widget())


	def stopSong(self):
		# Eski Aktif Müziğin Arkaplanını Düzelt
		if self.__activeSongIndex != -1:
			self.__changeObjectName(self.__v_box.itemAt(self.__activeSongIndex).widget(), "music_view")
		self.__activeSongIndex = -1

	def updateList(self, songlist, playlistName):
		self.__viewedList = list(filter(lambda song : self.__mainScreen.songExists(song["music_url"]), songlist))
		self.__activeSongIndex = -1
		self.__cleanList()
		for song in self.__viewedList:
			# Sondan Bir Öncesine Ekle (sonuncu her zaman stretch)
			self.__v_box.insertWidget(self.__v_box.count() - 1, MusicView(
				song, playlistName, MUSIC_ICON_PATH, self.__mainScreen
			))

	def updateArtistList(self, artistList):
		self.__viewedList = []
		self.__activeSongIndex = -1
		self.__cleanList()
		for artist in artistList:
			# Sondan Bir Öncesine Ekle (sonuncu her zaman stretch)
			self.__v_box.insertWidget(self.__v_box.count() - 1, ArtistView(
				artist, ARTIST_ICON_PATH, self.__mainScreen
			))

	def updatePlaylist(self, playlists):
		self.__viewedList = []
		self.__activeSongIndex = -1
		self.__cleanList()
		for playlist in playlists:
			# Sondan Bir Öncesine Ekle (sonuncu her zaman stretch)
			self.__v_box.insertWidget(self.__v_box.count() - 1, ListView(
				playlist, PLAYLIST_ICON_PATH, self.__mainScreen
			))
