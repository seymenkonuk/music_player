# ============================================================================
# File:    auth.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

import os
import requests

from config import SESSION_PATH, ENV_PATH

from dotenv import load_dotenv

load_dotenv(dotenv_path=ENV_PATH)

api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")


class Auth:
	def __init__(self):
		self.__resetAttributes()

	def __resetAttributes(self):
		self.__isLoggedIn = False
		self.__remember_me = False
		self.__token = None
		self.__email = None
		self.__name = None
		self.__surname = None
		self.__error_message = ""

	def __createSession(self, token: str):
		with open(SESSION_PATH, "w", encoding="utf-8") as file:
			file.write(token)

	def isLoggedIn(self):
		return self.__isLoggedIn
	
	def isRememberMeChecked(self):
		return self.__remember_me
	
	def getToken(self):
		return self.__token

	def getEmail(self):
		return self.__email

	def getName(self):
		return self.__name

	def getSurname(self):
		return self.__surname

	def getErrorMessage(self):
		return self.__error_message

	def login(self, email, password, remember_me):
		# API'ye istek at
		response = requests.post(api_base_url + "/auth/login", json={
			"email": email,
			"password": password,
			"remember_me": remember_me,
		})
		# Bilinmeyen Bir Hata
		if response.status_code != 200:
			self.__error_message = "Bilinmeyen bir hata oluştu"
			return False
		# Cevap Olumsuz Gelirse
		response = response.json()
		if not response["success"]:
			self.__error_message = response["message"]
			return False
		# Cevabı Kaydet
		self.__isLoggedIn = True
		self.__remember_me = remember_me
		self.__token = response["data"]["token"]
		self.__email = response["data"]["email"]
		self.__name = response["data"]["name"]
		self.__surname = response["data"]["surname"]
		self.__error_message = ""
		# Beni Hatırla İşaretlendiyse Oturumu Kaydet
		if remember_me:
			self.__createSession(self.getToken())
		# İstek Başarılı
		return True

	def logout(self):
		requests.post(api_base_url + "/auth/logout", json={
			"token": self.__token,
		})
		self.__resetAttributes()

	def loginWithToken(self, token):
		# API'ye istek at
		response = requests.post(api_base_url + "/auth/check-token", json={
			"token": token,
		})
		# Bilinmeyen Bir Hata
		if response.status_code != 200:
			self.__error_message = "Bilinmeyen bir hata oluştu"
			return False
		# Cevap Olumsuz Gelirse
		response = response.json()
		if not response["success"]:
			self.__error_message = response["message"]
			return False
		# Cevabı Kaydet
		self.__isLoggedIn = True
		self.__remember_me = True
		self.__token = response["data"]["token"]
		self.__email = response["data"]["email"]
		self.__name = response["data"]["name"]
		self.__surname = response["data"]["surname"]
		self.__error_message = ""
		# İstek Başarılı
		return True

	def signup(self, email, password, name, surname):
		# API'ye istek at
		response = requests.post(api_base_url + "/auth/signup", json={
			"email": email,
			"password": password,
			"name": name,
			"surname": surname,
		})
		# Bilinmeyen Bir Hata
		if response.status_code != 200:
			self.__error_message = "Bilinmeyen bir hata oluştu"
			return False
		# Cevap Olumsuz Gelirse
		response = response.json()
		if not response["success"]:
			self.__error_message = response["message"]
			return False
		# İstek Başarılı
		return True

	def emailVerify(self, email, code):
		# API'ye istek at
		response = requests.post(api_base_url + "/auth/verify-email", json={
			"email": email,
			"code": code,
		})
		# Bilinmeyen Bir Hata
		if response.status_code != 200:
			self.__error_message = "Bilinmeyen bir hata oluştu"
			return False
		# Cevap Olumsuz Gelirse
		response = response.json()
		if not response["success"]:
			self.__error_message = response["message"]
			return False
		# İstek Başarılı
		return True
	
	def resetPasswordRequest(self, email):
		# API'ye istek at
		response = requests.post(api_base_url + "/auth/reset-password-request", json={
			"email": email,
		})
		# Bilinmeyen Bir Hata
		if response.status_code != 200:
			self.__error_message = "Bilinmeyen bir hata oluştu"
			return False
		# Cevap Olumsuz Gelirse
		response = response.json()
		if not response["success"]:
			self.__error_message = response["message"]
			return False
		# İstek Başarılı
		return True
	
	def resetPasswordVerify(self, email, code):
		# API'ye istek at
		response = requests.post(api_base_url + "/auth/reset-password-verify", json={
			"email": email,
			"code": code,
		})
		# Bilinmeyen Bir Hata
		if response.status_code != 200:
			self.__error_message = "Bilinmeyen bir hata oluştu"
			return False
		# Cevap Olumsuz Gelirse
		response = response.json()
		if not response["success"]:
			self.__error_message = response["message"]
			return False
		# İstek Başarılı
		return True
	
	def resetPassword(self, email, code, new_password):
		# API'ye istek at
		response = requests.post(api_base_url + "/auth/reset-password", json={
			"email": email,
			"code": code,
			"new_password": new_password,
		})
		# Bilinmeyen Bir Hata
		if response.status_code != 200:
			self.__error_message = "Bilinmeyen bir hata oluştu"
			return False
		# Cevap Olumsuz Gelirse
		response = response.json()
		if not response["success"]:
			self.__error_message = response["message"]
			return False
		# İstek Başarılı
		return True
