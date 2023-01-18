"""
    ____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
       /____/

Made With ❤️ By Ghoul & Marci
"""

from observable import Observable


class ProtectorObservable:
    def __init__(self) -> None:
        self.obs = Observable()

    def dispatch(self, text: str, module: str) -> None:
        self.obs.trigger("pyprotector_detect", text, module)

    def disable(self) -> None:
        self.obs.off("pyprotector_detect")

    def enable(self) -> None:
        self.obs.on("pyprotector_detect")
