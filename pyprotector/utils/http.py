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
    try:
        response = httpx.get("https://ipinfo.io/json").json()
    except (
        httpx.TimeoutException,
        httpx.RequestError,
        httpx.ConnectError,
        httpx.HTTPError,
    ):
        return "No IP Address"

    ip = response.get("ip")
    return ip


def hasInternet() -> bool:
    try:
        if httpx.get("https://google.com"):
            return True
        else:
            return False
    except (
        httpx.TimeoutException,
        httpx.RequestError,
        httpx.ConnectError,
        httpx.HTTPError,
    ):
        return False
