# ============================================================================
# File:    filename.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

import os

def pathToFileNameWithExtension(path: str):
	return os.path.basename(path.rstrip("/")).strip()

def pathToFileNameWithoutExtension(path: str):
	base = pathToFileNameWithExtension(path)
	name, _ext = os.path.splitext(base)
	return name.strip()

def pathToFileExtension(path: str):
	base = pathToFileNameWithExtension(path)
	_name, ext = os.path.splitext(base)
	return ext.strip()

def pathToSongName(path: str):
	fileName = pathToFileNameWithoutExtension(path)
	result = fileName.split("-")

	if len(result) == 1:
		return fileName.strip()

	return "-".join(result[1:]).strip()

def pathToArtistName(path: str):
	fileName = pathToFileNameWithoutExtension(path)
	result = fileName.split("-")

	if len(result) == 1:
		return "Bilinmeyen Sanatçı"

	return result[0].strip()

def pathToSong(path: str):
	return {
		"artist_name": pathToArtistName(path),
		"music_name": pathToSongName(path),
		"music_url": path
	}
