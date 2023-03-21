"""
    ____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
	/____/

Made With ❤️ By Ghoul & Marci
"""
from dataclasses import dataclass

from datetime import datetime


class KeyauthAppData:
    def __init__(self, data: dict) -> None:
        """Object representing JSON response from keyauth API

        Args:
            data (dict): Data Received
        """
        self.users: int = data["numUsers"]
        self.keys: int = data["numKeys"]
        self.version: int = data["version"]
        self.customer_panel: str = data["customerPanelLink"]
        self.onlineUsers: int = data["numOnlineUsers"]

    def __repr__(self) -> str:
        return f"Keyauth App ({self.version}) with {self.users} users, {self.keys} keys and {self.onlineUsers} online users"


class KeyauthUser:
    def __init__(self, data: dict) -> None:
        """Object representing JSON response from keyauth API

        Args:
            data (dict): Data Received
        """
        self.username: str = data["username"]
        self.ip: str = data["ip"]
        self.hwid: str = data["hwid"]
        self.expiry: str = datetime.utcfromtimestamp(
            int(data["subscriptions"][0]["expiry"])
        ).strftime("%Y-%m-%d %H:%M:%S")
        self.date_created: str = datetime.utcfromtimestamp(
            int(data["createdate"])
        ).strftime("%Y-%m-%d %H:%M:%S")
        self.last_login: str = datetime.utcfromtimestamp(
            int(data["lastlogin"])
        ).strftime("%Y-%m-%d %H:%M:%S")
        self.current_subscription: Subscription = Subscription(
            **data["subscriptions"][0]
        )
        self.subscriptions: list[Subscription] = [
            Subscription(**subscription) for subscription in data["subscriptions"]
        ]

    def __repr__(self) -> str:
        return self.username


@dataclass
class KeyauthChat:
    author: str
    message: str
    timestamp: str

    def __post_init__(self) -> None:
        self.timestamp = datetime.utcfromtimestamp(int(self.timestamp)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )


@dataclass
class Subscription:
    subscription: str
    key: str
    expiry: str
    timeleft: str

    def __post_init__(self) -> None:
        self.expiry = datetime.utcfromtimestamp(int(self.expiry)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.timeleft = datetime.utcfromtimestamp(int(self.timeleft)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
