import tkinter as tk
from tkinter import filedialog
import configparser
import time
from typing import Dict, List

# CONFIG
debug = False

from directkeys import PressKey, ReleaseKey, D, A, S, ESC, SP, E

def read_config(config_file: str) -> Dict[str, int]:
    """
    Read a configuration file and return a dictionary of key-value pairs.

    Args:
        config_file (str): The path to the configuration file.

    Returns:
        Dict[str, int]: A dictionary containing the configuration key-value pairs.
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    return {key: int(value) for key, value in config['Character'].items()}

def simulate_key_press(keys: List[str], sleep_time: float = 0.02) -> None:
    """
    Simulate pressing and releasing a sequence of keys.

    Args:
        keys (List[str]): A list of key codes to simulate.
        sleep_time (float, optional): The time to sleep between key presses in seconds. Defaults to 0.02.
    """
    for key in keys:
        PressKey(key)
        time.sleep(sleep_time)
        ReleaseKey(key)
        time.sleep(sleep_time)

def adjust_slider(current_value: int, target_value: int, attribute_name: str, sleep_time: float = 0.02) -> None:
    """
    Adjust a slider by simulating key presses.

    Args:
        current_value (int): The current value of the slider.
        target_value (int): The desired value of the slider.
        attribute_name (str): The name of the attribute being adjusted.
        sleep_time (float, optional): The time to sleep between key presses in seconds. Defaults to 0.02.
    """
    print(f"Going from {current_value} to {target_value} for {attribute_name}")

    if current_value < target_value:
        for _ in range(target_value - current_value):
            PressKey(D)
            time.sleep(sleep_time)
            ReleaseKey(D)
            time.sleep(sleep_time)
    else:
        for _ in range(current_value - target_value):
            PressKey(A)
            time.sleep(sleep_time)
            ReleaseKey(A)
            time.sleep(sleep_time)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Character Creator")
        self.geometry("400x200")

        self.default_file = tk.StringVar()
        self.config_file = tk.StringVar()

        frame = tk.Frame(self)
        frame.pack(pady=20)

        default_label = tk.Label(frame, text="Default file:")
        default_label.grid(row=0, column=0)
        default_entry = tk.Entry(frame, textvariable=self.default_file)
        default_entry.grid(row=0, column=1)
        default_button = tk.Button(frame, text="Browse", command=self.select_default_file)
        default_button.grid(row=0, column=2)

        config_label = tk.Label(frame, text="Config file:")
        config_label.grid(row=1, column=0)
        config_entry = tk.Entry(frame, textvariable=self.config_file)
        config_entry.grid(row=1, column=1)
        config_button = tk.Button(frame, text="Browse", command=self.select_config_file)
        config_button.grid(row=1, column=2)

        run_button = tk.Button(self, text="Run", command=self.run_program)
        run_button.pack(pady=10)

    def select_default_file(self):
        file_path = filedialog.askopenfilename(title="Select Default File")
        self.default_file.set(file_path)

    def select_config_file(self):
        file_path = filedialog.askopenfilename(title="Select Config File")
        self.config_file.set(file_path)

    def run_program(self):
        default_file = self.default_file.get()
        config_file = self.config_file.get()

        if default_file and config_file:
            # Call your main function with the selected files
            main(default_file, config_file)
        else:
            print("Please select both files.")


def main(default_file: str, config_file: str) -> None:
    """
    Main function to adjust character attributes based on configuration files.
    """
    default_attributes = read_config(default_file)
    config_attributes = read_config(config_file)

    pages = {
        "page_1": [9, 7, 12, 6, 4],
        "page_2": [1, 4, 7, 9, 12, 7, 6, 6, 8],
        "page_3": [6, 3],
        "page_4": [9, 6, 8, 6, 3, 5, 6, 3],
    }

    attributes = default_attributes.copy()
    sleep_time = 0.02

    def next_page() -> None:
        """Go to the next page by simulating key presses."""
        simulate_key_press([ESC, E, SP])

    def change_category() -> None:
        """Change to the next category by simulating key presses."""
        simulate_key_press([ESC, S, SP])

    time.sleep(2)

    processed_attributes = 0
    processed_categories = 0
    processed_pages = 0

    for i, attribute_name in enumerate(attributes):
        page_name = f"page_{processed_pages + 1}"
        adjust_slider(attributes[attribute_name], config_attributes[attribute_name], attribute_name, sleep_time)
        processed_attributes += 1

        if debug:
            print(f"Performing Checks for:\n{processed_attributes} == {pages[page_name][processed_categories]}\n{processed_categories + 1} == {len(pages[page_name])}\ni: {i}\n attribute_name: {attribute_name}")

        if processed_attributes == pages[page_name][processed_categories]:
            if processed_categories + 1 == len(pages[page_name]):
                processed_attributes = 0
                processed_categories = 0
                processed_pages += 1
                next_page()
                continue
            else:
                processed_categories += 1
                processed_attributes = 0
                change_category()
                continue

        if i < len(attributes) - 1:
            simulate_key_press([S], sleep_time)

    print("Character creation complete!")

if __name__ == "__main__":
    app = App()
    app.mainloop()