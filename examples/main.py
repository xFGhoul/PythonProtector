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
        "AntiAnalysis"],
    logs_path=LOGGING_PATH,
    webhook_url="",
    on_detect=[
        "Report",
        "Exit",
        "Screenshot"],
)

# -- Example Event


@security.event.obs.on(
    "pyprotector_detect"
)  # Only Event, Anything Other Than This Will Error.
def on_detection(text: str, module: str):
    print(f"{module} - {text}")
    # Free To Do Whatever You Want Here...


# -- Main Code
if __name__ == "__main__":
    SecurityThread = Thread(
        name="Python Protector", target=security.start
    )  # -- Start Before Any Other Code Is Run
    SecurityThread.start()
    # Other Code
