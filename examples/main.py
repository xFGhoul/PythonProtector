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
    Path.home() / "AppData/Roaming/PythonProtector/logs/[Security]-{time:D-M-YY}.log"
)  # -- This can be renamed

# -- Construct Class
security = PythonProtector(debug=True, modules=["AntiProcess", "AntiVM", "Miscellaneous"], logs_path=LOGGING_PATH, webhook_url="", should_exit=True)

# -- Main Code
if __name__ == "__main__":
    SecurityThread = Thread(
        name="Python Protector", target=security.start
    )  # -- Start Before Any Other Code Is Run
    SecurityThread.start()
    # Other Code
