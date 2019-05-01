# Import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import numpy as np
import time
import cv2

# Toggle live view (for faster procesing toggle off)
live_view = 0 # 0 - live view off, 1 - live view on

light = 8 # GPIO Pin for front light

# Set GPIO mode and servo pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.output(light, True) # Turn the light on

# Initialize the camera
camera = PiCamera()
camera.rotation = 180
camera.resolution = (640, 480)
camera.framerate = 20
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(1)

# capture frames from the camera        
try:
    while True:
        try:
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                
                # Capture original image
                or_im = frame.array
                
                # ------------------------ Image processing ------------------ #
                # ------------------------------------------------------------ # 
                # Convert to HSV color space
                hsv_im = cv2.cvtColor(or_im, cv2.COLOR_BGR2HSV)

                # Define range of green color in HSV and mask it
                # this is the part where you have find correct values for your
                # system.
                lower_green = np.array([30,70,100])
                upper_green = np.array([70,255,255])

                # Threshold the HSV image to get only green colors
                green_mask = cv2.inRange(hsv_im, lower_green, upper_green)
                # Fine-tuning the mask
                green_mask = cv2.erode(green_mask, np.ones((10,10),np.uint8))

                # Bitwise-AND mask and original image for green colors
                green_res = cv2.bitwise_and(or_im,or_im, mask = green_mask)
                
                # ------------------------ Object detection ------------------ #
                # ------------------------------------------------------------ #
                # Find contours from mask
                _, contours,hierarchy = cv2.findContours(green_mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

                cnt = contours[0]
          
                # Get moments from cnt (contours dicitionary)
                M = cv2.moments(cnt)

                # Get cx and cy centroid coordinates
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                
                # Get area of the rect
                area = cv2.contourArea(cnt)
                
                # Create bounding rectangle around contours (around the object)
                x,y,w,h = cv2.boundingRect(cnt)
                rect = cv2.rectangle(or_im,(x, y),(x+w,y+h),(255, 0, 0),1)

                # show the image
                if live_view == 1:
                    cv2.imshow('Tracked Object', or_im)
                    key = cv2.waitKey(1) & 0xFF

                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)
                
                # ------------------------ Moving the Robot ------------------ #
                # ---- Test correct behaviour before using real movements ---- #
                # ------------------------------------------------------------ #  
                # Do not move the robot if the object is in range of distance (area size)
                if area <= 40000 and area >= 10000:
                    GPIO.output(31, False)
                    GPIO.output(33, False)
                    GPIO.output(35, False)
                    GPIO.output(37, False)
                
                # Move the robot - values depend on camera resolution and area size!!!
                if area > 40000: # move backward
                    #print('Moving back') # Test correct behaviour before using real movements
                    GPIO.output(31, False)
                    GPIO.output(33, True)
                    GPIO.output(35, False)
                    GPIO.output(37, True)
                    

                elif area < 5000: # move forward
                    #print('Moving forward') # Test correct behaviour before using real movements
                    GPIO.output(31, True)
                    GPIO.output(33, False)
                    GPIO.output(35, True)
                    GPIO.output(37, False)
                    

                # move left
                if cx <= 100: # Ball moving left
                    #print('Turning to the left') # Test correct behaviour before using real movements
                    GPIO.output(31, True)
                    GPIO.output(33, False)
                    GPIO.output(35, False)
                    GPIO.output(37, False)
                    print('Turning to the left')
         
                # move right        
                elif cx >= 500: # Ball moving right
                    #print('Turning to the right') # Test correct behaviour before using real movements
                    GPIO.output(31, False)
                    GPIO.output(33, False)
                    GPIO.output(35, True)
                    GPIO.output(37, False)
                    print('Turning to the right')

                print('cx =', cx, '; area =', area) 
        except IndexError:
            rawCapture = PiRGBArray(camera, size=(640, 480))
            pass
        except ZeroDivisionError:
            rawCapture = PiRGBArray(camera, size=(640, 480))
            print('Object not detected')
            pass


except KeyboardInterrupt:
    print('Interrupted')
    camera.close()
    cv2.destroyAllWindows()
    GPIO.cleanup()

