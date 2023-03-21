"""
    ____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
	/____/

Made With ❤️ By Ghoul & Marci
"""

import uuid
import httpx
import subprocess

from typing import Final, Optional, Union, Dict, List
from Crypto.Hash import SHA256
from httpx import Response

from ._constants import API
from .models import KeyauthAppData, KeyauthUser, KeyauthChat
from .exceptions import NewVersionAvailable, ApplicationNotFound, RequestError


class Keyauth:
    def __init__(
        self, name: str, ownerid: str, secret: str, version: str, file_hash: str
    ) -> None:
        self.name: str = name
        self.ownerid: str = ownerid
        self.secret: str = secret
        self.version: str = version
        self.file_hash: str = file_hash

        self.__session_id: None = None

        self.hwid: Final[str] = (
            subprocess.check_output("wmic csproduct get uuid")
            .decode()
            .split("\n")[1]
            .strip()
        )
        self.initialized: bool = False

    def _post_data(self, type: str, data: Optional[Dict] = None) -> Dict:
        _post_data = {
            "type": type,
            "sessionid": self.__session_id,
            "name": self.name,
            "ownerid": self.ownerid,
        }

        if data is None:
            pass
        else:
            _post_data.update(data)

        return _post_data

    def __request(self, data: Dict) -> Response:
        try:
            response = httpx.post(API.BASE_URL, params=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPError):
            raise RequestError("Internal Request Failed!")

    def initialize(self) -> Union[bool, KeyauthAppData]:
        """Initializes your Keyauth Application

        Raises:
            RuntimeError: If you have already initialized
            ApplicationNotFound: If your application does not exist
            NewVersionAvailable: If there is a new version available
            RequestError: There is an issue with the request

        Returns:
            Union[bool, KeyauthAppData]: Returns self.initialized and a class representing your app data
        """
        if self.__session_id is not None:
            raise RuntimeError("This session has already been initialized!")

        self._enc_key: str = SHA256.new(str(uuid.uuid4())[:8].encode()).hexdigest()

        response: Response = self.__request(
            self._post_data(
                type="init",
                data={
                    "ver": self.version,
                    "hash": self.file_hash,
                    "enckey": self._enc_key,
                },
            )
        )

        if response == "KeyAuth_Invalid":
            raise ApplicationNotFound("This Application Doesn't Exist")

        if response["message"] == "invalidver":
            raise NewVersionAvailable("This Version Is Out Of Date!")

        if not response["success"]:
            raise RequestError(response["message"])

        self.__session_id = response["sessionid"]
        self.initialized: bool = True
        return (self.initialized, KeyauthAppData(response["appinfo"]))

    def register(
        self, username: str, password: str, license: str, hwid: Optional[str] = None
    ) -> KeyauthUser:
        """Creates user with license key
        Args:
            username (str): user's input for username
            password (str): user's input for password
            license (str): user's input for license key
            hwid (Optional[str]): Hardware ID. Defaults to None.

        Raises:
            RequestError: If the request has failed

        Returns:
            KeyauthUser: The newly registered user
        """
        if hwid is None:
            hwid: str = self.hwid

        response: Response = self.__request(
            self._post_data(
                type="register",
                data={
                    "username": username,
                    "password": password,
                    "license": license,
                    "hwid": hwid,
                },
            )
        )

        if not response["success"]:
            raise RequestError(response["message"])

        return KeyauthUser(response["info"])

    def upgrade(self, username: str, key: str) -> KeyauthUser:
        """Add subscription to an user

        Args:
            username (str): username you want upgraded
            key (str): user's input for license key

        Raises:
            RequestError: If the request has failed

        Returns:
            KeyauthUser: Upgraded User
        """
        response: Response = self.__request(
            self._post_data(type="upgrade", data={"username": username, "key": key})
        )

        if not response["success"]:
            raise RequestError(response["message"])

        return KeyauthUser(response["info"])

    def login(
        self, username: str, password: str, hwid: Optional[str] = None
    ) -> KeyauthUser:
        """Login with username & password

        Args:
            username (str): user's input for username
            password (str): user's input for password
            hwid (Optional[str]): Hardware ID. Defaults to None.

        Raises:
            RequestError: If the request has failed

        Returns:
            KeyauthUser: Logged in User
        """
        if hwid is None:
            hwid: str = self.hwid

        response: Response = self.__request(
            self._post_data(
                type="login",
                data={"username": username, "password": password, "hwid": hwid},
            )
        )

        if not response["success"]:
            raise RequestError(response["message"])

        return KeyauthUser(response["info"])

    def license(self, license: str, hwid: Optional[str] = None) -> KeyauthUser:
        """Login with license key

        Args:
            license (str): user's input for license key
            hwid (Optional[str]): Hardware ID. Defaults to None.

        Raises:
            RequestError: If the request has failed

        Returns:
            KeyauthUser: Licensed User
        """
        if hwid is None:
            hwid: str = self.hwid

        response: Response = self.__request(
            self._post_data(type="license", data={"key": license})
        )

        if not response["success"]:
            raise RequestError(response["message"])

        return KeyauthUser(response["info"])

    def getOnlineUsers(self) -> Dict:
        """Get Online Users

        Raises:
            RequestError: If The Request has Failed

        Returns:
            Dict: Dictionary of Online Users
        """
        response: Response = self.__request(self._post_data(type="fetchOnline"))

        if not response["success"]:
            raise RequestError(response["message"])

        return response["users"]

    def setvar(self, variable: str, data: str) -> None:
        """Set Variable

        Args:
            variable (str): Variable Name
            data (str): Variable Value

        Raises:
            RequestError: If The Reuqest has Failed

        Returns:
            None
        """
        response: Response = self.__request(
            self._post_data(type="setvar", data={"var": variable, "data": data})
        )

        if not response["success"]:
            raise RequestError(response["message"])

        return response

    def getvar(self, variable: str) -> str:
        """Get Variable

        Args:
            variable (str): Variable Name

        Raises:
            RequestError: If The Reuqest has Failed

        Returns:
            str: Variable
        """
        response: Response = self.__request(
            self._post_data(type="getvar", data={"var": variable})
        )

        if not response["success"]:
            raise RequestError(response["message"])

        return response["success"]

    def var(self, variable: str) -> None:
        """Variable

        Args:
            variable (str): Variable Name

        Raises:
            RequestError: If The Reuqest has Failed

        Returns:
            str: Variable
        """
        response: Response = self.__request(
            self._post_data(type="var", data={"varid": variable})
        )

        if not response["success"]:
            raise RequestError(response["message"])

        return response["success"]

    def checkBlacklist(self, hwid: Optional[str] = None) -> bool:
        """Check The Blacklist

        Args:
            hwid (Optional[str]): User HWID. Defaults to None.

        Raises:
            RequestError: If The Reuqest has Failed

        Returns:
            bool: If The User Is Blacklisted
        """
        if hwid is None:
            hwid: str = self.hwid

        response: Response = self.__request(
            self._post_data(type="checkblacklist", data={"hwid": hwid})
        )

        if not response["success"]:
            raise RequestError(response["message"])

        return response["success"]

    def getChat(self, channel: str) -> List[KeyauthChat]:
        """Get Chats

        Args:
            channel (str): Channel Name

        Raises:
            RequestError: If The Reuqest has Failed

        Returns:
            List[KeyauthChat]: List Of Keyauth Chats
        """
        response: Response = self.__request(
            self._post_data(type="chatget", data={"channel": channel})
        )

        if not response["success"]:
            raise RequestError(response["message"])

        return [KeyauthChat(**chat) for chat in response["messages"]]

    def sendChat(self, channel: str, message: str) -> str:
        """Send A Chat

        Args:
            channel (str): Channel Name
            message (str): Message

        Raises:
            RequestError: If The Reuqest has Failed

        Returns:
            str: Response
        """
        response: Response = self.__request(
            self._post_data(
                type="chatsend", data={"channel": channel, "message": message}
            )
        )

        if not response["success"]:
            raise RequestError(response["message"])

        return response["message"]

    def download(self, file_id: str) -> bytes:
        """Download File

        Args:
            file_id (str): File ID

        Raises:
            RequestError: If The Reuqest has Failed

        Returns:
            bytes: Bytes Object
        """
        response: Response = self.__request(
            self._post_data(type="file", data={"fileid": file_id})
        )

        if not response["success"]:
            raise RequestError(response["message"])

        file = bytes.fromhex(response["contents"])
        return file

    def checkSession(self) -> bool:
        """Check Session

        Raises:
            RequestError: If The Reuqest has Failed

        Returns:
            bool: If The Session is Valid
        """
        response: Response = self.__request(self._post_data(type="check"))

        if not response["success"]:
            raise RequestError(response["message"])

        return response["success"]

    def changeUsername(self, username: str) -> bool:
        """Change Username

        Args:
            username (str): New Username

        Raises:
            RequestError: If The Reuqest has Failed

        Returns:
            bool: If the username has changed or not
        """
        response: Response = self.__request(
            self._post_data(type="changeUsername", data={"newUsername": username})
        )

        if not response["success"]:
            raise RequestError(response["message"])

        return response["success"]

    def log(self, user: str, message: str) -> None:
        """Log Message

        Args:
            user (str): Username
            message (str): Message
        """
        self.__request(
            self._post_data(type="log", data={"user": user, "message": message})
        )

    def webhook(self, webhook_id: str, params: str) -> None:
        """Send Webhook

        Args:
            webhook_id (str): Webhook ID
            params (str): Parameters
        """
        self.__request(
            self._post_data(
                type="webhook", data={"webid": webhook_id, "params": params}
            )
        )

    def ban(self) -> None:
        """Ban User"""
        self.__request(self._post_data(type="ban"))
