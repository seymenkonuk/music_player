# ============================================================================
# File:    musicControlBar.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton
from PyQt5.QtCore import Qt

from helper.timeUtils import seconds_to_time

from config import PLAY_ICON_PATH, PAUSE_ICON_PATH, PREV_ICON_PATH, NEXT_ICON_PATH, BACKWARD_ICON_PATH, FORWARD_ICON_PATH
from config import LIKE_OFF_ICON_PATH, LIKE_ON_ICON_PATH, SHUFFLE_FALSE_ICON_PATH, SHUFFLE_TRUE_ICON_PATH, CLOSE_ICON_PATH
from config import LOOP0_ICON_PATH, LOOP1_ICON_PATH, LOOP2_ICON_PATH, VOLUME_OFF_ICON_PATH, VOLUME_ON_ICON_PATH

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from screen.music import MusicScreen


class MusicWidget(QFrame):
	def __init__(self, mainScreen: 'MusicScreen'):
		super().__init__()
		# 
		self.__mainScreen = mainScreen
		# 
		self.__ignore_slider_change = False
		# 
		self.__initUI()

	def __initUI(self):
		# 
		self.setObjectName("music_control_bar")
		self.setFixedHeight(100)
		self.setMinimumWidth(800)
		self.isVisible = False
		self.hide()
		# 
		self.__passingTime = QLabel()
		self.__remainingTime = QLabel()
		self.__slider = QSlider(Qt.Horizontal)
		self.__slider.setMinimum(0)
		self.__slider.setMaximum(100)
		self.__slider.setValue(0)
		self.__slider.setEnabled(False)
		self.__slider.valueChanged.connect(self.__slider_changed)
		self.__songName = QLabel()
		# Backward Button
		backwardButton = QPushButton()
		backwardButton.setIcon(QIcon(BACKWARD_ICON_PATH))
		backwardButton.setObjectName("transparent_button")
		backwardButton.clicked.connect(self.__backwardF)
		# Previous Button
		previousButton = QPushButton()
		previousButton.setIcon(QIcon(PREV_ICON_PATH))
		previousButton.setObjectName("transparent_button")
		previousButton.clicked.connect(self.__previousF)
		# Pause Button
		self.__pauseButton = QPushButton()
		self.__pauseButton.setIcon(QIcon(PAUSE_ICON_PATH))
		self.__pauseButton.setObjectName("transparent_button")
		self.__pauseButton.clicked.connect(self.__pauseF)
		# Next Button
		nextButton = QPushButton()
		nextButton.setIcon(QIcon(NEXT_ICON_PATH))
		nextButton.setObjectName("transparent_button")
		nextButton.clicked.connect(self.__nextF)
		# Forward Button
		forwardButton = QPushButton()
		forwardButton.setIcon(QIcon(FORWARD_ICON_PATH))
		forwardButton.setObjectName("transparent_button")
		forwardButton.clicked.connect(self.__forwardF)
		# Like Button
		self.__likeButton = QPushButton()
		self.__likeButton.setIcon(QIcon(LIKE_OFF_ICON_PATH))
		self.__likeButton.setObjectName("transparent_button")
		self.__likeButton.clicked.connect(self.__likeF)
		# Shuffle Button
		self.__shuffleButton = QPushButton()
		self.__shuffleButton.setIcon(QIcon(SHUFFLE_TRUE_ICON_PATH))
		self.__shuffleButton.setObjectName("transparent_button")
		self.__shuffleButton.clicked.connect(self.__shuffleF)
		# Loop Button
		self.__loopButton = QPushButton()
		self.__loopButton.setIcon(QIcon(LOOP0_ICON_PATH))
		self.__loopButton.setObjectName("transparent_button")
		self.__loopButton.clicked.connect(self.__loopF)
		# Volume Button
		self.__volumeButton = QPushButton()
		self.__volumeButton.setIcon(QIcon(VOLUME_ON_ICON_PATH))
		self.__volumeButton.setObjectName("transparent_button")
		self.__volumeButton.clicked.connect(self.__volumeF)
		# Close Button
		closeButton = QPushButton()
		closeButton.setIcon(QIcon(CLOSE_ICON_PATH))
		closeButton.setObjectName("transparent_button")
		closeButton.clicked.connect(self.__closeF)
		# Layout
		v_box = QVBoxLayout()
		h_box_up = QHBoxLayout()
		h_box_down = QHBoxLayout()
		h_box_down_left = QHBoxLayout()
		h_box_down_mid = QHBoxLayout()
		h_box_down_right = QHBoxLayout()

		h_box_up.setContentsMargins(0, 0, 0, 0)
		h_box_down.setContentsMargins(0, 0, 0, 0)
		h_box_down_left.setContentsMargins(0, 0, 0, 0)
		h_box_down_mid.setContentsMargins(0, 0, 0, 0)
		h_box_down_right.setContentsMargins(0, 0, 0, 0)

		v_box.setSpacing(10)
		h_box_up.setSpacing(10)
		h_box_down.setSpacing(0)
		h_box_down_left.setSpacing(10)
		h_box_down_mid.setSpacing(10)
		h_box_down_right.setSpacing(10)

		h_box_up.addWidget(self.__passingTime)
		h_box_up.addWidget(self.__slider)
		h_box_up.addWidget(self.__remainingTime)

		h_box_down_left.addWidget(self.__songName)
		h_box_down_left.addStretch()

		h_box_down_mid.addStretch()
		h_box_down_mid.addWidget(backwardButton)
		h_box_down_mid.addWidget(previousButton)
		h_box_down_mid.addWidget(self.__pauseButton)
		h_box_down_mid.addWidget(nextButton)
		h_box_down_mid.addWidget(forwardButton)
		h_box_down_mid.addStretch()

		h_box_down_right.addStretch()
		h_box_down_right.addWidget(self.__likeButton)
		h_box_down_right.addWidget(self.__shuffleButton)
		h_box_down_right.addWidget(self.__loopButton)
		h_box_down_right.addWidget(self.__volumeButton)
		h_box_down_right.addWidget(closeButton)

		h_box_down.addLayout(h_box_down_left)
		h_box_down.addLayout(h_box_down_mid)
		h_box_down.addLayout(h_box_down_right)

		v_box.addLayout(h_box_up)
		v_box.addLayout(h_box_down)

		self.setLayout(v_box)
	
	def setSongName(self, name: str):
		self.__songName.setText(name)

	def __backwardF(self):
		self.__mainScreen.moveMusicTo(-5)

	def __forwardF(self):
		self.__mainScreen.moveMusicTo(5)

	def __previousF(self):
		self.__mainScreen.prevMusic()

	def __nextF(self):
		self.__mainScreen.nextMusic()

	def __pauseF(self):
		self.__mainScreen.pauseMusic()

	def __likeF(self):
		self.__mainScreen.toggleLike()

	def __shuffleF(self):
		self.__mainScreen.toggleShuffle()

	def __loopF(self):
		self.__mainScreen.toggleLoop()

	def __volumeF(self):
		self.__mainScreen.toggleVolume()

	def __closeF(self):
		self.__mainScreen.stopMusic()

	def __slider_changed(self, value):
		if not self.__ignore_slider_change:
			pass
		self.__ignore_slider_change = False

	def update(self, currentTime, maxTime, isPlay, isLiked, isShuffle, loopValue, isMuted):
		remainingTime = maxTime - currentTime
		# 
		self.__passingTime.setText(seconds_to_time(currentTime))
		self.__remainingTime.setText(seconds_to_time(remainingTime))
		# 
		self.__slider.setMaximum(maxTime)
		if self.__slider.value() != currentTime:
			self.__slider.setValue(currentTime)
			self.__ignore_slider_change = True
		# 		
		self.__pauseButton.setIcon(QIcon(PAUSE_ICON_PATH if isPlay else PLAY_ICON_PATH))
		self.__likeButton.setIcon(QIcon(LIKE_ON_ICON_PATH if isLiked else LIKE_OFF_ICON_PATH))
		self.__shuffleButton.setIcon(QIcon(SHUFFLE_TRUE_ICON_PATH if isShuffle else SHUFFLE_FALSE_ICON_PATH))
		self.__loopButton.setIcon(QIcon([LOOP0_ICON_PATH, LOOP1_ICON_PATH, LOOP2_ICON_PATH][loopValue]))
		self.__volumeButton.setIcon(QIcon(VOLUME_OFF_ICON_PATH if isMuted else VOLUME_ON_ICON_PATH))
