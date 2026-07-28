# Color Recognition using OpenCV

A real-time color detection project built with Python and OpenCV. The program uses a webcam feed to detect and highlight predefined colors (Red, Green, Blue, Yellow) by drawing a bounding box and label around each detected region.

## How It Works

1. Capture video from the webcam frame by frame using cv2.VideoCapture(0).
2. Convert each frame from BGR to HSV color space. HSV (Hue, Saturation, Value) makes it much easier to isolate a specific color than RGB/BGR, because the "Hue" channel represents color itself, separate from brightness and lighting.
3. Create a mask using cv2.inRange() for each target color's HSV range. Pixels that fall inside the range become white (255) in the mask; everything else becomes black (0).
4. Clean the mask with morphological operations (erosion + dilation) to remove small noise and fill gaps.
5. Find contours in the cleaned mask using cv2.findContours(). Contours are the outlines of the connected white regions (i.e., the detected color blobs).
6. Filter by area to ignore tiny, insignificant blobs (adjustable via MIN_CONTOUR_AREA).
7. Draw a bounding box and label on the original frame around any contour that passes the area filter.
8. Display the result in a live window, updated every frame.


## Setup Instructions (Anaconda Prompt)

### 1. Open Anaconda Prompt
Launch it from the Start Menu (Windows) or your applications list.

### 2. Create and activate a virtual environment
```bash
conda create -n opencv-env python=3.10 -y
conda activate opencv-env
```
Your prompt should now show (opencv-env) at the start of the line, confirming you're inside the environment.

### 3. Navigate to the project folder
```bash
cd "path\to\color-recognition-opencv"
```
Use quotes around the path if it contains spaces or non-English characters.

### 4. Install dependencies
```bash
pip install -r requirements.txt
```
(or manually: pip install opencv-python numpy)

### 5. Run the script
```bash
python color_recognition.py
```

A window will open showing your webcam feed with colored boxes drawn around any detected Red, Green, Blue, or Yellow objects.

## Controls

| Key | Action |
|-----|--------|
| q | Quit the program |
| t | Toggle the HSV tuning trackbar window |

---

You can find the right HSV values by:
- Using the built-in tuning window (press t while the program is running), or
- Picking a pixel color from a sample image and converting it to HSV manually.

## Requirements

- Python 3.8+
- A working webcam
- OpenCV (opencv-python)
- NumPy

Install everything with:
```bash
pip install -r requirements.txt
```

---

## Notes

- Red requires two HSV ranges because red hue values wrap around both ends of OpenCV's 0–179 hue scale.
- Lighting conditions significantly affect detection accuracy — use the tuning window if colors aren't being detected reliably.
- MIN_CONTOUR_AREA can be increased/decreased in the script to filter out small or large detected regions.
