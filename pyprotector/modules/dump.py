"""
	____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
	   /____/

Made With ❤️ By Ghoul & Marci
"""
import ctypes
import win32api


from ctypes import WinDLL
from ctypes import wintypes

from ..types import Event, Logger
from ..abc import Module
from ..utils.webhook import Webhook


class AntiDump(Module):
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

        self.kernel32: WinDLL = ctypes.windll.kernel32
        self.ntdll: WinDLL = ctypes.windll.ntdll

    @property
    def name(self) -> str:
        return "Anti Dump"
    
    @property
    def version(self) -> int:
        return 1.0

    def ErasePEHeaderFromMemory(self) -> None:
        oldProtect = wintypes.DWORD(0)

        baseAddress = ctypes.c_int(win32api.GetModuleHandle(None))

        self.kernel32.VirtualProtect(
            ctypes.pointer(baseAddress), 4096, 0x04, ctypes.pointer(oldProtect)
        )
        ctypes.memset(
            ctypes.pointer(baseAddress),
            4096,
            ctypes.sizeof(baseAddress))
        self.event.dispatch(
            "pe_header_erased", "PE Header Erased From Memory", self.name
        )

    def StartChecks(self) -> None:
        if self.report:
            self.logger.info("Starting Anti Dump")

        if self.report:
            self.logger.info("Erasing PE Header From Memory")
        self.ErasePEHeaderFromMemory()
        if self.report:
            self.logger.info("PE Header Erased From Memory")

            self.logger.info("Finished Anti Dump")
