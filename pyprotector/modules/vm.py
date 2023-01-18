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
import os
import re
import sys
import uuid

import httpx

from typing import List

from ..types import Event, Logger
from ..abc import Module
from ..constants import Lists, UserInfo
from ..utils.webhook import Webhook


class AntiVM(Module):
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

        self.HWIDS: List[str] = httpx.get(
            "https://raw.githubusercontent.com/xFGhoul/PythonProtector/dev/data/hwid_list.txt"
        ).text
        self.PC_NAMES: List[str] = httpx.get(
            "https://raw.githubusercontent.com/xFGhoul/PythonProtector/dev/data/pc_name_list.txt"
        ).text
        self.PC_USERNAMES: List[str] = httpx.get(
            "https://raw.githubusercontent.com/xFGhoul/PythonProtector/dev/data/pc_username_list.txt"
        ).text
        self.IPS: List[str] = httpx.get(
            "https://raw.githubusercontent.com/xFGhoul/PythonProtector/dev/data/ip_list.txt"
        ).text
        self.MACS: List[str] = httpx.get(
            "https://raw.githubusercontent.com/xFGhoul/PythonProtector/dev/data/mac_list.txt"
        ).text
        self.GPUS: List[str] = httpx.get(
            "https://raw.githubusercontent.com/xFGhoul/PythonProtector/dev/data/gpu_list.txt"
        ).text
        self.PLATFORMS: List[str] = httpx.get(
            "https://raw.githubusercontent.com/xFGhoul/PythonProtector/dev/data/pc_platforms.txt"
        ).text

    @property
    def name(self):
        return "Anti VM"

    def get_base_prefix_compat(self) -> None:
        return (
            getattr(sys, "base_prefix", None)
            or getattr(sys, "real_prefix", None)
            or sys.prefix
        )

    def CheckLists(self) -> None:
        if UserInfo.HWID in self.HWIDS:
            self.logger.info(
                f"Blacklisted HWID Detected. HWID: {UserInfo.HWID}")
            if self.report:
                self.webhook.send(
                    f"Blacklisted HWID Detected: `{UserInfo.HWID}`", self.name
                )
                self.event.dispatch("Blacklisted HWID Detected", self.name)
            if self.exit:
                os._exit(1)

        if UserInfo.USERNAME in self.PC_USERNAMES:
            self.logger.info(f"Blacklisted PC User: {UserInfo.USERNAME}")
            if self.report:
                self.webhook.send(
                    f"Blacklisted PC User: `{UserInfo.USERNAME}`", self.name
                )
                self.event.dispatch("Blacklisted PC User Detected", self.name)
            if self.exit:
                os._exit(1)

        if UserInfo.PC_NAME in self.PC_NAMES:
            self.logger.info(f"Blacklisted PC Name: {UserInfo.PC_NAME}")
            if self.report:
                self.webhook.send(
                    f"Blacklisted PC Name: `{UserInfo.PC_NAME}`", self.name
                )
                self.event.dispatch("Blacklisted PC Name Detected", self.name)
            if self.exit:
                os._exit(1)

        if UserInfo.IP in self.IPS:
            self.logger.info(f"Blacklisted IP: {UserInfo.IP}")
            if self.report:
                self.webhook.send(
                    f"Blacklisted IP: `{UserInfo.IP}`", self.name)
                self.event.dispatch("Blacklisted IP Detected", self.name)
            if self.exit:
                os._exit(1)

        if UserInfo.MAC in self.MACS:
            self.logger.info(f"Blacklisted MAC: {UserInfo.MAC}")
            if self.report:
                self.webhook.send(
                    f"Blacklisted MAC: `{UserInfo.MAC}`", self.name)
                self.event.dispatch("Blacklisted MAC Detected", self.name)
            if self.exit:
                os._exit(1)

        if UserInfo.GPU in self.GPUS:
            self.logger.info(f"Blacklisted GPU: {UserInfo.GPU}")
            if self.report:
                self.webhook.send(
                    f"Blacklisted GPU: `{UserInfo.GPU}`", self.name)
                self.event.dispatch("Blacklisted GPU Detected", self.name)
            if self.exit:
                os._exit(1)

    def CheckVirtualEnv(self) -> None:
        if self.get_base_prefix_compat() != sys.prefix:
            if self.exit:
                os._exit(1)

    def CheckRegistry(self) -> None:
        reg1: int = os.system(
            "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2> nul"
        )
        reg2: int = os.system(
            "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2> nul"
        )

        if reg1 != 1 and reg2 != 1:
            self.logger.info("VMWare Registry Detected")
            if self.report:
                self.webhook.send("VMWare Registry Detected", self.name)
                self.event.dispatch("VMWare Registry Detected", self.name)
            if self.exit:
                os._exit(1)

    def CheckMacAddress(self) -> None:
        mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
        vmware_mac_list = ["00:05:69", "00:0c:29", "00:1c:14", "00:50:56"]
        if mac_address[:8] in vmware_mac_list:
            self.logger.info("VMWare MAC Address Detected")
            if self.report:
                self.webhook.send("VMWare MAC Address Detected", self.name)
                self.event.dispatch("VMWare MAC Address Detected", self.name)
            if self.exit:
                os._exit(1)

    def CheckScreenSize(self) -> None:
        x = ctypes.windll.user32.GetSystemMetrics(0)
        y = ctypes.windll.user32.GetSystemMetrics(1)
        if x <= 200 or y <= 200:
            self.logger.info(f"Screen Size X: {x} | Y: {y}")
            if self.report:
                self.webhook.send(
                    f"Screen Size Is: **x**: {x} | **y**: {y}", self.name)
                self.event.dispatch(f"Screen Size X: {x} | Y: {y}", self.name)
            if self.exit:
                os._exit(1)

    def CheckProcessesAndFiles(self) -> None:
        vmware_dll: str = os.path.join(
            os.environ["SystemRoot"], "System32\\vmGuestLib.dll"
        )
        virtualbox_dll: str = os.path.join(
            os.environ["SystemRoot"], "vboxmrxnp.dll")

        process: str = os.popen(
            'TASKLIST /FI "STATUS eq RUNNING" | find /V "Image Name" | find /V "="'
        ).read()
        processList = []

        for processNames in process.split(" "):
            if ".exe" in processNames:
                processList.append(
                    processNames.replace(
                        "K\n",
                        "").replace(
                        "\n",
                        ""))

        if any(Lists.VIRTUAL_MACHINE_PROCESSES) in processList:
            self.logger.info("Blacklisted Virtual Machine Process Running")
            if self.report:
                self.webhook.send(
                    "Blacklisted Virtual Machine Process Running", self.name
                )
                self.event.dispatch(
                    "Blacklisted Virtual Machine Process Running", self.name
                )
            if self.exit:
                os._exit(1)

        if os.path.exists(vmware_dll):
            self.logger.info("VMWare DLL Detected")
            if self.report:
                self.webhook.send("VMWare DLL Detected", self.name)
                self.event.dispatch("VMWare DLL Detected", self.name)
            if self.exit:
                os._exit(1)

        if os.path.exists(virtualbox_dll):
            self.logger.info("VirtualBox DLL Detected")
            if self.report:
                self.webhook.send("VirtualBox DLL Detected", self.name)
                self.event.dispatch("VirtualBox DLL Detected")
            if self.exit:
                os._exit(1)

    def StartChecks(self) -> None:
        self.CheckVirtualEnv()
        self.CheckRegistry()
        self.CheckMacAddress()
        self.CheckScreenSize()
        self.CheckProcessesAndFiles()
        self.CheckLists()
