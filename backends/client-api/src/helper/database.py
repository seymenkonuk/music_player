# ============================================================================
# File:    database.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

import hashlib
import sqlite3

from config import DATABASE_PATH

from helper.createCode import createCode, createFormattedCode


class DatabaseControl:
	def __init__(self):
		# Bağlantıyı Oluştur
		self.__connect = sqlite3.connect(DATABASE_PATH)
		self.__cursor = self.__connect.cursor()
		# Verileri Dizi Halinde Değil, Sözlük Halinde Döndürür
		self.__cursor.row_factory = sqlite3.Row
		# 
		self.__createTables()

	def __del__(self):
		self.__connect.close()

	def __createTables(self):
		self.__createUsersTable()
		self.__createSessionTable()

	def __createUsersTable(self):
		self.__cursor.execute("""
		CREATE TABLE IF NOT EXISTS user (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			email VARCHAR(255) NOT NULL, 
			password VARCHAR(255) NOT NULL, 
			name VARCHAR(255) NOT NULL, 
			surname VARCHAR(255) NOT NULL, 
			created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
			verification_code VARCHAR(255) NOT NULL,
			is_verify INT NOT NULL DEFAULT 0,
			reset_password_code VARCHAR(255) DEFAULT NULL, 
			reset_password_time TIMESTAMP DEFAULT NULL,
			UNIQUE (email)
		);
		""")
		self.__connect.commit()

	def __createSessionTable(self):
		self.__cursor.execute("""
		CREATE TABLE IF NOT EXISTS session (
			token VARCHAR(255) NOT NULL,
			user_id VARCHAR(255) NOT NULL,
			created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
			expires_at TIMESTAMP,
			PRIMARY KEY (token),
			FOREIGN KEY (user_id) REFERENCES user(id)
		);
		""")
		self.__connect.commit()

	# PUBLIC METOTLAR
	# Kullanıcı Oluştur
	def createUser(self, email: str, password: str, name: str, surname: str):
		if self.isEmailTaken(email):
			return
		verification_code = createFormattedCode(4, 4)
		self.__cursor.execute(
			"INSERT INTO user (email, password, name, surname, verification_code) VALUES (?, ?, ?, ?, ?)", 
			(email, DatabaseControl.hashPassword(password), name, surname, verification_code)
		)
		self.__connect.commit()
		last_id = self.__cursor.lastrowid
		return last_id, verification_code

	# Oturum Oluştur
	def createSession(self, email: str, remember_me: bool):
		id = self.__getUserId(email)
		if id is None:
			return
		token = createCode(64)
		if remember_me:
			self.__cursor.execute(
				"INSERT INTO session (token, user_id) VALUES (?, ?)", 
				(token, id)
			)
		else:
			self.__cursor.execute(
				"INSERT INTO session (token, user_id, expires_at) VALUES (?, ?, datetime('now', '+1 day'))", 
				(token, id)
			)
		self.__connect.commit()
		return token

	# Kullanıcının Id'sini Al
	def __getUserId(self, email: str):
		self.__cursor.execute(
			"SELECT id FROM user WHERE email = ?", 
			(email,)
		)
		row = self.__cursor.fetchone()
		if row is None:
			return None
		return row["id"]

	# Email Mevcut Mu
	def isEmailTaken(self, email: str):
		self.__deleteExpiredUser()
		# 
		self.__cursor.execute(
			"SELECT COUNT(*) as user_count FROM user WHERE email = ?", 
			(email,)
		)
		row = self.__cursor.fetchone()
		return row["user_count"] != 0

	# Email Doğrulandı Mı
	def isVerifiedEmail(self, email: str):
		self.__cursor.execute(
			"SELECT COUNT(*) as user_count FROM user WHERE email = ? and is_verify = 1", 
			(email,)
		)
		row = self.__cursor.fetchone()
		return row["user_count"] != 0

	# Oturum Geçerli Mi
	def isSessionValid(self, token: str):
		self.__cursor.execute(
			"SELECT COUNT(*) as token_count FROM session WHERE token = ? and (expires_at is NULL or expires_at > datetime('now'))", 
			(token,)
		)
		row = self.__cursor.fetchone()
		return row["token_count"] != 0

	# Kullanıcı Bilgilerini Getir
	def getUserInfo(self, email: str):
		self.__cursor.execute(
			"SELECT email, name, surname, created_at, is_verify FROM user WHERE email = ?", 
			(email,)
		)
		row = self.__cursor.fetchone()
		return row

	# Kullanıcı Bilgilerini Getir
	def __getUserInfoById(self, userId: int):
		self.__cursor.execute(
			"SELECT email, name, surname, created_at, is_verify FROM user WHERE id = ?", 
			(userId,)
		)
		row = self.__cursor.fetchone()
		return row

	# Kullanıcı Bilgilerini Getir
	def getUserInfoByToken(self, token: str):
		self.__cursor.execute(
			"SELECT user_id FROM session WHERE token = ?", 
			(token,)
		)
		row = self.__cursor.fetchone()
		if row is None:
			return None
		return self.__getUserInfoById(row["user_id"])

	# Kullanıcının Parolasının Hash'ini Getir
	def getPasswordHash(self, email: str):
		self.__cursor.execute(
			"SELECT password FROM user WHERE email = ?", 
			(email,)
		)
		row = self.__cursor.fetchone()
		if row is None:
			return None
		return row["password"]

	# Kullanıcının Doğrulama Kodunu Doğrula
	def verifyEmail(self, email: str, verification_code: str):
		self.__cursor.execute(
			"UPDATE user SET is_verify = 1 WHERE email = ? and is_verify = 0 and verification_code is not NULL and verification_code = ? and created_at > datetime('now', '-3 minutes')",
			(email, verification_code)
		)
		self.__connect.commit()
		# Hatalı Kod
		if self.__cursor.rowcount == 0:
			self.__deleteUser(email)
			return False
		return True

	# Kod oluşturur
	def resetPasswordRequest(self, email: str):
		# Kullanıcı Yoksa Bir Şey Yapma
		if not self.isEmailTaken(email):
			return
		# Doğrulanmamış Hesap
		if not self.isVerifiedEmail(email):
			return
		code = createFormattedCode(4, 4)
		self.__cursor.execute(
			"UPDATE user SET reset_password_code = ?, reset_password_time = datetime('now') WHERE email = ? and is_verify = 1",
			(code, email)
		)
		self.__connect.commit()
		return code

	# Kullanıcının Parola Sıfırlama Kodunu Doğrula
	def verifyResetPassword(self, email: str, reset_password_code: str):
		# Kullanıcı Yoksa Bir Şey Yapma
		if not self.isEmailTaken(email):
			return False
		# Doğrulanmamış Hesap
		if not self.isVerifiedEmail(email):
			return False
		# Parola Sıfırlama Kodunu Getir
		self.__cursor.execute(
			"SELECT reset_password_code FROM user WHERE email = ? and reset_password_time > datetime('now', '-5 minutes')", 
			(email,)
		)
		row = self.__cursor.fetchone()
		# Hatalı Kod
		if row is None or not row["reset_password_code"] == reset_password_code:
			self.__revokeResetPasswordCode(email)
			return False
		return True

	# Parolayı Değiştir
	def changePassword(self, email: str, new_password: str):
		self.__cursor.execute(
			"UPDATE user SET password = ?, reset_password_code = NULL, reset_password_time = NULL WHERE email = ?",
			(DatabaseControl.hashPassword(new_password), email)
		)
		self.__connect.commit()
		return True

	# Oturumu Sonlandır
	def deleteSession(self, token: str):
		self.__cursor.execute(
			"DELETE FROM session WHERE token = ?", 
			(token,)
		)
		self.__connect.commit()

	def __revokeResetPasswordCode(self, email):
		self.__cursor.execute("UPDATE user SET reset_password_code = 'NULL' and reset_password_time = 'NULL' WHERE email = ?", (email,))
		self.__connect.commit()

	def __deleteUser(self, email):
		self.__cursor.execute("DELETE FROM user WHERE email = ?", (email,))
		self.__connect.commit()

	# Zamanında Doğrulanmamış Kullanıcıları Sil
	def __deleteExpiredUser(self):
		self.__cursor.execute("DELETE FROM user WHERE created_at <= datetime('now', '-3 minutes') and is_verify = 0")
		self.__connect.commit()

	@staticmethod
	def hashPassword(password):
		return hashlib.sha256(password.encode()).hexdigest()
