"""
	____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
	   /____/

Made With ❤️ By Ghoul & Marci
"""

from pathlib import Path
from threading import Thread

from pyprotector import PythonProtector
from pyprotector.keyauth import Keyauth
from pyprotector.keyauth.utils import getchecksum

# -- Define Constants
LOGGING_PATH = (
    Path.home() / "AppData/Roaming/PythonProtector/logs/[Security].log"
)  # -- This can be any path

# -- Construct Class
security = PythonProtector(
    debug=True,
    modules=[
        "AntiProcess",
        "AntiVM",
        "Miscellaneous",
        "AntiDLL",
        "AntiAnalysis",
        "AntiDump",
    ],
    logs_path=LOGGING_PATH,
    webhook_url="",
    on_detect=["Report", "Exit", "Screenshot"],
)

auth = Keyauth(
    name="",
    ownerid="",
    secret="",
    version="",
    file_hash=getchecksum())

# -- Example Event


@security.event.obs.on("process_running")
def on_process_running(text: str, module: str, process):
    print(f"{module} - {text}\nProcess Name: {process.name()}")
    print(security.user)
    auth.ban()
    # Free To Do Whatever You Want Here...


# -- Main Code
if __name__ == "__main__":
    SecurityThread = Thread(
        name="Python Protector", target=security.start
    )  # -- Start Before Any Other Code Is Run
    SecurityThread.start()
    auth.initialize()
    # Other Code
