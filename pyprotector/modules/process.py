"""
        ____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
           /____/

Made With ❤️ By Ghoul & Marci
"""

import os
import time

import psutil
import win32gui

from win32process import GetWindowThreadProcessId

from ..types import Event, Logger
from ..abc import Module
from ..constants import Lists
from ..utils.webhook import Webhook
import contextlib


class AntiProcess(Module):
    def __init__(
        self, webhook: Webhook, logger: Logger, exit: bool, report: bool, event: Event
    ) -> None:
        self.webhook: Webhook = webhook
        self.logger: Logger = logger
        self.exit: bool = exit
        self.report: bool = report
        self.event: Event = event

    @property
    def name(self) -> str:
        return "Anti Process"

    @property
    def version(self) -> float:
        return 1.0

    def CheckProcessList(self) -> None:
        """
        Checks the Process List for any Blacklisted Programs
        """
        while True:
            try:
                time.sleep(2.0)
                for process in psutil.process_iter():
                    if any(
                        process_name in process.name().lower()
                        for process_name in Lists.BLACKLISTED_PROGRAMS
                    ):
                        try:
                            if self.report:
                                self.logger.info(f"{process.name} Process Was Running")
                                self.webhook.send(
                                    f"`{process.name()}` was detected running on the system.",
                                    self.name,
                                )
                                self.event.dispatch(
                                    ["process_running", "pyprotector_detect"],
                                    f"{process.name()} was detected running on the system.",
                                    self.name,
                                    process=process,
                                )
                            process.kill()
                            if self.exit:
                                self.logger.info("Exiting Due to Blacklisted Process")
                                os._exit(1)
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
            except BaseException:
                pass

    def CheckWindowNames(self) -> None:
        """Checks Window Names Against Blacklisted List"""

        def winEnumHandler(hwnd, _ctx) -> None:
            if (
                win32gui.GetWindowText(hwnd).lower()
                not in Lists.BLACKLISTED_WINDOW_NAMES
            ):
                return
            pid: tuple[int, int] = GetWindowThreadProcessId(hwnd)
            if isinstance(pid, int):
                with contextlib.suppress(BaseException):
                    psutil.Process(pid).terminate()

            else:
                for process in pid:
                    with contextlib.suppress(BaseException):
                        psutil.Process(process).terminate()

            self.logger.info(f"{win32gui.GetWindowText(hwnd)} Found")
            if self.report:
                self.webhook.send(
                    f"Debugger {win32gui.GetWindowText(hwnd)}",
                    self.name,
                )
                self.event.dispatch(
                    ["window_name_detected", "pyprotector_detect"],
                    f"Debugger {win32gui.GetWindowText(hwnd)} Found Open",
                    self.name,
                    window_name=win32gui.GetWindowText(hwnd),
                )
            if self.exit:
                self.logger.info("Exiting Due to Blacklisted Window Name")
                os._exit(1)

        while True:
            win32gui.EnumWindows(winEnumHandler, None)
