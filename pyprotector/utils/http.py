"""
	____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
	   /____/

Made With ❤️ By Ghoul & Marci
"""

import httpx


def getIPAddress() -> str:
    response = httpx.get("https://ipinfo.io/json").json()
    ip = response.get("ip")
    return ip


def hasInternet() -> bool:
    if httpx.get("https://google.com"):
        return True
    else:
        return False
