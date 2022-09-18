from pyprotector import PythonProtector

from pathlib import Path

# -- Define Constants
LOGGING_PATH = Path.home() / "AppData/Roaming/PythonProtector/logs/[Security]-{time:D-M-YY}.log" # -- This can be renamed

security = PythonProtector(debug=True, logs_path=LOGGING_PATH, webhook_url="")

if __name__ == "__main__":
    security.start() # -- Start Before Any Other Code Is Run 
    # Other Code