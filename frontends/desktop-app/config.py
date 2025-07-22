# ============================================================================
# File:    config.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

#####

ENV_DIR = PROJECT_ROOT / "env"
DB_DIR = PROJECT_ROOT / "db"
IMAGES_DIR = PROJECT_ROOT / "assets" / "images"

#####

STYLE_PATH = str(PROJECT_ROOT / "style.qss")

#####

ICON_PATH = str(IMAGES_DIR / "favicon.png")

#####

ENV_PATH = str(ENV_DIR / ".env")

#####

SESSION_PATH = str(DB_DIR / "token")
APP_DATA_PATH = str(DB_DIR / "app_data.db")

#####

INFO_ICON_PATH = str(IMAGES_DIR / "info.png")
WARNING_ICON_PATH = str(IMAGES_DIR / "warning.png")
VERIFICATION_ICON_PATH = str(IMAGES_DIR / "verification.png")

#####

PLAY_ICON_PATH = str(IMAGES_DIR / "play.png")
PAUSE_ICON_PATH = str(IMAGES_DIR / "pause.png")

NEXT_ICON_PATH = str(IMAGES_DIR / "next.png")
PREV_ICON_PATH = str(IMAGES_DIR / "previous.png")

BACKWARD_ICON_PATH = str(IMAGES_DIR / "backward.png")
FORWARD_ICON_PATH = str(IMAGES_DIR / "forward.png")

LIKE_ON_ICON_PATH = str(IMAGES_DIR / "like_on.png")
LIKE_OFF_ICON_PATH = str(IMAGES_DIR / "like_off.png")

SHUFFLE_ICON_PATH = str(IMAGES_DIR / "shuffle.png")
SHUFFLE_TRUE_ICON_PATH = str(IMAGES_DIR / "shuffle_true.png")
SHUFFLE_FALSE_ICON_PATH = str(IMAGES_DIR / "shuffle_false.png")

LOOP0_ICON_PATH = str(IMAGES_DIR / "loop_0.png")
LOOP1_ICON_PATH = str(IMAGES_DIR / "loop_1.png")
LOOP2_ICON_PATH = str(IMAGES_DIR / "loop_2.png")

VOLUME_ON_ICON_PATH = str(IMAGES_DIR / "volume_on.png")
VOLUME_OFF_ICON_PATH = str(IMAGES_DIR / "volume_off.png")

CLOSE_ICON_PATH = str(IMAGES_DIR / "close.png")

MUSIC_ICON_PATH = str(IMAGES_DIR / "music.png")
ARTIST_ICON_PATH = str(IMAGES_DIR / "artist.png")
PLAYLIST_ICON_PATH = str(IMAGES_DIR / "playlist.png")

ADD_ICON_PATH = str(IMAGES_DIR / "add.png")
DELETE_ICON_PATH = str(IMAGES_DIR / "delete.png")
