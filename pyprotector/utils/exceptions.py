"""
	____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
	   /____/

Made With ❤️ By Ghoul & Marci
"""


class ProtectorException(Exception):
    """Base Class For All PythonProtector Exceptions"""


class ModulesNotValid(ProtectorException):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class DetectionsNotValid(ProtectorException):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class LogsPathEmpty(ProtectorException):
    def __init__(self, message: str) -> None:
        super().__init__(message)
