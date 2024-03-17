import os
import subprocess
from pathlib import Path
import nicegui
import sys

import PyInstaller.__main__


def buildApp():
    PyInstaller.__main__.run(
        [
            "{}/app.py".format(Path(__file__).parent),
            "--name",
            "myapp",
            "--onefile",
            "--add-data",
            f"{Path(nicegui.__file__).parent}{os.pathsep}nicegui",
        ]
    )


if __name__ == "__main__":
    buildApp()
