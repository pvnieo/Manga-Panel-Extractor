# Manga-Panel-Extractor
A python implementation of a Manga Panel Extractor and a dialogue bubble text eraser. (But we don't really care that much about text eraser so we might as well decide to get rid of this)

The text erasor is based on the CRAFT text detector. See [here](https://github.com/clovaai/CRAFT-pytorch) for more information.

## Installation

This service runs on python >= 3.6, use pip to install dependencies:

Optionally use a virtual environment
```
python3 -m venv venv

source venv/bin/activate
```
Then
```
pip3 install -r requirements.txt
```

## Usage
Use the `get_images.sh` script to get all the images to be processed. 

Give it executable permissions
```
sudo chmod +x get_images.sh
```

Then simply run
```
./get_images.sh
```

Use the `main.py` script to extract panels from manga pages provided in `folder`.
```
usage: main.py [-h] [-kt] [-minp [1-99]] [-maxp [1-99]] [-f TEST_FOLDER]

Implementation of a Manga Panel Extractor and dialogue bubble text eraser.

optional arguments:
  -h, --help            show this help message and exit
  -jc, --just_contours  Just save contours in a file. Will not output panel images.
  -kt, --keep_text      Do not erase the dialogue bubble text.
  -minp [1-99], --min_panel [1-99]
                        Percentage of minimum panel area in relation to total page area.
  -maxp [1-99], --max_panel [1-99]
                        Percentage of minimum panel area in relation to total page area.
  -f FOLDER, --folder FOLDER
                        folder path to input manga pages.
                        Panels will be saved to a directory named `panels` in this folder.
```

### Example
```
python main.py -kt -jc -f ./images/
```

### Issues

The two main point to reach MVP are:

[ ] Setup proper strategy for panels/contours order
[ ] Create FastApi app

After we reach MVP we can thing about all the other thing like CI/CD, Containerization and so on