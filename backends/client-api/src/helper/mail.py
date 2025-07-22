# ============================================================================
# File:    mail.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

import os
import smtplib

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime

from string import Template

from config import ERROR_LOG_PATH, RESET_PASSWORD_TEMPLATE_PATH, SUCCESS_SIGNUP_TEMPLATE_PATH, VERIFICATION_EMAIL_TEMPLATE_PATH

from dotenv import load_dotenv

load_dotenv()


class MailSender:
	def __init__(self):
		self.__e_mail = os.getenv("EMAIL")
		self.__password = os.getenv("PASSWORD")
		self.__display_name = os.getenv("DISPLAY_NAME")
		print(self.__e_mail)
		try:
			self.__connect()
		except:
			print(".env dosyasındaki bilgiler hatalı!")

	def __connect(self):
		self.__smtp = smtplib.SMTP(os.getenv("SMTP_HOST"), os.getenv("SMTP_PORT"))
		self.__smtp.ehlo()
		self.__smtp.starttls()
		self.__smtp.login(self.__e_mail, self.__password)

	def __del__(self):
		self.__smtp.close()

	def __send(self, to, subject, content, subtype):
		message = MIMEMultipart()
		message['From'] = f"{Header(self.__display_name, 'utf-8').encode()} <{self.__e_mail}>"
		message["Subject"] = subject
		message["To"] = to
		message.attach(MIMEText(content, subtype))
		self.__smtp.sendmail(message["From"], message["To"], message.as_string())

	def sendVerificationMail(self, mail: str, verification_code: str):
		try:
			template = self.__readTemplate(VERIFICATION_EMAIL_TEMPLATE_PATH)
			content = template.substitute(code=verification_code)
			self.__send(mail, "Mail Adresini Doğrula | <Marka İsmi>", content, "plain")
		except Exception as error:
			self.__log(error)

	def sendResetPassword(self, mail: str, verification_code: str):
		try:
			template = self.__readTemplate(RESET_PASSWORD_TEMPLATE_PATH)
			content = template.substitute(code=verification_code)
			self.__send(mail, "Şifreni Sıfırla | <Marka İsmi>", content, "plain")
		except Exception as error:
			self.__log(error)

	def sendSuccessSignUp(self, mail: str):
		try:
			template = self.__readTemplate(SUCCESS_SIGNUP_TEMPLATE_PATH)
			content = template.substitute()
			self.__send(mail, "Kayıt Başarılı | <Marka İsmi>", content, "plain")
		except Exception as error:
			self.__log(error)

	def __readTemplate(self, path: str) -> Template:
		with open(path, "r", encoding="utf-8") as file:
			return Template(file.read())

	def __log(self, log):
		with open(ERROR_LOG_PATH, "a+", encoding="utf-8") as file:
			file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} -> {str(log)}\n")
