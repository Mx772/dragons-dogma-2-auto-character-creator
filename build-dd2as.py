# Test
import sys
from cx_Freeze import setup, Executable

sys.path.append('src')

packages = ["win32gui", "src"]

build_exe_options = {
    "excludes": ["http", "html", "unittest", "urllib", "test", "email",],
    "include_files": ["defaults", "templates"],
    "optimize": 0,
    "include_msvcr": True,
    "no_compress": True,
    "packages" :packages,
    "build_exe": "build/DD2AutoSlider"
}

executables = [
    Executable(
        "src/main.py",
        copyright="Copyright (C) 2024 Mx772",
        shortcut_name="DD2AutoSlider",
        shortcut_dir="DD2AutoSlider",
        target_name="DD2AutoSlider",
    )
]

setup(
    name="DD2AutoSlider",
    description="AutoSlider for DD2 Character Creation",
    options={"build_exe": build_exe_options},
    executables=executables,
)
