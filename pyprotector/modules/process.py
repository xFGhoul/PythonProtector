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


class AntiProcess(Module):
    def __init__(
            self,
            webhook: Webhook,
            logger: Logger,
            exit: bool,
            report: bool,
            event: Event) -> None:
        self.webhook: Webhook = webhook
        self.logger: Logger = logger
        self.exit: bool = exit
        self.report: bool = report
        self.event: Event = event

    @property
    def name(self) -> str:
        return "Anti Process"
    
    @property
    def version(self) -> int:
        return 1.0

    def CheckProcessList(self) -> None:
        while True:
            try:
                time.sleep(0.7)
                for process in psutil.process_iter():
                    if any(
                        process_name in process.name().lower()
                        for process_name in Lists.BLACKLISTED_PROGRAMS
                    ):
                        try:
                            if self.report:
                                self.logger.info(
                                    f"{process.name} Process Was Running")
                                self.webhook.send(
                                    f"`{process.name()}` was detected running on the system.", self.name, )
                                self.event.dispatch(
                                    "process_running",
                                    f"{process.name()} was detected running on the system.",
                                    self.name,
                                    process=process,
                                )
                                self.event.dispatch(
                                    "pyprotector_detect",
                                    f"{process.name()} was detected running on the system.",
                                    self.name,
                                    process=process,
                                )
                            process.kill()
                            if self.exit:
                                os._exit(1)
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
            except BaseException:
                pass

    def CheckWindowNames(self) -> None:
        def winEnumHandler(hwnd, ctx) -> None:
            if win32gui.GetWindowText(hwnd).lower(
            ) in Lists.BLACKLISTED_WINDOW_NAMES:
                pid: tuple[int, int] = GetWindowThreadProcessId(hwnd)
                if isinstance(pid, int):
                    try:
                        psutil.Process(pid).terminate()
                    except BaseException:
                        pass
                else:
                    for process in pid:
                        try:
                            psutil.Process(process).terminate()
                        except BaseException:
                            pass
                self.logger.info(f"{win32gui.GetWindowText(hwnd)} Found")
                if self.report:
                    self.webhook.send(
                        f"Debugger {win32gui.GetWindowText(hwnd)}", self.name
                    )
                    self.event.dispatch(
                        "window_name_detected",
                        f"Debugger {win32gui.GetWindowText(hwnd)} Found Open",
                        self.name,
                        window_name=win32gui.GetWindowText(hwnd),
                    )
                    self.event.dispatch(
                        "pyprotector_detect",
                        f"Debugger {win32gui.GetWindowText(hwnd)} Found Open",
                        self.name,
                        window_name=win32gui.GetWindowText(hwnd),
                    )
                if self.exit:
                    os._exit(1)

        while True:
            win32gui.EnumWindows(winEnumHandler, None)
