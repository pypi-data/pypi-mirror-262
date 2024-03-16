# Catvibes
A simple music player offering not only a terminal based frontend but also a Qt based one.

# Qt look (with kvantum theme)
![](https://github.com/12fab4/Catvibes/blob/c4132bccc69fb53482da531fe58736929310f073/images/qtui.png?raw=true)
# Qt look (with Windows theme)
![](https://github.com/12fab4/Catvibes/blob/c4132bccc69fb53482da531fe58736929310f073/images/windows.png?raw=true)
# terminal look
![](https://github.com/12fab4/Catvibes/blob/c4132bccc69fb53482da531fe58736929310f073/images/terminalui.png?raw=true)


# Installation

    pip install Catvibes

## Requirements:
python and the following packages (will be installed as dependencies with pip):

    pip install ytmusicapi eyed3 yt-dlp PyQt6

it also requires ffplay

On linux install ffmpeg which is available on debian-based and arch-based distros and probably already installed

On Windows follow this tutorial: https://phoenixnap.com/kb/ffmpeg-windows


# Controls
## GUI:
launch with the --gui flag

## commandline:
f: find a song by typing a searchterm (ideally songname and bandname). Shows 3 results by default (select with the number keys).

esc: terminates searching usw and also exits the program

r: random shuffle, shuffles the queue randomly and adds the whole playlist to the queue when empty

p: play the whole playlist

a: add current song to the playlist

space: play / pause

n: next song

b: previous song

l: create a new playlist