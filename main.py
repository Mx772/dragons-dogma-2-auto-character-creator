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
    app.schedule_log(f"Going from {current_value} to {target_value} for {attribute_name}")
    app.update()

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
        self.geometry("600x400")

        self.default_file = tk.StringVar()
        self.target_file = tk.StringVar()
        self.log_messages = tk.StringVar()
        self.log_messages.set("")

        frame = tk.Frame(self)
        frame.pack(pady=20)

        default_label = tk.Label(frame, text="Default Config:")
        default_label.grid(row=0, column=0)

        # Add buttons for selecting the default config file
        human_male_button = tk.Button(frame, text="Human Male", command=lambda: self.set_default_file(r"defaults\human_male.ini"))
        human_male_button.grid(row=0, column=1, padx=5)

        human_female_button = tk.Button(frame, text="Human Female", command=lambda: self.set_default_file(r"defaults\human_female.ini"))
        human_female_button.grid(row=0, column=2, padx=5)

        beastren_male_button = tk.Button(frame, text="Beastren Male", command=lambda: self.set_default_file(r"defaults\beastren_male.ini"))
        beastren_male_button.grid(row=0, column=3, padx=5)

        beastren_female_button = tk.Button(frame, text="Beastren Female", command=lambda: self.set_default_file(r"defaults\beastren_female.ini"))
        beastren_female_button.grid(row=0, column=4, padx=5)

        target_label = tk.Label(frame, text="Target Config:")
        target_label.grid(row=1, column=0)
        target_entry = tk.Entry(frame, textvariable=self.target_file)
        target_entry.grid(row=1, column=1)
        target_button = tk.Button(frame, text="Browse", command=self.select_target_file)
        target_button.grid(row=1, column=2)
        
        console_frame = tk.Frame(self)
        console_frame.pack(fill="both", expand=True)

        console_label = tk.Label(console_frame, text="Log Messages:")
        console_label.pack(side="top", fill="x")

        self.console_text = tk.Text(console_frame, wrap="word", height=10)
        self.console_text.pack(side="top", fill="both", expand=True)
        self.console_text.configure(state="disabled")

        run_button = tk.Button(self, text="Run", command=self.run_program)
        run_button.pack(pady=10)

    def set_default_file(self, file_path):
        self.default_file.set(file_path)

    def select_target_file(self):
        file_path = filedialog.askopenfilename(title="Select Target File")
        self.target_file.set(file_path)

    def log(self, message):
        current_log = self.log_messages.get()
        self.log_messages.set(current_log + message + "\n")
        self.console_text.configure(state="normal")
        self.console_text.insert("end", message + "\n")
        self.console_text.configure(state="disabled")
        self.console_text.see("end")

    def schedule_log(self, message):
        self.after(0, self.log, message)
        
    def run_program(self):
        default_file = self.default_file.get()
        target_file = self.target_file.get()

        if default_file and target_file:
            # Call your main function with the selected files
            main(default_file, target_file)
        else:
            print("Please select both files.")

def main(default_file: str, target_file: str) -> None:
    """
    Main function to adjust character attributes based on configuration files.
    """
    default_attributes = read_config(default_file)
    target_attributes = read_config(target_file)

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
        adjust_slider(attributes[attribute_name], target_attributes[attribute_name], attribute_name, sleep_time)
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

    app.schedule_log("Character creation complete!")

if __name__ == "__main__":
    app = App()
    app.mainloop()