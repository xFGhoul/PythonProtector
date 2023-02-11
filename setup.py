"""
	____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
	   /____/

Made With ❤️ By Ghoul & Marci
"""

from setuptools import setup

with open("README.md", encoding="utf8") as readme_file:
    README = readme_file.read()

with open("HISTORY.md") as history_file:
    HISTORY = history_file.read()

setup(
    name="PythonProtector",
    packages=["pyprotector", "pyprotector.utils", "pyprotector.modules"],
    version="1.8",
    license="MIT",
    description="Library for protecting your python files",
    author="Ghoul & Marci",
    url="https://github.com/xFGhoul/PythonProtecttor",
    long_description_content_type="text/markdown",
    long_description=README + "\n\n" + HISTORY,
    python_requires=">=3.11",
    project_urls={
        "Homepage": "http://ghouldev.me/PythonProtector/",
        "Source": "https://github.com/xFGhoul/PythonProtector",
    },
    keywords=[
        "keyauth",
        "protection",
        "protect",
        "obfuscate",
        "obfuscation",
        "WMI",
        "windows",
    ],
    install_requires=[
        "humanize",
        "loguru",
        "discord-webhook",
        "py-cpuinfo",
        "command_runner",
        "psutil",
        "httpx",
        "WMI",
        "pywin32",
        "Pillow",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: Windows",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
)
