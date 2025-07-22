# ============================================================================
# File:    createCode.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

import random
import string

def createCode(length):
	characters = string.ascii_letters + string.digits

	return ''.join([random.choice(characters) for _ in range(length)])

def createFormattedCode(length, count):
	result = ""
	for _ in range(count):
		result += createCode(length) + " "
	result = result[:-1]
	return result
