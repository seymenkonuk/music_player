# ============================================================================
# File:    findMusic.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

import os

from PyQt5.QtCore import QUrl

from helper.filename import pathToSong, pathToFileExtension

from config import ENV_PATH

from dotenv import load_dotenv

load_dotenv(dotenv_path=ENV_PATH)

musicPath = os.getenv("MUSIC_ROOT_PATH", os.path.abspath(os.sep))
fileExtensions = os.getenv("MUSIC_FILE_EXTENSIONS", ".mp3").split(";")

def getMusicFiles():
	# Yoksa Dizini Oluştur
	if not os.path.exists(musicPath):
		os.makedirs(musicPath)
	result = []
	# İlgili Dizindeki Tüm Müzik Dosyalarını Bul ve Geriye Döndür
	for root, _dirs, files in os.walk(musicPath):
		for file in files:
			if pathToFileExtension(file) in fileExtensions:
				result.append(pathToSong(QUrl.fromLocalFile(root + os.sep + file).toString()))
	return result
