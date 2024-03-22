# Dragons Dogma II Auto Character Creator
An automated Python script for creating and customizing characters in Dragon's Dogma 2. 

This python script takes two ini files. 
`default.ini` which is the default woman preset and `character_config.ini` which is the desired presets. 
(TODO: Male/Other Races) 

The script then goes through each page simulating key presses to set the 'default' character to the desired. 

## Installation
As all modules are python-native, it should run without any installation. 
Will require Python to be installed, tested working on `Python 3.10.11`.

Will likely require Windows, untested on other OS.

## Usage

`git clone https://github.com/Mx772/dragons-dogma-2-auto-character-creator.git`

Open the directory and run:
`python main.py`

I have it set to a `2` second delay, after running, select the first section of the character creator.


## Preview

https://github.com/Mx772/dragons-dogma-2-auto-character-creator/assets/9059161/dc098fe9-3587-4bb8-87ae-cb40c875dc1d


## TODO

- Male + Other Races
- Tattoos
- Complex sliders (Where one slider causes others to move)
- Simple GUI

## FAQ

> Does it support xyz os?

I only have windows, if it works on another OS or Python version, let me know via opening an issue and I will update the readme.

> Why do you have a default profile vs reading the screen?

I wanted to be able to support different languages/resolutions/colors by default.

> I found a bug!

Open an issue please!

> How can I make a template?

Copy `character_config.ini` and edit the values as needed. 

> What is the current `character_config.ini` based on?

[This post on reddit](https://www.reddit.com/r/fashiondogma/comments/1bgyw62/asian_girl/). It was on the front page and had photos of sliders. With photos, you can auto read the values in some programs which was easier than manually doing it. 

## Credits
directkeys.py logic via stackoverflow user `user573949` - [Post](http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game)
