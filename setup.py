import sys
from cx_Freeze import setup, Executable

packages = ["win32gui"]

build_exe_options = {
    "excludes": ["http", "html", "unittest", "urllib", "test", "email",],
    "include_files": ["defaults", "templates"],
    "optimize": 0,
    "include_msvcr": True,
    "no_compress": True,
    "packages" :packages,
}

executables = [
    Executable(
        "main.py",
        copyright="Copyright (C) 2024 Mx772",
        shortcut_name="DD2AutoSlider",
        shortcut_dir="DD2AutoSlider",
        target_name="DD2AutoSlider",
    )
]

setup(
    name="DD2AutoSlider",
    version="0.0.3",
    description="AutoSlider for DD2 Character Creation",
    options={"build_exe": build_exe_options},
    executables=executables,
)