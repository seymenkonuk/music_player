# ============================================================================
# File:    music.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QScrollArea

from layout.headerBar import HeaderWidget
from layout.sidebar import SidebarWidget
from layout.listBar import ListMusicWidget
from layout.musicControlBar import MusicWidget

from helper.findMusic import getMusicFiles
from helper.playMusic import MusicPlayer

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from main import AppWindow


class MusicScreen(QFrame):
	def __init__(self, mainWindow: 'AppWindow'):
		super().__init__()
		# 
		self.__mainWindow = mainWindow
		# 
		self.__mediaPlayer = MusicPlayer(self)
		# 
		self.__allLocalSong = None
		self.__allLocalArtistName = None
		#
		self.__ignoreAllOnExit = False
		# 
		self.__initUI()
		# 
		if self.__sidebar.getDefaultMenu() is not None:
			self.__sidebar.getDefaultMenu().click()

	def __initUI(self):
		# Ekran Dörde Bölünecek Bu Dört Kısmı Oluştur
		self.__header = HeaderWidget(self)
		self.__sidebar = SidebarWidget(self)
		self.__listbar = ListMusicWidget(self)
		self.__musicControlBar = MusicWidget(self)
		# Kaydırılabilir Alan (Sidebar)
		scroll_area1 = QScrollArea()
		scroll_area1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		scroll_area1.setFixedWidth(300)
		scroll_area1.setMinimumHeight(500)
		scroll_area1.setObjectName("scroll_area")
		scroll_area1.setWidgetResizable(True)
		scroll_area1.setWidget(self.__sidebar)
		# Kaydırılabilir Alan (Şarkılar Listesi Bunun İçerisinde Olacak)
		self.__scroll_area2 = QScrollArea()
		self.__scroll_area2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.__scroll_area2.setObjectName("scroll_area")
		self.__scroll_area2.setWidgetResizable(True)
		self.__scroll_area2.setWidget(self.__listbar)
		# Layout
		v_box2 = QVBoxLayout()
		v_box2.setContentsMargins(0,0,0,0)
		v_box2.setSpacing(0)
		v_box2.addWidget(self.__header)
		v_box2.addWidget(self.__scroll_area2)

		v_box3 = QVBoxLayout()
		v_box3.setContentsMargins(0,0,0,0)
		v_box3.setSpacing(0)
		v_box3.addWidget(scroll_area1)

		h_box = QHBoxLayout()
		h_box.setContentsMargins(0,0,0,0)
		h_box.setSpacing(0)
		h_box.addLayout(v_box3)
		h_box.addLayout(v_box2)

		v_box1 = QVBoxLayout()
		v_box1.setContentsMargins(0,0,0,0)
		v_box1.setSpacing(0)
		v_box1.addLayout(h_box)
		v_box1.addWidget(self.__musicControlBar)

		self.setLayout(v_box1)
	
	def isLoggedIn(self):
		return self.__mainWindow.getAuth().isLoggedIn()
	
	def getAuthName(self):
		return self.__mainWindow.getAuth().getName()

	def getAllLocalSong(self):
		if self.__allLocalSong is None:
			self.__allLocalSong = getMusicFiles()
		return self.__allLocalSong

	def getAllLocalArtistName(self):
		if self.__allLocalArtistName is None:
			artistNames = map(lambda song : song["artist_name"], self.getAllLocalSong())
			uniqueArtistNames = set(artistNames)
			self.__allLocalArtistName = sorted(list(uniqueArtistNames), key=lambda artist_name : artist_name.lower())
		return self.__allLocalArtistName

	def getArtistSong(self, artistName):
		return sorted(list(filter(lambda song : song["artist_name"] == artistName, self.getAllLocalSong())), key=lambda song : song["music_name"].lower())

	def getArtistSongCount(self, artistName):
		return len(self.getArtistSong(artistName))

	def getAllPlaylist(self):
		return list( self.__mainWindow.getDatabase().readAllPlaylist())

	def getPlaylistSong(self, playlistName):
		return list(self.__mainWindow.getDatabase().readPlaylistSong(playlistName))

	def getPlaylistSongCount(self, playlistName):
		return len(self.getPlaylistSong(playlistName))

	def getLikedSong(self):
		return self.__mainWindow.getDatabase().readLikedSong()

	def getMostListenedSong(self):
		return self.__mainWindow.getDatabase().readMostListenedSong()

	def getRecentlyPlayedSong(self):
		return self.__mainWindow.getDatabase().readHistoryDistinct()

	def getActiveList(self):
		return self.__mediaPlayer.getActiveList()

	def getViewedList(self):
		return self.__listbar.getViewedList()

	def songExists(self, music_url):
		# Local Dosya Cihazda Mevcut İse
		if QUrl(music_url).isLocalFile():
			if os.path.isfile(QUrl(music_url).toLocalFile()):
				return True
		# Uzak Dosya Giriş Yapıldıysa
		else:
			if self.isLoggedIn():
				return True
		return False

	def playMusic(self, song, songlist):
		if self.__mediaPlayer.playMusic(song, songlist):
			# Veritabanına Ekle
			self.__mainWindow.getDatabase().insertHistory(song["music_url"])
			# Müzik Barını Güncelle
			self.__musicControlBar.setSongName(song["music_name"])
			self.__musicControlBar.show()
			# Listeyi Güncelle
			self.__listbar.activeSong(song)

	def isPlaying(self):
		return self.__mediaPlayer.isPlaying()

	def pauseMusic(self):
		self.__mediaPlayer.pauseMusic()
		self.updateMusicControlBar()

	def stopMusic(self):
		self.__mediaPlayer.stopMusic()
		self.__listbar.stopSong()
		self.__musicControlBar.hide()

	def ignore_if_exiting(func):
		def wrapper(self, *args, **kwargs):
			if not self.__ignoreAllOnExit:
				return func(self, *args, **kwargs)
		return wrapper

	@ignore_if_exiting
	def prevMusic(self):
		self.__mediaPlayer.prevMusic()

	@ignore_if_exiting
	def nextMusic(self):
		self.__mediaPlayer.nextMusic()

	@ignore_if_exiting
	def moveMusicTo(self, time):
		self.__mediaPlayer.changeTime(self.__mediaPlayer.getCurrentDuration() + time)

	@ignore_if_exiting
	def toggleLike(self):
		self.__mainWindow.getDatabase().changeToggleLike(self.__mediaPlayer.getActiveSong()["music_url"])
		self.updateMusicControlBar()

	@ignore_if_exiting
	def toggleLoop(self):
		self.__mediaPlayer.toggleLoop()
		self.updateMusicControlBar()

	@ignore_if_exiting
	def toggleVolume(self):
		self.__mediaPlayer.setMuted(not self.__mediaPlayer.isMuted())
		self.updateMusicControlBar()

	@ignore_if_exiting
	def toggleShuffle(self):
		self.__mediaPlayer.toggleShuffle()
		self.updateMusicControlBar()

	@ignore_if_exiting
	def updateHeaderBar(self, text):
		self.__header.setLabel(text)

	@ignore_if_exiting
	def updateListBarWithSonglist(self, songlist, playlistName = ""):
		self.__listbar.updateList(songlist, playlistName)
		self.__listbar.activeSong(self.__mediaPlayer.getActiveSong())

	@ignore_if_exiting
	def updateListBarWithPlaylists(self, playlists):
		self.__listbar.updatePlaylist(playlists)

	@ignore_if_exiting
	def updateListBarWithArtistList(self, artistList):
		self.__listbar.updateArtistList(artistList)

	@ignore_if_exiting
	def updateMusicControlBar(self):
		currentTime = self.__mediaPlayer.getCurrentDuration()
		maxTime = self.__mediaPlayer.getAudioDuration()
		isPlay = self.__mediaPlayer.isPlaying()
		isLiked = self.__mainWindow.getDatabase().isLiked(self.__mediaPlayer.getActiveSong()["music_url"])
		isShuffle = self.__mediaPlayer.getShuffleStatus()
		loopValue = self.__mediaPlayer.getLoop()
		isMuted = self.__mediaPlayer.isMuted()
		self.__musicControlBar.update(currentTime, maxTime, isPlay, isLiked, isShuffle, loopValue, isMuted)

	@ignore_if_exiting
	def updateSideBar(self):
		pass

	@ignore_if_exiting
	def toScroll(self, widget: QWidget):
		self.__scroll_area2.ensureWidgetVisible(widget)

	def clickedItem(self, text: str):
		self.__header.setLabel(text)
		if text == "Tüm Şarkılar":
			# Sadece Dosya İsimlerine Göre ve Büyük Küçük Harf Bakmaksızın Sırala
			self.updateListBarWithSonglist(sorted(self.getAllLocalSong(), key=lambda song : song["music_name"].lower()))
		elif text == "Son Eklenen":
			# Son Değiştirilme Tarihine Göre Sırala
			self.updateListBarWithSonglist(sorted(self.getAllLocalSong(), key=lambda song : os.stat(QUrl(song["music_url"]).toLocalFile()).st_mtime, reverse=True))
		elif text == "Beğendiklerin":
			self.updateListBarWithSonglist(self.getLikedSong())
		elif text == "En Çok Dinlediklerin":
			self.updateListBarWithSonglist(self.getMostListenedSong())
		elif text == "Son Oynatılan":
			self.updateListBarWithSonglist(self.getRecentlyPlayedSong())
		elif text == "Sanatçılar":
			self.updateListBarWithArtistList(self.getAllLocalArtistName())
		elif text == "Oynatma Listeleri":
			self.updateListBarWithPlaylists(self.getAllPlaylist())
		elif text == "Çıkış Yap":
			self.__ignoreAllOnExit = True
			self.stopMusic()
			self.__mainWindow.logout()
			return
		self.__scroll_area2.verticalScrollBar().setValue(0)

	def addPlaylist(self, playlistName, music_url):
		self.__mainWindow.getDatabase().addPlaylist(playlistName, music_url)

	def deleteSongFromPlaylist(self, playlistName, music_url):
		self.__mainWindow.getDatabase().deleteSongFromPlaylist(playlistName, music_url)
		self.updateListBarWithSonglist(self.getPlaylistSong(playlistName), playlistName)
	
	def deletePlaylist(self, playlistName):
		self.__mainWindow.getDatabase().deletePlaylist(playlistName)
		self.updateListBarWithPlaylists(self.getAllPlaylist())

