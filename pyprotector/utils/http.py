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


def get_ip_address() -> str:
    data = httpx.get("https://ipinfo.io/json").json()
    ip = data.get("ip")
    return ip


def hasInternet() -> bool:
    if httpx.get("https://google.com"):
        return True
    else:
        return False
