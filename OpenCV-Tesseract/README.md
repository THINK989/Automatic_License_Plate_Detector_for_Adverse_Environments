# OpenCV-Tesseract
---

One of the traditional techniques used for license plate detection by detecting **canny edges** and **filtering** down to the one which is shaped like a rectangle.
Cropping such a rectangle and give it as an input to tesseract-OCR for converting the image to text for License Plate Recognition.


## Get Started
---

To run the script 
```
python opencv-tesseract.py
```

## Results
---

It takes a lot of time to run on the input.mpg video provided in data folder . Specifically 3 min to process a 11 sec video for both license plate detection and
recognition. Recognition accuracy is too less as well. The script only detects only 1 license plate per frame. There are better approaches using OpenCV, but i will stick to this one.



