# ============================================================================
# File:    config.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

#####

DB_DIR = PROJECT_ROOT / ".." / "db"
TEMPLATE_DIR = PROJECT_ROOT / "templates"


#####

DATABASE_PATH = str(DB_DIR / "database.db")
ERROR_LOG_PATH = str(DB_DIR / "error.log")

#####

RESET_PASSWORD_TEMPLATE_PATH = str(TEMPLATE_DIR / "reset_password_mail.txt")
SUCCESS_SIGNUP_TEMPLATE_PATH = str(TEMPLATE_DIR / "success_signup_mail.txt")
VERIFICATION_EMAIL_TEMPLATE_PATH = str(TEMPLATE_DIR / "verification_mail.txt")
