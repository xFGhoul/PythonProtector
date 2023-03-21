"""
    ____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
	/____/

Made With ❤️ By Ghoul & Marci
"""


class KeyauthException(BaseException):
    """
    Base Class of All Keyauth Issues
    """


class NewVersionAvailable(KeyauthException):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ApplicationNotFound(KeyauthException):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class RequestError(KeyauthException):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NotInitialized(KeyauthException):
    def __init__(self, message: str) -> None:
        super().__init__(message)
