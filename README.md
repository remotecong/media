# Media (WIP)

Allows you to save songs through the jw.org online library. Currently only does the _Meeting Version of Songs_. 

## Install:
```bash
pip install -r requirements.txt
```

## Usage:
```bash
python songs.py 93 57 30
```

The first time you run it will try and load up its default settings json file `.settings.json` and figure out where to store downloaded videos. Give it a path (perhaps to OnlyM's Media dir?) so that all media in the future will end up here.

## Songs (songs.py)
Downloads the meeting version of songs. It will download them as `Song {number}.mp4`.
