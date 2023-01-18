"""
    ____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
       /____/

Made With ❤️ By Ghoul & Marci
"""


from abc import ABCMeta, abstractmethod


class Module(metaclass=ABCMeta):
    def __init__(self, webhook, logger, exit, report, event) -> None:
        self.webhook = webhook
        self.logger = logger
        self.exit = exit
        self.report = report
        self.event = event

    @property
    @abstractmethod
    def name(self):
        pass
