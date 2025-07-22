# ============================================================================
# File:    playMusic.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

import random

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from screen.music import MusicScreen


class MusicPlayer(QMediaPlayer):
	# statik değişkenler
	noLoop = 0
	singleLoop = 1
	listLoop = 2

	def __init__(self, mainScreen: 'MusicScreen'):
		super().__init__()
		# 
		self.__mainScreen = mainScreen
		# 
		self.__activeSongList = []
		self.__activeSong = {"music_name": "", "music_url": "", "artist_name": ""}
		# 
		self.__loop = MusicPlayer.noLoop
		self.__isShuffle = False
		# 
		self.__ignore_state_change = False
		# 
		self.stateChanged.connect(self.__mediaStateChanged)
		self.positionChanged.connect(self.__mediaPositionChanged)

	def getActiveList(self):
		return self.__activeSongList
	
	def getActiveSong(self):
		return self.__activeSong

	def getLoop(self):
		return self.__loop
	
	def getShuffleStatus(self):
		return self.__isShuffle
	
	def toggleLoop(self):
		self.__loop = (self.__loop + 1) % 3

	def toggleShuffle(self):
		self.__isShuffle = not self.__isShuffle
	
	def ignore_state_change(func):
		def wrapper(self, *args, **kwargs):
			def end_ignore_state_change():
				self.__ignore_state_change = False
			self.__ignore_state_change = True
			QTimer.singleShot(1000, end_ignore_state_change)
			return func(self, *args, **kwargs)
		return wrapper

	@ignore_state_change
	def playMusic(self, song, songlist):
		if song in songlist:
			# Değişkenleri Güncelle
			self.__activeSong = song
			self.__activeSongList = songlist
			# Müziği Çal
			self.setMedia(QMediaContent(QUrl(song["music_url"])))
			self.play()
			return True
		return False
	
	@ignore_state_change
	def changeTime(self, time):
		if time < 0:
			time = 0
		if time > self.getAudioDuration():
			time = self.getAudioDuration() - 1
		self.setPosition(time * 1000)

	@ignore_state_change
	def pauseMusic(self):
		if self.isPlaying():
			self.pause()
			return False
		else:
			self.play()
			return True

	@ignore_state_change
	def stopMusic(self):
		self.__activeSong = {"music_name": "", "music_url": "", "artist_name": ""}
		self.stop()

	def isPlaying(self):
		return self.state() == QMediaPlayer.PlayingState

	def getAudioDuration(self):
		return self.duration() // 1000

	def getCurrentDuration(self):
		return self.position() // 1000

	def nextMusic(self):
		if self.__activeSong in self.__activeSongList:
			current_index = self.__activeSongList.index(self.__activeSong) + 1

			# Shuffle Aktif ise Listeyi Karıştır
			if self.getShuffleStatus():
				current_index = random.randint(0, len(self.__activeSongList) - 1)
			
			# Şarkı Kalmadıysa
			if current_index >= len(self.__activeSongList):
				# Döngü Kapalıysa Bitir
				if self.getLoop() == MusicPlayer.noLoop:
					self.__mainScreen.stopMusic()
					return
				# Döngü Açıksa Başa Dön
				else:
					current_index = 0

			self.__mainScreen.playMusic(self.__activeSongList[current_index], self.__activeSongList)

	def prevMusic(self):
		if self.__activeSong in self.__activeSongList:
			current_index = self.__activeSongList.index(self.__activeSong) - 1

			# Shuffle Aktif ise Listeyi Karıştır
			if self.getShuffleStatus():
				current_index = random.randint(0, len(self.__activeSongList) - 1)
			
			# Şarkı Kalmadıysa
			if current_index < 0:
				# Döngü Kapalıysa Bitir
				if self.getLoop() == MusicPlayer.noLoop:
					self.__mainScreen.stopMusic()
					return
				# Döngü Açıksa En Sona Git
				else:
					current_index = len(self.__activeSongList) - 1

			self.__mainScreen.playMusic(self.__activeSongList[current_index], self.__activeSongList)

	# Müzik Bittiğinde Yeni Müzik
	def __mediaStateChanged(self, state):
		# şarkı bittiyse
		if state == QMediaPlayer.StoppedState and not self.__ignore_state_change:
			if self.getLoop() == MusicPlayer.singleLoop:
				self.__mainScreen.playMusic(self.__activeSong, self.__activeSongList)
			else:
				self.__mainScreen.nextMusic()
		# ignore'u kaldır
		if self.__ignore_state_change:
			self.__ignore_state_change = False

	def __mediaPositionChanged(self, _position):
		self.__mainScreen.updateMusicControlBar()
