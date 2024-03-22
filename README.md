# Gestures

Gestures is a Python-based project that enables you to control the mouse pointer on your computer using hand gestures. It utilizes the MediaPipe library for hand tracking and the OpenCV library for camera access and frame extraction.

## Demo

The demo video is not out yet; I'm working on it. Stay tuned!

## Prerequisites

Make sure you have Python 3.x installed. The required libraries will be installed automatically when you run the main script.

```bash
git clone https://github.com/Matthiasklaasse/gestures.git
cd gestures
python main.py
```
## Configuration

You can customize certain parameters in the `config.ini` file to adjust sensitivity, click duration, or any other settings that suit your preferences.

## Troubleshooting

If you encounter any issues while running the gestures project, let me know in the comments of the demo video.

## Controls

1. touch your middle finger with your thumb to click
2. touch your ring finger with your thumb it triggers a right click
3. touch you index finger with your thumb to 'grab' you cursor and move it around the screen

## System reqirements

The code will run anywhere but i recomend haveing a pc with a gpu becouse on my laptop with intel itergated grapics it lags a little, ive tried to make the code a efficiens as possible but python will be python...