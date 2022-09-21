from distutils.core import setup

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name="PythonProtector",  
    packages=["pyprotector"],  
    version="1.0",  #
    license="MIT",  
    description="Library for protecting your python files",  
    author="Ghoul & Macri",
    url="https://github.com/xFGhoul/PythonProtecttor",  
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    keywords=["keyauth", "protection", "protect", "obfuscate", "WMI"],  
    install_requires=["humanize", "loguru", "discord-webhook", "py-cpuinfo", "command_runner", "psutil", "httpx", "WMI", "pywin32"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3", 
        "Programming Language :: Python :: 3.10",
    ],
)