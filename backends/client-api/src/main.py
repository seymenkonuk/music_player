# ============================================================================
# File:    main.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

from fastapi import FastAPI

from helper.database import DatabaseControl
from helper.mail import MailSender

from models import *

app = FastAPI()

# 
@app.post("/auth/login")
def login(request: LoginData):
    database = DatabaseControl()
    # Request Validation!!
    error = validateLoginData(request)
    if error != "":
        return failMessage(error)
    # Kullanıcı Bulunamadı!
    if not database.isEmailTaken(request.email):
        return failMessage("Kullanıcı adı veya parola hatalı!")
    # Parola Hatalı!
    if not DatabaseControl.hashPassword(request.password) == database.getPasswordHash(request.email):
        return failMessage("Kullanıcı adı veya parola hatalı!")
    # Oturum Oluştur
    token = database.createSession(request.email, request.remember_me)
    # Sonucu Döndür
    return successMessage(
        "Giriş başarılı!", 
        {
            "token": token,
            **database.getUserInfo(request.email),
        }
    )

# 
@app.post("/auth/check-token")
def checkToken(request: LoginWithTokenData):
    database = DatabaseControl()
    # Request Validation!!
    error = validateLoginWithTokenData(request)
    if error != "":
        return failMessage(error)
    # Oturum Bulunamadı!
    if not database.isSessionValid(request.token):
        return failMessage("Geçersiz oturum!")
    # Sonucu Döndür
    return successMessage(
        "Giriş başarılı!",
        {
            "token": request.token,
            **database.getUserInfoByToken(request.token),
        }
    )

# 
@app.post("/auth/logout")
def logout(request: LogoutData):
    database = DatabaseControl()
    # Request Validation!!
    error = validateLogoutData(request)
    if error != "":
        return failMessage(error)
    # Oturum Bulunamadı!
    if not database.isSessionValid(request.token):
        return failMessage("Geçersiz oturum!")
    # Çıkış İşlemini Yap
    database.deleteSession(request.token)
    # Sonucu Döndür
    return successMessage("Çıkış başarılı!")

# 
@app.post("/auth/signup")
def signup(request: SignupData):
    database = DatabaseControl()
    mailSender = MailSender()
    # Request Validation!!
    error = validateSignupData(request)
    if error != "":
        return failMessage(error)
    # Kullanıcı Zaten Kayıtlı!
    if database.isEmailTaken(request.email):
        return failMessage("Email zaten kullanılıyor!")
    # Kullanıcı Oluştur
    _id, verification_code = database.createUser(request.email, request.password, request.name, request.surname)
    # Mail Gönder
    mailSender.sendVerificationMail(request.email, verification_code)
    # Sonucu Döndür
    return successMessage("Kayıt başarılı!")

# 
@app.post("/auth/verify-email")
def verifyEmail(request: EmailVerifyData):
    database = DatabaseControl()
    mailSender = MailSender()
    # Request Validation!!
    error = validateEmailVerifyData(request)
    if error != "":
        return failMessage(error)
    # Kullanıcı Bulunamadı!
    if not database.isEmailTaken(request.email):
        return failMessage("Kullanıcı bulunamadı!")
    # Zaten Doğrulanmış Hesap
    if database.isVerifiedEmail(request.email):
        return failMessage("Bu hesap daha önce zaten doğrulandı!")
    # Doğrulama Kodu Hatalı
    if not database.verifyEmail(request.email, request.code):
        return failMessage("Doğrulama kodu hatalı!")
    # Mail Gönder
    mailSender.sendSuccessSignUp(request.email)
    # Sonucu Döndür
    return successMessage("Email doğrulama başarılı!")

# 
@app.post("/auth/reset-password-request")
def resetPasswordRequest(request: ResetPasswordRequestData):
    database = DatabaseControl()
    mailSender = MailSender()
    # Request Validation!!
    error = validateResetPasswordRequestData(request)
    if error != "":
        return failMessage(error)
    # Kullanıcı Bulunamadı!
    if not database.isEmailTaken(request.email):
        return failMessage("Kullanıcı bulunamadı!")
    # Doğrulanmamış Hesap
    if not database.isVerifiedEmail(request.email):
        return failMessage("Doğrulanmamış hesap parola sıfırlama talep edemez!")
    # Parola Sıfırlama Kodu Üret ve Veritabanına Kaydet
    reset_password_code = database.resetPasswordRequest(request.email)
    # Mail Gönder
    mailSender.sendResetPassword(request.email, reset_password_code)
    # Sonucu Döndür
    return successMessage("Doğrulama kodu içeren mail gönderildi!")

# 
@app.post("/auth/reset-password-verify")
def resetPasswordVerify(request: ResetPasswordVerifyData):
    database = DatabaseControl()
    # Request Validation!!
    error = validateResetPasswordVerifyData(request)
    if error != "":
        return failMessage(error)
    # Kullanıcı Bulunamadı!
    if not database.isEmailTaken(request.email):
        return failMessage("Kullanıcı bulunamadı!")
    # Doğrulanmamış Hesap
    if not database.isVerifiedEmail(request.email):
        return failMessage("Doğrulanmamış hesap parola sıfırlama talep edemez!")
    # Parola Sıfırlama Kodu Hatalı!
    if not database.verifyResetPassword(request.email, request.code):
        return failMessage("Parola sıfırlama kodu hatalı!")
    # Sonucu Döndür
    return successMessage("Parola sıfırlama isteği doğrulandı!")

# 
@app.post("/auth/reset-password")
def resetPassword(request: ResetPasswordData):
    database = DatabaseControl()
    # Request Validation!!
    error = validateResetPasswordData(request)
    if error != "":
        return failMessage(error)
    # Kullanıcı Bulunamadı!
    if not database.isEmailTaken(request.email):
        return failMessage("Kullanıcı bulunamadı!")
    # Doğrulanmamış Hesap
    if not database.isVerifiedEmail(request.email):
        return failMessage("Doğrulanmamış hesap parola sıfırlama talep edemez!")
    # Parola Sıfırlama Kodu Hatalı!
    if not database.verifyResetPassword(request.email, request.code):
        return failMessage("Parola sıfırlama kodu hatalı!")
    # Parolayı Değiştir
    database.changePassword(request.email, request.new_password)
    # Sonucu Döndür
    return successMessage("Parola başarıyla değiştirildi!")

# Başarılı Mesaj Örneği
def successMessage(message: str, data: list = []):
    return {
        "success": True,
        "message": message,
        "data": data
    }

# Başarısız Mesaj Örneği
def failMessage(message: str, error: list = []):
    return {
        "success": False,
        "message": message,
        "error": error
    }
