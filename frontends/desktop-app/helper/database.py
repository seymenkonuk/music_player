# ============================================================================
# File:    database.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

import sqlite3

from helper.filename import pathToSong

from config import APP_DATA_PATH

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from helper.auth import Auth


class DatabaseControl:
	def __init__(self, auth: 'Auth'):
		self.__auth = auth
		# Bağlantıyı Oluştur
		self.__connect = sqlite3.connect(APP_DATA_PATH)
		self.__cursor = self.__connect.cursor()
		# Verileri Dizi Halinde Değil, Sözlük Halinde Döndürür
		self.__cursor.row_factory = sqlite3.Row
		# 
		self.__createTables()

	def __del__(self):
		self.__connect.close()

	def __createTables(self):
		self.__createPlaylistTable()
		self.__createPlaylistContentTable()
		self.__createLikedSongTable()
		self.__createHistoryTable()

	def __createPlaylistTable(self):
		self.__cursor.execute("""
		CREATE TABLE IF NOT EXISTS playlist (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			owner_email VARCHAR(255) NOT NULL DEFAULT '',
			name VARCHAR(255) NOT NULL,
			created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
			UNIQUE (owner_email, name)
		);
		""")
		self.__connect.commit()

	def __createPlaylistContentTable(self):
		self.__cursor.execute("""
		CREATE TABLE IF NOT EXISTS playlist_content (
			playlist_id INTEGER NOT NULL,
			music_url VARCHAR(255) NOT NULL,
			created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (playlist_id, music_url),
			FOREIGN KEY (playlist_id) REFERENCES playlist(id) ON DELETE CASCADE
		);
		""")
		self.__connect.commit()


	# Beğenilen Müzikleri Kaydeder
	def __createLikedSongTable(self):
		self.__cursor.execute("""
		CREATE TABLE IF NOT EXISTS liked_song (
			owner_email VARCHAR(255) NOT NULL DEFAULT '',
			music_url VARCHAR(255) NOT NULL,
			created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (owner_email, music_url)
		);
		""")
		self.__connect.commit()

	# Dinlenen Müzikleri ve Ne Zaman Dinlendiklerini Kaydeder
	def __createHistoryTable(self):
		self.__cursor.execute("""
		CREATE TABLE IF NOT EXISTS history (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			owner_email VARCHAR(255) NOT NULL DEFAULT '',
			music_url VARCHAR(255) NOT NULL,
			created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
		);
		""")
		self.__connect.commit()

	# PUBLIC METOTLAR
	# Beğenilen Şarkılara Bir Şarkı Ekle
	def __insertLikedSong(self, music_url):
		self.__cursor.execute(
			"INSERT INTO liked_song (owner_email, music_url) VALUES (?, ?)", 
			(self.__auth.getEmail() or "", music_url)
		)
		self.__connect.commit()

	# Son Oynatılan Şarkılara Bir Şarkı Ekle
	def insertHistory(self, music_url):
		self.__cursor.execute(
			"INSERT INTO history (owner_email, music_url) VALUES (?, ?)", 
			(self.__auth.getEmail() or "", music_url)
		)
		self.__connect.commit()

	# Yoksa Oynatma Listesi Oluştur
	def createPlaylist(self, playlistName):
		if self.__isPlaylistExists(playlistName):
			return False
		self.__cursor.execute(
			"INSERT INTO playlist (owner_email, name) VALUES (?, ?)", 
			(self.__auth.getEmail() or "", playlistName)
		)
		self.__connect.commit()
		return True

	# Şarkıyı Oynatma Listesine Ekle
	def addPlaylist(self, playlistName, music_url):
		# Yoksa Oluştur
		self.createPlaylist(playlistName)
		# Zaten Şarkı Eklendi
		if self.__isPlaylistSongExists(playlistName, music_url):
			return
		# Playlist ID'sini Al
		playlist_id = self.__getPlaylistId(playlistName)
		# Şarkıyı Ekle
		self.__cursor.execute(
			"INSERT INTO playlist_content (playlist_id, music_url) VALUES (?, ?)", 
			(playlist_id, music_url)
		)
		self.__connect.commit()

	# Beğenilen Şarkılardan Bir Şarkı Çıkart
	def __deleteLikedSong(self, music_url):
		self.__cursor.execute(
			"DELETE FROM liked_song WHERE owner_email = ? and music_url = ?", 
			(self.__auth.getEmail() or "", music_url)
		)
		self.__connect.commit()

	# Son Oynatılan Şarkılardan Bir Şarkı Çıkart
	def deleteHistory(self, music_url):
		self.__cursor.execute(
			"DELETE FROM history WHERE owner_email = ? and music_url = ?", 
			(self.__auth.getEmail() or "", music_url)
		)
		self.__connect.commit()

	# Oynatma Listesinin Tamamını Sil
	def deletePlaylist(self, playlistName):
		self.__cursor.execute(
			"DELETE FROM playlist WHERE owner_email = ? and name = ?", 
			(self.__auth.getEmail() or "", playlistName)
		)
		self.__connect.commit()

	# Oynatma Listesinden Bir Şarkıyı Sil
	def deleteSongFromPlaylist(self, playlistName, music_url):
		self.__cursor.execute(
			"DELETE FROM playlist_content WHERE playlist_id = (SELECT id FROM playlist WHERE owner_email = ? and name = ?) and music_url = ?", 
			(self.__auth.getEmail() or "", playlistName, music_url)
		)
		self.__connect.commit()

	# Tüm Beğenilen Şarkıları Göster
	def readLikedSong(self):
		self.__cursor.execute(
			"SELECT music_url FROM liked_song WHERE owner_email = ? ORDER BY created_at DESC", 
			(self.__auth.getEmail() or "", )
		)
		for song in self.__cursor:
			yield pathToSong(dict(song)["music_url"])

	# Geçmişteki Şarkıları Benzersizleri Göster
	def readHistoryDistinct(self):
		self.__cursor.execute(
			"SELECT music_url, MAX(created_at) as newdate FROM history WHERE owner_email = ? GROUP BY music_url ORDER BY newdate DESC",
			(self.__auth.getEmail() or "", )
		)
		for song in self.__cursor:
			yield pathToSong(dict(song)["music_url"])

	# En Çok Dinlenen Şarkıları Göster
	def readMostListenedSong(self):
		self.__cursor.execute(
			"SELECT music_url, COUNT(*) as number FROM history WHERE owner_email = ? GROUP BY music_url ORDER BY number DESC",
			(self.__auth.getEmail() or "", )
		)
		for song in self.__cursor:
			yield pathToSong(dict(song)["music_url"])

	# Tüm Oynatma Listelerini Göster
	def readAllPlaylist(self):
		self.__cursor.execute(
			"SELECT name FROM playlist WHERE owner_email = ? ORDER BY name ASC", 
			(self.__auth.getEmail() or "", )
		)
		for playlist in self.__cursor:
			yield playlist["name"]

	# Oynatma Listesinde Bulunan Şarkıları Göster
	def readPlaylistSong(self, playlistName):
		self.__cursor.execute(
			"SELECT music_url FROM playlist_content WHERE playlist_id = (SELECT id FROM playlist WHERE owner_email = ? and name = ? LIMIT 1)", 
			(self.__auth.getEmail() or "", playlistName)
		)
		for song in self.__cursor:
			yield pathToSong(dict(song)["music_url"])

	# Oynatma Listesinin Id'sini Bul
	def __getPlaylistId(self, playlistName):
		self.__cursor.execute(
			"SELECT id FROM playlist WHERE owner_email = ? and name = ?", 
			(self.__auth.getEmail() or "", playlistName)
		)
		row = self.__cursor.fetchone()
		return row["id"]

	# O Şarkı Zaten Beğenildi Mi
	def isLiked(self, music_url):
		self.__cursor.execute(
			"SELECT COUNT(*) as like_count FROM liked_song WHERE owner_email = ? and music_url = ?", 
			(self.__auth.getEmail() or "", music_url)
		)
		row = self.__cursor.fetchone()
		return row["like_count"] != 0

	# Bu İsimde Oynatma Listesi Var Mı
	def __isPlaylistExists(self, playlistName):
		self.__cursor.execute(
			"SELECT COUNT(*) as playlist_count FROM playlist WHERE owner_email = ? and name = ?", 
			(self.__auth.getEmail() or "", playlistName)
		)
		row = self.__cursor.fetchone()
		return row["playlist_count"] != 0

	# Bu Şarkı Zaten Oynatma Listesinde Mevcut Mu?
	def __isPlaylistSongExists(self, playlistName, music_url):
		if not self.__isPlaylistExists(playlistName):
			return False
		playlist_id = self.__getPlaylistId(playlistName)
		#
		self.__cursor.execute(
			"SELECT COUNT(*) as song_count FROM playlist_content WHERE playlist_id = ? and music_url = ?", 
			(playlist_id, music_url)
		)
		row = self.__cursor.fetchone()
		return row["song_count"] != 0

	# Beğen Butonuna Tıklandığında
	def changeToggleLike(self, music_url):
		if self.isLiked(music_url):
			self.__deleteLikedSong(music_url)
		else:
			self.__insertLikedSong(music_url)
