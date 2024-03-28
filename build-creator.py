import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "excludes": ["http", "html", "unittest", "urllib", "test", "email",],
    "include_files": ["defaults", "templates"],
    "optimize": 0,
    "include_msvcr": True,
    "no_compress": True,
    "build_exe": "build/DD2AutoSlider-Creator"
}

executables = [
    Executable(
        "creator/creator.py",
        copyright="Copyright (C) 2024 Mx772",
        shortcut_name="DD2AutoSlider-Creator",
        shortcut_dir="DD2AutoSlider-Creator",
        target_name="DD2AutoSlider-Creator",
    )
]

setup(
    name="DD2AutoSlider-Creator",
    version="0.0.1",
    description="AutoSlider Creator for DD2 Character Creation",
    options={"build_exe": build_exe_options},
    executables=executables,
)