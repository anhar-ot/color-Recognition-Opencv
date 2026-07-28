"""
Color Recognition using OpenCV
--------------------------------
Detects a chosen color (default: red) from a live webcam feed,
draws a bounding box around it, and labels it on screen.

Run with:
    python color_recognition.py

Controls:
    q  -> quit
    t  -> toggle the HSV tuning trackbars window
"""

import cv2
import numpy as np

# ---------------------------------------------------------
# 1. Default HSV ranges for common colors.
#    HSV = Hue, Saturation, Value. OpenCV's Hue range is 0-179.
#    Feel free to add more colors or tune these with the
#    trackbar window (press 't').
# ---------------------------------------------------------
COLOR_RANGES = {
    "Red":    [(np.array([0, 120, 70]),   np.array([10, 255, 255])),
               (np.array([170, 120, 70]), np.array([180, 255, 255]))],  # red wraps around hue=0
    "Green":  [(np.array([36, 100, 70]),  np.array([89, 255, 255]))],
    "Blue":   [(np.array([94, 100, 70]),  np.array([126, 255, 255]))],
    "Yellow": [(np.array([20, 100, 70]),  np.array([35, 255, 255]))],
}

MIN_CONTOUR_AREA = 800  # ignore tiny noisy blobs


def build_mask(hsv_frame, ranges):
    """Combine one or more HSV ranges into a single binary mask."""
    mask = None
    for lower, upper in ranges:
        part = cv2.inRange(hsv_frame, lower, upper)
        mask = part if mask is None else cv2.bitwise_or(mask, part)
    return mask


def clean_mask(mask):
    """Reduce noise using morphological operations."""
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    return mask


def detect_and_draw(frame, hsv_frame, color_name, ranges, box_color):
    mask = build_mask(hsv_frame, ranges)
    mask = clean_mask(mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > MIN_CONTOUR_AREA:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)
            cv2.putText(frame, color_name, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, box_color, 2)
    return mask


def nothing(x):
    pass


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: could not access the webcam.")
        return

    # Colors used to draw each bounding box (BGR format for cv2.rectangle)
    draw_colors = {
        "Red": (0, 0, 255),
        "Green": (0, 255, 0),
        "Blue": (255, 0, 0),
        "Yellow": (0, 255, 255),
    }

    show_trackbars = False
    window_tune = "HSV Tuner"

    print("Press 'q' to quit, 't' to toggle the HSV tuning window.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: failed to grab frame.")
            break

        frame = cv2.flip(frame, 1)  # mirror for a more natural view
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Detect every color in COLOR_RANGES
        for color_name, ranges in COLOR_RANGES.items():
            detect_and_draw(frame, hsv, color_name, ranges, draw_colors[color_name])

        cv2.imshow("Color Recognition", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('t'):
            show_trackbars = not show_trackbars
            if show_trackbars:
                cv2.namedWindow(window_tune)
                cv2.createTrackbar("LH", window_tune, 0, 179, nothing)
                cv2.createTrackbar("LS", window_tune, 100, 255, nothing)
                cv2.createTrackbar("LV", window_tune, 70, 255, nothing)
                cv2.createTrackbar("UH", window_tune, 10, 179, nothing)
                cv2.createTrackbar("US", window_tune, 255, 255, nothing)
                cv2.createTrackbar("UV", window_tune, 255, 255, nothing)
            else:
                cv2.destroyWindow(window_tune)

        if show_trackbars:
            lh = cv2.getTrackbarPos("LH", window_tune)
            ls = cv2.getTrackbarPos("LS", window_tune)
            lv = cv2.getTrackbarPos("LV", window_tune)
            uh = cv2.getTrackbarPos("UH", window_tune)
            us = cv2.getTrackbarPos("US", window_tune)
            uv = cv2.getTrackbarPos("UV", window_tune)
            custom_mask = cv2.inRange(hsv, np.array([lh, ls, lv]), np.array([uh, us, uv]))
            cv2.imshow(window_tune, custom_mask)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
