from pyprotector import PythonProtector

from pathlib import Path
from threading import Thread

# -- Define Constants
LOGGING_PATH = (
    Path.home() / "AppData/Roaming/PythonProtector/logs/[Security]-{time:D-M-YY}.log"
)  # -- This can be renamed

# -- Construct Class
security = PythonProtector(debug=True, logs_path=LOGGING_PATH, webhook_url="")

# -- Main Code
if __name__ == "__main__":
    SecurityThread = Thread(
        name="Python Protector", target=security.start
    )  # -- Start Before Any Other Code Is Run
    SecurityThread.start()
    # Other Code
