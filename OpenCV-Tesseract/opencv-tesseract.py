"""
An old unreliable approach which requires a lot of hand engineering
And even after spending time on it for a lont time, It might not work as expected
Note:- This script will only provide 1 bounding box per frame. 
To allow multiple bbox changes are to made in preprocessing function by using lists of list 
instead of sigle coordinates
"""
import cv2
from pytesseract import image_to_string
from numpy import median
from time import time

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = median(image)
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged

def preprocessing(frame):
    # thresh = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 115, 3)
    x,y,w,h,plate_number = 0,0,0,0,None
    # Detect Edges on the image
    edges = auto_canny(frame)
    # Find all the contours i.e. all clossed lines
    _, cnts, _ = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Narrow down the number of contours to places where is it most populated
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    for ctr in cnts:
        perimeter = cv2.arcLength(ctr, True)
        # Narrow down even more to only accept rectangles
        if len(cv2.approxPolyDP(ctr, 0.02*perimeter, True)) == 4:
            x, y, w, h = cv2.boundingRect(ctr)
            lic_plate = frame[y:y+h, x:x+w]
            plate_number = image_to_string(lic_plate)
            # only accepts contours with text in it
            if plate_number:  
                return x, y, w, h, True, plate_number
    return x, y, w, h, False, plate_number

def main():
    # Capture Video specifying the video file
    # If the video input is a IP Camera then use cap = cv2.VideoCapture("ipcam_streaming_url") instead
    # check https://stackoverflow.com/questions/49978705/access-ip-camera-in-python-opencv for more
    cap = cv2.VideoCapture('data/input.mpg') # Video is clipped from https://www.youtube.com/watch?v=fxQBibd-dqw
    
    # Get width and height of the frame of video
    width  = cap.get(3) # float width
    height = cap.get(4) # float height
    
    # Prepare for writing the output frame in the new video which will have bbox and char recognition
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    out_video = cv2.VideoWriter('result/output.avi', fourcc, 20.0, (int(width), int(height)), True)
    
    #font to be used to put text in frame later
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Monitor time taken to run the script
    start = time()

    # Run until the video is not over
    while(cap.isOpened()):
        # Read each frame where ret is a return boollean value(True or False)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert the frame to gray scale
        # Send the frame for preprocessing to get bounding box and the plate_numbers
        x, y, w, h,avail,plate_number = preprocessing(gray)
        frame_copy = frame.copy()
        if avail:
            # Draw a rectangle from the extracted coordinates above
            cv2.rectangle(frame_copy, (x, y), (x + w, y + h), (255, 0, 255), 2)
            # Put a text above the rectangle where text is the output from pytesseract
            cv2.putText(frame_copy, str(plate_number), (x, y), font, 0.7, (255, 0, 255), 2, cv2.LINE_AA)
        
        # cv2.imshow('frame',frame_copy)
        out_video.write(frame_copy) # write the modifies frame into output video 
        # to forcefully stop the running loop and break out, if it doesnt work use ctlr+c
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    print('Time taken to run through the whole video is {}s'.format(time() - start))
    # Release the current
    cap.release()
    cv2.destroyAllWindows()
   

if __name__ == "__main__":
    main()