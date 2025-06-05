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
from typing import List


class ProtectorObservable:
    def __init__(self) -> None:
        self.obs: Observable = Observable()

    def dispatch(self, events: List[str], text: str, module: str, **kwargs) -> None:
        """
        It triggers an event.

        Args:
          event (str): The event name.
          text (str): The text that was sent
          module (str): The name of the module that triggered the event.

        Returns:
          None
        """
        for event in events:
            self.obs.trigger(event, text, module, **kwargs)
