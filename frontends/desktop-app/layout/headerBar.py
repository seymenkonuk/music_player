# ============================================================================
# File:    headerBar.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

import random

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton

from config import PLAY_ICON_PATH, SHUFFLE_ICON_PATH

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from screen.music import MusicScreen


class HeaderWidget(QFrame):
	def __init__(self, mainScreen: 'MusicScreen'):
		super().__init__()
		# 
		self.__mainScreen = mainScreen
		# 
		self.__initUI()

	def __initUI(self):
		self.setObjectName("headerbar")
		# Label
		self.__label = QLabel()
		# Play List Button
		playButton = QPushButton()
		playButton.setIcon(QIcon(PLAY_ICON_PATH))
		playButton.setObjectName("transparent_button")
		playButton.clicked.connect(self.__play)
		# Shuffle Button
		shuffleButton = QPushButton()
		shuffleButton.setIcon(QIcon(SHUFFLE_ICON_PATH))
		shuffleButton.setObjectName("transparent_button")
		shuffleButton.clicked.connect(self.__shuffle)
		# Layout
		h_box = QHBoxLayout()
		h_box.addWidget(self.__label)
		h_box.addStretch()
		h_box.addWidget(playButton)
		h_box.addWidget(shuffleButton)
		self.setLayout(h_box)

	def setLabel(self, text):
		self.__label.setText(text)

	def __play(self):
		viewedList = self.__mainScreen.getViewedList()
		if len(viewedList) > 0:
			self.__mainScreen.playMusic(viewedList[0], viewedList)

	def __shuffle(self):
		viewedList = self.__mainScreen.getViewedList()
		random.shuffle(viewedList)
		self.__mainScreen.updateListBarWithSonglist(viewedList)
		self.__play()
