# Fibo_1
Raspberry Pi based project. A ball following robot using Raspberry Pi camera module.

# Equipment used
- Raspberry Pi 3 model B
- Raspberry Pi Camera V2
- L298N Dual H Bridge DC Stepper Motor Driver Controller
- Power supply for Raspberry Pi (any suitable)
- Power supply for motors (6 x AA battery)
- Devastator tank from DFRobot (Any robot can be used. Check technical specifications of your's and make changes accordingly.)

# Object Detection Background
Correct color (object) detection depends heavily on surrounding light condition. Color detection settings in this project were optimized for no ambient light (dark room). 6 white LEDs connected to Raspberry Pi, were used as the only light source.

1. This project uses common color detection method implemented via OpenCV methods. Image from camera is converted to HSV color space. HSV values are selected to detect green hues in a certain range based on color of the ball. For this project a tennis ball was used, so green hues were selected and the image was masked. Any color can be detected by changing this HSV range. 
2. From the masked image contours were detected and based on this, a rectangle around the object was determined. This rectangle plays important role next.
3. Area of the rectangle and 'cx' (horizontal) position was used to control the robot's movement. These values should be selected accordingly to the camera resolution. (640 x 480 was used in this project).

N.B. The rectangle is based on the range of hues selected previously and the HSV values depends on light properties. If there is change of ambient light, the HSV values may change due the camera image processing such as (mainly) white balance. Change in white balance produce change in RGB (BGR) values and consequently HSV values. Important for this project is to have non-changing light, hence only the LEDs were used to produce light. This project is not likely to work correctly under any other light. Please be careful !!!

# Robot Movement
Once the correct rectangle was established (object in interest was found), the 'cx' value and area was used to control the movement in a simple if-else statement. These values should be again set accordingly to the camera resolution

# Disclaimer
Although all precautions were taken to work safely, I do not accept any responsibility for damaged equipment, nor harm to people. Safety first, be safe ...

# Shopping
Motor driver controller : https://www.amazon.co.uk/Module-Bridge-Driver-Stepper-Controller/dp/B07H76LH76/ref=sr_1_7?keywords=l298n+driver+board&qid=1556728850&s=gateway&sr=8-7

Devastator robot : https://www.dfrobot.com/product-1477.html
