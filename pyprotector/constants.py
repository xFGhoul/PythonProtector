import os
import re
import wmi
import uuid
import subprocess

from typing import Final, List, final

from .utils.http import get_ip_address

computer = wmi.WMI()


@final
class UserInfo:
    USERNAME: Final[str] = os.getlogin()
    PC_NAME: Final[str] = os.getenv("COMPUTERNAME")
    IP: Final[str] = get_ip_address()
    HWID: Final[str] = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
    MAC: Final[str] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    GPU: Final[str] = computer.Win32_VideoController()[0].Name
    
@final
class ProtectorInfo:
    VERSION: Final[str] = "1.0"
    ROOT_PATH = os.path.abspath(os.curdir)
    

@final
class EmbedConfig:
    COLOR: Final[str] = "5865F2"
    TITLE: Final[str] = "PythonProtector - 1.0"
    VERSION: Final[str] = "1.0"
    ICON: Final[str] = "https://thereisabotforthat-storage.s3.amazonaws.com/1548526271231_security%20bot%20logo.png"
    
@final
class Lists:
    BLACKLISTED_PROGRAMS: Final[List[str]] = [
            "httpdebuggerui.exe", 
            "wireshark.exe", 
            "HTTPDebuggerSvc.exe", 
            "fiddler.exe", 
            "regedit.exe", 
            "taskmgr.exe", 
            "vboxservice.exe", 
            "df5serv.exe", 
            "processhacker.exe", 
            "vboxtray.exe", 
            "vmtoolsd.exe", 
            "vmwaretray.exe",
            "ida.exe",
            "ida64.exe", 
            "ollydbg.exe",
            "pestudio.exe", 
            "vmwareuser", 
            "vgauthservice.exe", 
            "vmacthlp.exe", 
            "x96dbg.exe", 
            "vmsrvc.exe", 
            "x32dbg.exe", 
            "vmusrvc.exe", 
            "prl_cc.exe", 
            "prl_tools.exe", 
            "xenservice.exe", 
            "qemu-ga.exe", 
            "joeboxcontrol.exe", 
            "ksdumperclient.exe", 
            "ksdumper.exe",
            "joeboxserver.exe"
        ]
    BLACKLISTED_DLLS: Final[List[str]] = [
        "sbiedll.dll",
        "api_log.dll",
        "dir_watch.dll",
        "pstorec.dll",
        "vmcheck.dll",
        "wpespy.dll"
        ]
    VIRTUAL_MACHINE_PROCESSES: Final[List[str]] = [
        "xenservice.exe",
        "VMSrvc.exe",
        "VMUSrvc.exe",
        "VMwareService.exe",
        "VMwareTray.exe",
        "vboxservice.exe",
        "vboxtray.exe",
        "qemu-ga.exe",
        "vdagent.exe",
        "vdservice.exe"
    ]
    BLACKLISTED_WINDOW_NAMES: Final[List[str]] = [
        "IDA: Quick start",
        "VBoxTrayToolWndClass",
        "VBoxTrayToolWnd",
        
        
    ]
    