# Dragons Dogma II Auto Character Creator
An automated Python script for creating and customizing characters in Dragon's Dogma 2. 

This python script takes two ini files. 
A default profile which is used to find the original value, and a target profile which is the desired presets. 
(TODO: Default Other Races) 

The script then goes through each page simulating key presses to set the 'default' character to the desired. 

## Installation
As all modules are python-native, it should run without any installation. 
Will require Python to be installed, tested working on `Python 3.10.11`.

Will likely require Windows, untested on other OS.

## Preset Creation

As of v0.0.9, a new .exe and python script is included named `DD2AutoSlider-Creator`. 

It is a commandline script to help you create new presets!

You select the base/default, then can enter for each section. 
If you wish to skip the rest of the tool, type 'skip' in a field where it expects a number (So an attribute, not asking if you want to skip a section)

If you want to add a preset to the templates folder, please open an issue and use the 'template/preset' option OR for pull/code credit, open a Pull Request with it! 

## Usage

Via Git:

`git clone https://github.com/Mx772/dragons-dogma-2-auto-character-creator.git`

Via Github:

Download the release .zip [here](https://github.com/octo-org/octo-repo/releases/latest) and unzip it.

Open the directory and run:
```
python -m pip install -r requirements.txt
python main.py
```
**OR**
Run the .exe on windows.

This will pop up a GUI for you to select the `default` and `target` ini file you wish to use. 

(Defaults found in the /default directory, example woman in /templates directory)

If you are using the Character Creator vs the game, toggle the box in the upper right. 

I have it set to a `3` second delay, after pressing 'run', setup your game like the screenshot below (Cursor far left, hover on 'body' category)

<details>
<summary>Starting Screenshot</summary>

![image](https://github.com/Mx772/dragons-dogma-2-auto-character-creator/assets/9059161/637c021c-92bc-4179-b764-c5184bc021f6)


</details>


> What is the 'default' profile?


<details>
<summary>Default Woman</summary>

![defaultGif](https://github.com/Mx772/dragons-dogma-2-auto-character-creator/assets/9059161/bb7f280d-721a-4740-ac93-894916a8ab34)

</details>

<details>
<summary>Default Man</summary>

![male_default](https://github.com/Mx772/dragons-dogma-2-auto-character-creator/assets/9059161/e6811a84-5026-4c51-b06b-f4ae4d3230ea)

</details>



## Preview

![gitGif](https://github.com/Mx772/dragons-dogma-2-auto-character-creator/assets/9059161/beb9b701-8a2d-4447-be86-f9e8a387a5a2)



## TODO

- Fix Images
- Allow config of speed

## FAQ

> Does it support xyz os?

I only have windows, if it works on another OS or Python version, let me know via opening an issue and I will update the readme.

> Why do you have a default profile vs reading the screen?

I wanted to be able to support different languages/resolutions/colors by default.

> I found a bug!

Open an issue please!

> How can I make a template?

Copy the .ini file for the given sex and edit the values as needed. 

> What is the current template based on?

[This post on reddit](https://www.reddit.com/r/fashiondogma/comments/1bgyw62/asian_girl/). It was on the front page and had photos of sliders. With photos, you can auto read the values in some programs which was easier than manually doing it. 

## Credits
directkeys.py logic via stackoverflow user `user573949` - [Post](http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game)

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FMx772%2Fdragons-dogma-2-auto-character-creator%2Ftree%2Fmain&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
