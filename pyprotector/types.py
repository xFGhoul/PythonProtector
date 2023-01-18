"""
	____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
	   /____/image.png

Made With ❤️ By Ghoul & Marci
"""
from typing import Type

from pyprotector.utils.events import ProtectorObservable
from loguru import logger

Event = Type[ProtectorObservable]
Logger = Type[logger]
