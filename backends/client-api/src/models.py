# ============================================================================
# File:    models.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

import re

from pydantic import BaseModel


class LoginData(BaseModel):
    email: str
    password: str
    remember_me: bool

class LoginWithTokenData(BaseModel):
    token: str

class LogoutData(BaseModel):
    token: str

class SignupData(BaseModel):
    email: str
    password: str
    name: str
    surname: str

class EmailVerifyData(BaseModel):
    email: str
    code: str

class ResetPasswordRequestData(BaseModel):
    email: str

class ResetPasswordVerifyData(BaseModel):
    email: str
    code: str

class ResetPasswordData(BaseModel):
    email: str
    code: str
    new_password: str

def validateLoginData(data: LoginData):
    # Email 
    if len(data.email) < 5:
        return "Email adresi 5 karakterden kısa olamaz!"
    # Email Format
    if not isValidEmail(data.email):
        return "Geçersiz email adresi!"
    # Password 
    if len(data.password) < 5:
        return "Parola alanı 5 karakterden kısa olamaz!"
    return ""

def validateLoginWithTokenData(data: LoginWithTokenData):
    # Token
    if len(data.token) != 64:
        return "Token alanı 64 karakter olmalıdır!"
    return ""

def validateLogoutData(data: LogoutData):
    # Token
    if len(data.token) != 64:
        return "Token alanı 64 karakter olmalıdır!"
    return ""

def validateSignupData(data: SignupData):
    # Email 
    if len(data.email) < 5:
        return "Email adresi 5 karakterden kısa olamaz!"
    # Email Format
    if not isValidEmail(data.email):
        return "Geçersiz email adresi!"
    # Name
    if len(data.name) < 2:
        return "İsim alanı 2 karakterden kısa olamaz!"
    # Surname 
    if len(data.surname) < 2:
        return "Soyisim alanı 2 karakterden kısa olamaz!"
    # Password
    if len(data.password) < 5:
        return "Parola alanı 5 karakterden kısa olamaz!"
    return ""

def validateEmailVerifyData(data: EmailVerifyData):
    # Email 
    if len(data.email) < 5:
        return "Email adresi 5 karakterden kısa olamaz!"
    # Email Format
    if not isValidEmail(data.email):
        return "Geçersiz email adresi!"
    # Code
    if len(data.code) != 19:
        return "Geçersiz kod!"
    return ""

def validateResetPasswordRequestData(data : ResetPasswordRequestData):
    # Email 
    if len(data.email) < 5:
        return "Email adresi 5 karakterden kısa olamaz!"
    # Email Format
    if not isValidEmail(data.email):
        return "Geçersiz email adresi!"
    return ""

def validateResetPasswordVerifyData(data: ResetPasswordVerifyData):
    # Email 
    if len(data.email) < 5:
        return "Email adresi 5 karakterden kısa olamaz!"
    # Email Format
    if not isValidEmail(data.email):
        return "Geçersiz email adresi!"
    # Code
    if len(data.code) != 19:
        return "Geçersiz kod!"
    return ""

def validateResetPasswordData(data: ResetPasswordData):
    # Email 
    if len(data.email) < 5:
        return "Email adresi 5 karakterden kısa olamaz!"
    # Email Format
    if not isValidEmail(data.email):
        return "Geçersiz email adresi!"
    # Code
    if len(data.code) != 19:
        return "Geçersiz kod!"
    # Password 
    if len(data.new_password) < 5:
        return "Parola alanı 5 karakterden kısa olamaz!"
    return ""

def isValidEmail(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None
