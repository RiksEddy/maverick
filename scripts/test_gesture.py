from apds9960.const import *
from apds9960 import APDS9960
import smbus
from time import sleep

#WIRING
#GND -> GND
#VCC -> 3v3
#SDA -> I2C1 SDA (GPIO 2)
#SCL -> I2C1 SCL (GPIO 3)

port = 1
bus = smbus.SMBus(port)
apds = APDS9960(bus)

dirs = {
    APDS9960_DIR_UP: "up",
    APDS9960_DIR_DOWN: "down"
}
try:

    print("Gesture Test")
    print("============")
    apds.enableGestureSensor()
    while True:
        sleep(0.1)
        if apds.isGestureAvailable():
            motion = apds.readGesture()
            print("Gesture={}".format(dirs.get(motion, "unknown")))


finally:
    GPIO.cleanup()
    print("Bye")
