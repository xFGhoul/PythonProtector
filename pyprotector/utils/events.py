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


class ProtectorEvent:
    def __init__(self, event: str, text: str, module: str, **kwargs) -> None:
        self.event: str = event
        self.text: str = text
        self.module: str = module
        self.extra: dict = kwargs


class ProtectorObservable:
    def __init__(self) -> None:
        self.obs: Observable = Observable()

    def dispatch(self, event: str, text: str, module: str, **kwargs) -> ProtectorEvent:
        """
        It triggers an event.

        Args:
          event (str): The event name.
          text (str): The text that was sent
          module (str): The name of the module that triggered the event.

        Returns:
          ProtectorEvent
        """
        self.obs.trigger(event, text, module, **kwargs)
        return ProtectorEvent(event, text, module, **kwargs)
