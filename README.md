# Deep Work
Visualization and productivity timer written in Python

## Why?
I read Cal Newport's [Deep Work](https://www.amazon.com/Deep-Work-Focused-Success-Distracted/dp/1455586692) and wanted to create a scoreboard that helps me track my work.

## Usage
Change `constants.py` `VISUAL_PATH` and `DEEP_PATH` to wherever you want. `DEEP_PATH` is where all of your time logs are stored. `VISUAL_PATH` is where daily JSON is outputted when stopping or `deep update` (it should be your visual folder).

#### `./deep.py start`
starts the timer

#### `./deep.py stop` 
stops the timer

#### `./deep.py clear`
deletes the log

#### `./deep.py log`
pretty prints the log

#### `./deep.py update` 
called automatically after stop, outputs todays deep work to `VISUAL_PATH` (json)

## Visualization

To start the visualization go into the visual folder and type `./start.sh`. You can then visit `http://localhost:1337` to see your daily work.

![deep work image](https://i.imgur.com/tY9dxxz.png)
