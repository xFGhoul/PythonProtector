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
    """
    Get IP Address of User

    Returns:
      The IP address of the machine that is running the code.
    """
    try:
        response = httpx.get("https://ipinfo.io/json")
        response.raise_for_status()
    except (
        httpx.TimeoutException,
        httpx.RequestError,
        httpx.ConnectError,
        httpx.HTTPError,
    ):
        return "No IP Address"

    response = response.json()
    return response.get("ip")


def hasInternet() -> bool:
    """
    Checks if the user has internet

    Returns:
      A boolean value.
    """
    try:
        response = httpx.get("https://www.google.com", timeout=5)
        response.raise_for_status()
        return True
    except (
        httpx.TimeoutException,
        httpx.RequestError,
        httpx.ConnectError,
        httpx.HTTPError,
    ):
        return False
