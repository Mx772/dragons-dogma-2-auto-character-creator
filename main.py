import tkinter as tk
from tkinter import filedialog
import win32gui
import configparser
import time
from typing import Dict, List
from typing import Union
import os

# CONFIG
debug = False

from directkeys import PressKey, ReleaseKey, D, A, S, ESC, SP, E

def read_config(config_file: str) -> tuple[Dict[str, str], Dict[str, Dict[str, int]]]:
    """
    Read a configuration file and return a dictionary of key-value pairs, grouped by sections.
    The '[Info]' section is handled separately with string values.

    Args:
        config_file (str): The path to the configuration file.

    Returns:
        Dict[str, Dict[str, Union[int, str]]]: A dictionary where the keys are section names,
            and the values are dictionaries containing the key-value pairs for that section.
            The '[Info]' section is a separate dictionary with string values.
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    info_section = {}
    attributes_section = {}

    for section in config.sections():
        if section == 'Info':
            info_section = {key: value for key, value in config[section].items()}
        else:
            attributes_section[section] = {
                key: int(value) if value else -200
                for key, value in config[section].items()
            }

    return info_section, attributes_section

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
        self.geometry("1000x800")

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
        
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Create a frame for the photo box
        photo_frame = tk.Frame(main_frame)
        photo_frame.pack(side="left", fill="both", expand=True)
        
        # Create a label for the photo box
        photo_label = tk.Label(photo_frame, text="Target:")
        photo_label.pack(side="top", fill="x")

        # Create a canvas to display the photo
        self.photo_canvas = tk.Canvas(photo_frame, width=400, height=400)
        self.photo_canvas.pack(fill="both", expand=True)

        # Load and display the default photo
        default_photo_path = os.path.join("templates", "photos", "default.png")
        self.load_photo(default_photo_path)

        # Create a frame for the log box
        console_frame = tk.Frame(main_frame)
        console_frame.pack(side="left", fill="both", expand=True)

        console_label = tk.Label(console_frame, text="Log Messages:")
        console_label.pack(side="top", fill="x")

        self.console_text = tk.Text(console_frame, wrap="word", height=10)
        self.console_text.pack(side="top", fill="both", expand=True)
        self.console_text.configure(state="disabled")

        # Bind the target_file variable to a function that updates the photo
        self.target_file.trace("w", self.update_photo)

        run_button = tk.Button(self, text="Run", command=self.run_program)
        run_button.pack(pady=10)


    def load_photo(self, photo_path):
        if os.path.exists(photo_path):
            self.photo_image = tk.PhotoImage(file=photo_path)
            self.photo_canvas.create_image(0, 0, anchor="nw", image=self.photo_image)
        else:
            app.schedule_log(f"Could not find photo in {photo_path}")

    def update_photo(self, *args):
        target_file = self.target_file.get()
        if target_file:
            photo_filename = os.path.splitext(os.path.basename(target_file))[0] + ".png"
            photo_path = os.path.join("templates", "photos", photo_filename)
            self.load_photo(photo_path)
        else:
            default_photo_path = os.path.join("templates", "photos", "default.png")
            self.load_photo(default_photo_path)
            
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
    _, default_attributes = read_config(default_file)
    info, target_attributes = read_config(target_file)

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
    if dd2_window:
        app.schedule_log(f"Found window for {window_name}!")
    else:
        app.schedule_log(f"Could not find game window {window_name} - If you are using the 'Character Creator' make sure to click the toggle!")
        
    window_set_foreground(dd2_window)
    app.schedule_log(f"Please highlight 'Body > Body > Height and do not move the mouse!")
    app.schedule_log(f"Waiting for 3 seconds...")
    app.schedule_log(f"To stop the app, close the Console window!")
    time.sleep(3)

    processed_attributes = 0
    processed_categories = 0
    processed_pages = 0
    
    for section_name, section_attributes in default_attributes.items():
        page_name = f"page_{processed_pages + 1}"
        
        if section_name in target_attributes:
            target_section = target_attributes[section_name]
        else:
            app.schedule_log(f"Could not find section '{section_name}' in target attribute file.")
            continue
        
        attribute_list = list(section_attributes.keys())  
        for i, attribute_name in enumerate(attribute_list):
            if attribute_name in target_section:
                target_value = target_section[attribute_name]
              
                # If it's not '-200' which is set by config-reader to an arbitrarily low number which means it wasn't set. 
                if target_value == -200:
                    app.schedule_log(f"Could not find a value for {attribute_name} in target attribute file, using default of {attributes[section_name][attribute_name]}!")
                    
                elif 'edit' in attribute_name:
                    # If the attribute is a toggle
                    if target_value == 1:
                        
                        # If target config has enabled a secondary
                        app.schedule_log(f"Enabling secondary section for {attribute_name}")
                        PressKey(SP)
                        time.sleep(sleep_time)
                        ReleaseKey(SP)
                        time.sleep(sleep_time)
                        print(f'Adding addl fields: {pages[page_name][processed_categories]} += {pages[page_name][processed_categories]-1}')
                        pages[page_name][processed_categories] += pages[page_name][processed_categories]-1
                else:
                    
                    # If hell - If it's a preset value, skip it since it makes no difference
                    if 'preset' not in attribute_name:
                        adjust_slider(attributes[section_name][attribute_name], target_value, attribute_name, sleep_time)
                        attributes[section_name] = update_dependent_attributes(attribute_name, target_value, attributes[section_name])
                    else:
                        app.schedule_log(f"Skipping preset for {attribute_name} so it doesn't change values!")
            else:
                app.schedule_log(f"Could not find {attribute_name} in target attribute file, using default of {attributes[section_name][attribute_name]}!")
                
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