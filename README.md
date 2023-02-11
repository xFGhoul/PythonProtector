# PythonProtector

![pyprotector](https://cdn.discordapp.com/attachments/1019356864548446269/1066498438386176102/image.png)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

A modern, easy to use and feature-rich way to protect your Python Programs.

## Features

- Completely Configurable Module System 
- Completely Configurable On Detection System
- Encrypted Logging System With Remote Uploading
- Discord Webhook Support
- Clean, Optimized Code
- Constant Updates

## Installation

**Python 3.11 or higher is required**

Install The PyPi Version:

```sh
py -3 -m pip install -U PythonProtector
```

You may also install the development version:
```sh
pip install git+https://github.com/xFGhoul/PythonProtector.git
```

## Usage

Quick Example:
```py
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
        "AntiAnalysis",
        "AntiDump"],
    logs_path=LOGGING_PATH,
    webhook_url="",
    on_detect=[
        "Report",
        "Exit",
        "Screenshot"],
)

# -- Main Code
if __name__ == "__main__":
    SecurityThread = Thread(
        name="Python Protector", target=security.start
    )  # -- Start Before Any Other Code Is Run
    SecurityThread.start()
    # Other Code
```

You can find more examples in the [examples](https://github.com/xFGhoul/PythonProtector/blob/dev/examples/) directory.

## Files and Explanations

`├──`[`.github`](https://github.com/xFGhoul/PythonProtector/blob/dev/.github) — GitHub configuration including CI/CD workflows<br>
`├──`[`.vscode`](https://github.com/xFGhoul/PythonProtector/blob/dev/.vscode) — VSCode Related Settings<br>
`├──`[`data`](https://github.com/xFGhoul/PythonProtector/blob/dev/data) — Data Files Needed By PythonProtector<br>
`├──`[`examples`](https://github.com/xFGhoul/PythonProtector/blob/dev/examples) — Examples Showing How To Use PythonProtector<br>
`├──`[`pyprotector`](https://github.com/xFGhoul/PythonProtector/blob/dev/pyprotector) — Source Code Of PythonProtector<br>
`├──`[`scripts`](https://github.com/xFGhoul/PythonProtector/blob/dev/scripts) — Scripts Used In The Development Process<br>

## Links

- [Documentation](http://ghouldev.me/PythonProtector/)
- [Official Discord Server](https://discord.gg/yMu9qjdrmp)

> Made With ❤️ By `ghoul#1337` and `Marci#0101`