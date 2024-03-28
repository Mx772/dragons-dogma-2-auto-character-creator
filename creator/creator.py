import configparser
import os

# Ask for race and gender
print("Select your race and gender:")
print("1. Human Male")
print("2. Human Female")
print("3. Beastren Male")
print("4. Beastren Female")
choice = input("Enter your choice (1-4): ")

# Set the default file based on the choice
if choice == "1":
    default_file = "defaults/human_male.ini"
elif choice == "2":
    default_file = "defaults/human_female.ini"
elif choice == "3":
    default_file = "defaults/beastren_male.ini"
elif choice == "4":
    default_file = "defaults/beastren_female.ini"
else:
    print("Invalid choice. Exiting.")
    exit()

# Read the default file into a ConfigParser object
config = configparser.ConfigParser(allow_no_value=True)
config.read(default_file)

# Iterate over sections and options
for section in config.sections():
    print(f"\nSection: {section}")
    skip_section = input(f"Skip this section? (y/n) ").lower() == "y"
    if skip_section:
        continue

    skip_remaining = False
    for option in config.options(section):
        default_value = config.get(section, option)
        if section == "info":
            new_value = input(f"What is the value for {option} (default: {default_value})? ")
            if new_value:
                config.set(section, option, new_value)
        else:
            while True:
                new_value = input(f"What is the value for {option} (default: {default_value})? ")
                if new_value.lower() == "skip":
                    skip_remaining = True
                    break
                if new_value == "":
                    break
                try:
                    new_value = int(new_value)
                    config.set(section, option, str(new_value))
                    break
                except ValueError:
                    print("Invalid input. Please enter an integer.")
        if skip_remaining:
            break

    if skip_remaining:
        break

# Get the name from the [info] section
output_file = f"{config.get('info', 'name')}.ini"

# Write the updated config to the output file
with open(output_file, "w") as configfile:
    config.write(configfile)

print(f"\nNew .ini file saved as {output_file}")