import tkinter as tk
from tkinter import filedialog
import win32gui
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

def window_set_foreground(window_handle):
    """
    Set the specified window to the foreground.

    Args:
        window_handle (int): The handle of the window to set to the foreground.

    Returns:
        None
    """
    win32gui.SetForegroundWindow(window_handle)

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

attribute_dependencies = {
    "arm_size": ["upper_arm_thickness", "forearm_thickness"],
    "leg_size": ["thigh_size", "calf_size"],
    "brow_depth_overall": ["brow_depth_inner", "brow_depth_outer"],
    "bridge_bump_overall": ["bridge_bump_upper", "bridge_bump_lower"],
    "cheek_thickness": ["cheek_bulge", "neck_fat"],
    "body_tattoo_overall_scale": ["body_tattoo_vert_scale", "body_tattoo_horz_scale"],
    "right_arm_overall_scale": ["right_arm_vert_scale", "right_arm_horz_scale"],
    "left_arm_overall_scale": ["left_arm_vert_scale", "left_arm_horz_scale"],
    "right_leg_overall_scale": ["right_leg_vert_scale", "right_leg_horz_scale"],
    "left_leg_overall_scale": ["left_leg_vert_scale", "left_leg_horz_scale"],
    "body_scar_overall_scale": ["body_scar_vert_scale", "body_scar_horz_scale"],
    "right_arm_scar_overall_scale": ["right_arm_scar_horz_scale", "right_arm_scar_vert_scale"],
    "left_arm_scar_overall_scale": ["left_arm_scar_horz_scale", "left_arm_scar_vert_scale"],
    "right_leg_scar_overall_scale": ["right_leg_scar_horz_scale", "right_leg_scar_vert_scale"],
    "left_leg_scar_overall_scale": ["left_leg_scar_horz_scale", "left_leg_scar_vert_scale"],
}
   
def update_dependent_attributes(primary_attribute: str, new_value: int, attributes: dict) -> dict:
    """
    Update the dependent attributes based on the primary attribute's new value.

    Args:
        primary_attribute (str): The name of the primary attribute that was changed.
        new_value (int): The new value of the primary attribute.
        attributes (dict): The dictionary containing the attribute values.

    Returns:
        dict: The updated dictionary with the dependent attributes' values changed.
    """
    print(f"{primary_attribute}, {new_value}")
    updated_attributes = attributes.copy()
    if primary_attribute in attribute_dependencies:
        print(f"found {primary_attribute}")
        dependent_attributes = attribute_dependencies[primary_attribute]
        print(f"{dependent_attributes}")
        primary_old_value = attributes[primary_attribute]
        primary_value_change = new_value - primary_old_value

        for dependent_attribute in dependent_attributes:
            old_value = attributes[dependent_attribute]
            updated_value = old_value + primary_value_change
            print(f"Updating {dependent_attribute} from {old_value} to {updated_value}")
            updated_attributes[dependent_attribute] = updated_value

    return updated_attributes

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
        self.title("DD2 Auto Slider")
        self.geometry("600x400")

        self.window_name_var = tk.StringVar(value="Dragon's Dogma 2")
        self.default_file = tk.StringVar()
        self.target_file = tk.StringVar()
        self.log_messages = tk.StringVar()
        self.selected_default = tk.StringVar()
        self.log_messages.set("")

        frame = tk.Frame(self)
        frame.pack(pady=20)

        default_label = tk.Label(frame, text="Default Config:")
        default_label.grid(row=0, column=0)

        # Add buttons for selecting the default config file
        human_male_button = tk.Button(frame, text="Human Male", wraplength=100, command=lambda: self.set_default_file(r"defaults\human_male.ini", human_male_button))
        human_male_button.grid(row=0, column=1, padx=2, sticky="ew")

        human_female_button = tk.Button(frame, text="Human Female", wraplength=100, command=lambda: self.set_default_file(r"defaults\human_female.ini", human_female_button))
        human_female_button.grid(row=0, column=2, padx=2, sticky="ew")

        beastren_male_button = tk.Button(frame, text="Beastren Male", wraplength=100, command=lambda: self.set_default_file(r"defaults\beastren_male.ini", beastren_male_button))
        beastren_male_button.grid(row=0, column=3, padx=2, sticky="ew")

        beastren_female_button = tk.Button(frame, text="Beastren Female", wraplength=100, command=lambda: self.set_default_file(r"defaults\beastren_female.ini", beastren_female_button))
        beastren_female_button.grid(row=0, column=4, padx=2, sticky="ew")

        target_label = tk.Label(frame, text="Target Config:")
        target_label.grid(row=1, column=0)
        target_entry = tk.Entry(frame, textvariable=self.target_file)
        target_entry.grid(row=1, column=1)
        target_button = tk.Button(frame, text="Browse", command=self.select_target_file)
        target_button.grid(row=1, column=2)
        
        # Create a label for the toggle box
        toggle_label = tk.Label(frame, text="DD2 CC")
        toggle_label.grid(row=1, column=3)

        # Create a checkbox for toggling the window name
        self.toggle_checkbox = tk.Checkbutton(frame, text="", variable=self.window_name_var, onvalue="Character Creator & Storage", offvalue="Dragon's Dogma 2")
        self.toggle_checkbox.grid(row=1, column=4)
        
        console_frame = tk.Frame(self)
        console_frame.pack(fill="both", expand=True)

        console_label = tk.Label(console_frame, text="Log Messages:")
        console_label.pack(side="top", fill="x")

        self.console_text = tk.Text(console_frame, wrap="word", height=10)
        self.console_text.pack(side="top", fill="both", expand=True)
        self.console_text.configure(state="disabled")

        run_button = tk.Button(self, text="Run", command=self.run_program)
        run_button.pack(pady=10)

    def set_default_file(self, file_path, button):
        previous_button = self.nametowidget(self.selected_default.get())
        if previous_button:
            previous_button.configure(relief="raised")

        self.default_file.set(file_path)
        self.selected_default.set(str(button))
        button.configure(relief="sunken")

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
        window_name = self.window_name_var.get()

        if default_file and target_file:
            # Call your main function with the selected files
            main(default_file, target_file, window_name)
        else:
            print("Please select both files.")

def main(default_file: str, target_file: str, window_name: str) -> None:
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
        "page_5": [1, 17, 17, 17, 17, 17, 1, 13, 13, 13, 13, 13, 4],
    }

    attributes = default_attributes.copy()
    sleep_time = 0.02

    def next_page() -> None:
        """Go to the next page by simulating key presses."""
        simulate_key_press([ESC, E, SP])

    def change_category() -> None:
        """Change to the next category by simulating key presses."""
        simulate_key_press([ESC, S, SP])

    dd2_window = win32gui.FindWindow(None, window_name)
    window_set_foreground(dd2_window)
    time.sleep(2)

    processed_attributes = 0
    processed_categories = 0
    processed_pages = 0
    
    for i, attribute_name in enumerate(attributes):
        page_name = f"page_{processed_pages + 1}"
        adjust_slider(attributes[attribute_name], target_attributes[attribute_name], attribute_name, sleep_time)
        attributes = update_dependent_attributes(attribute_name, target_attributes[attribute_name], attributes)
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