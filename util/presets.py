import os
import configparser

# Set the directory where the .ini files are located
templates_dir = 'templates'

# Create a list to store the formatted strings
formatted_strings = []

# Loop through all the .ini files in the templates directory
for filename in os.listdir(templates_dir):
    if filename.endswith('.ini'):
        # Create a ConfigParser object and read the .ini file
        config = configparser.ConfigParser()
        config.read(os.path.join(templates_dir, filename))

        # Extract the name, author, and source from the [info] section
        name = config.get('info', 'name').strip('"')
        author_url = config.get('info', 'author').strip('"')
        source_url = config.get('info', 'source').strip('"')

        # Extract the author name from the URL
        author = author_url.split('/')[-1]

        # Format the string with a link for the author
        formatted_string = f"- {name} by [{author}]({source_url})"
        formatted_strings.append(formatted_string)

# Write the formatted strings to a file named templates.md
with open('templates/templates.md', 'w') as f:
    for formatted_string in formatted_strings:
        f.write(formatted_string + '\n')
