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
import ctypes

from ctypes import WinDLL

from ..types import Event, Logger
from ..abc import Module
from ..utils.webhook import Webhook


class AntiAnalysis(Module):
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
        return "Anti Analysis"

    @property
    def version(self) -> int:
        return 1.0

    def CheckDebugPrivilege(self) -> None:
        hToken = ctypes.c_void_p()
        if (
            self.ntdll.NtOpenProcessToken(
                self.kernel32.GetCurrentProcess(), 0x0020, ctypes.byref(hToken)
            )
            != 0
        ):
            return

        privileges = ctypes.create_string_buffer(1024)
        return_length = ctypes.c_ulong()
        if (
            self.ntdll.NtQueryInformationToken(
                hToken,
                0x03,
                ctypes.byref(privileges),
                ctypes.sizeof(privileges),
                ctypes.byref(return_length),
            )
            != 0
        ):
            self.ntdll.NtClose(hToken)
            return

        debug_privilege = (ctypes.c_int *
                           (return_length.value //
                            8)).from_buffer(privileges)
        for priv in debug_privilege:
            if priv.s_luid.LowPart == 21 and priv.s_attributes & 0x00000002:
                self.ntdll.NtClose(hToken)
                self.logger.info("Debug Privilege Found Enabled")
                if self.report:
                    self.webhook.send("Debug Privilege Enabled", self.name)
                    self.event.dispatch(
                        "debug_privilege_found",
                        "Debug Privilege Enabled",
                        self.name)
                    self.event.dispatch(
                        "pyprotector_detect",
                        "Debug Privilege Enabled",
                        self.name)
                if self.exit:
                    os._exit(1)

        self.ntdll.NtClose(hToken)

    def HideThreads(self) -> None:
        PID = self.kernel32.GetCurrentProcessId()
        hProcess = self.kernel32.OpenProcess(0x1F0FFF, False, PID)
        if hProcess is None:
            return

        TID = self.kernel32.GetCurrentThreadId()
        hThread = self.kernel32.OpenThread(0x1F03FF, False, TID)
        if hThread is None:
            self.kernel32.CloseHandle(hProcess)
            return

        self.ntdll.NtSetInformationThread(
            hThread, 0x11, ctypes.byref(
                (ctypes.c_int(1)), ctypes.sizeof(
                    ctypes.c_int)))

        self.kernel32.CloseHandle(hThread)
        self.kernel32.CloseHandle(hProcess)

    def CheckDebugObject(self) -> None:
        PID = self.kernel32.GetCurrentProcessId()

        hProcess = self.kernel32.OpenProcess(0x1F0FFF, False, PID)
        if hProcess is None:
            return

        HasDebugObject = (
            self.ntdll.NtQueryInformationProcess(
                hProcess,
                0x1E,
                ctypes.byref(ctypes.c_int(0)),
                ctypes.sizeof(ctypes.c_int),
                ctypes.byref(ctypes.c_int(0)),
            )
            == 0
        )
        if HasDebugObject:
            self.kernel32.CloseHandle(hProcess)
            self.logger.info("Debug Object Handle Found")
            if self.report:
                self.webhook.send("Debug Object Handle Detected", self.name)
                self.event.dispatch(
                    "debug_object_handle_found",
                    "Debug Object Handle Detected",
                    self.name,
                )
                self.event.dispatch(
                    "pyprotector_detect",
                    "Debug Object Handle Detected",
                    self.name,
                )
            if self.exit:
                os._exit((1))

    def CheckSEDebugName(self) -> None:
        PID = self.kernel32.GetCurrentProcessId()

        hProcess = self.kernel32.OpenProcess(0x1F0FFF, False, PID)
        if hProcess is None:
            return

        DebugObjectHandle = ctypes.c_void_p()
        if (
            self.ntdll.NtQueryObject(
                hProcess,
                0x1F,
                ctypes.byref(DebugObjectHandle),
                ctypes.sizeof(DebugObjectHandle),
                None,
            )
            == 0
        ):
            self.kernel32.CloseHandle(hProcess)
            self.logger.info("Debug Object Handle Found")
            if self.report:
                self.webhook.send("Debug Object Handle Detected", self.name)
                self.event.dispatch(
                    "se_debug_name", "Debug Object Handle Detected", self.name
                )
                self.event.dispatch(
                    "pyprotector_detect",
                    "Debug Object Handle Detected",
                    self.name)
            if self.exit:
                os._exit((1))

    def CheckNtGlobalFlag(self) -> None:
        PEB = ctypes.c_int(0)
        self.ntdll.NtQueryInformationProcess.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_void_p,
            ctypes.c_ulong,
            ctypes.POINTER(ctypes.c_ulong),
        ]
        self.ntdll.NtQueryInformationProcess(
            self.kernel32.GetCurrentProcess(),
            0,
            ctypes.byref(PEB),
            ctypes.sizeof(PEB),
            None,
        )
        if (PEB.value & 0x00000001) != 0:
            self.logger.info(
                "NT_GLOBAL_FLAG_DEBUGGED Found in the Process Environment Block"
            )
            if self.report:
                self.webhook.send(
                    "NT_GLOBAL_FLAG_DEBUGGED Found in the Process Environment Block", self.name, )
                self.event.dispatch(
                    "nt_global_flag_debugged",
                    "NT_GLOBAL_FLAG_DEBUGGED Found in the Process Environment Block",
                    self.name,
                )
                self.event.dispatch(
                    "pyprotector_detect",
                    "NT_GLOBAL_FLAG_DEBUGGED Found in the Process Environment Block",
                    self.name,
                )
            if self.exit:
                os._exit(1)

    def CheckHardwareBreakpoints(self) -> None:
        ThreadContext = ctypes.c_void_p()
        TID = self.kernel32.GetCurrentThreadId()
        hThread = self.kernel32.OpenThread(0x1F03FF, False, TID)
        if hThread is None:
            return

        if not self.kernel32.GetThreadContext(
                hThread, ctypes.byref(ThreadContext)):
            self.kernel32.CloseHandle(hThread)
            return

        if (
            ThreadContext.contents.Dr0 != 0
            or ThreadContext.contents.Dr1 != 0
            or ThreadContext.contents.Dr2 != 0
            or ThreadContext.contents.Dr3 != 0
        ):
            self.kernel32.CloseHandle(hThread)
            self.logger.info("Hardware Breakpoints Found Set")
            if self.report:
                self.webhook.send("Hardware Breakpoints Found Set", self.name)
                self.event.dispatch(
                    "hardware_breakpoint_set",
                    "Hardware Breakpoints Found Set",
                    self.name,
                )
                self.event.dispatch(
                    "pyprotector_detect",
                    "Hardware Breakpoints Found Set",
                    self.name,
                )
            if self.exit:
                os._exit(1)

        self.kernel32.CloseHandle(hThread)

    def CheckDebugFilterState(self) -> None:
        self.ntdll.DbgSetDebugFilterState(0, 0)

        DebugFilterState = ctypes.c_uint()
        self.ntdll.DbgQueryDebugFilterState(0, ctypes.byref(DebugFilterState))

        if DebugFilterState.value != 0:
            self.logger.info("Debug Filter State is not 0")
            if self.report:
                self.webhook.send(
                    "Debug Filter State `!= 0`, debugging detected", self.name
                )
                self.event.dispatch(
                    "debug_filter_state",
                    "Debug Filter State is not 0",
                    self.name)
                self.event.dispatch(
                    "pyprotector_detect",
                    "Debug Filter State is not 0",
                    self.name)
            if self.exit:
                os._exit(1)

    def CheckPEB(self) -> None:
        class PEB(ctypes.Structure):
            _fields_ = [("BeingDebugged", ctypes.c_byte)]

        process = self.kernel32.GetCurrentProcess()

        peb = PEB()
        self.ntdll.NtQueryInformationProcess(
            process, 0, ctypes.pointer(peb), ctypes.sizeof(peb), None
        )

        if peb.BeingDebugged:
            self.logger.info("Process Being Debugged")
            if self.report:
                self.webhook.send("Process Found Being Debugged", self.name)
                self.event.dispatch(
                    "peb_being_debugged",
                    "Process Found Being Debugged",
                    self.name)
                self.event.dispatch(
                    "pyprotector_detect",
                    "Process Found Being Debugged",
                    self.name)
            if self.exit:
                os._exit(1)

    def StartAnalyzing(self) -> None:
        if self.report:
            self.logger.info("Starting Analysis Checks")
        self.CheckDebugPrivilege()
        self.CheckDebugObject()
        self.CheckSEDebugName()
        self.CheckNtGlobalFlag()
        self.CheckHardwareBreakpoints()
        self.CheckDebugFilterState()
        self.CheckPEB()
        if self.report:
            self.logger.info("Finished All Analysis Checks")

        if self.report:
            self.logger.info("Hiding Threads")
        self.HideThreads()
        if self.report:
            self.logger.info("Threads Hidden")
