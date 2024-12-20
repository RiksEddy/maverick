from rpi_ws281x import PixelStrip, Color
import json

# Read the config file  
with open('/home/maverick/config.json') as config_file:
    config = json.load(config_file)

# LED strip configuration:
LED_COUNT = config["number_of_LEDs"]  # Set LED_COUNT from config
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz
LED_DMA = 10          # DMA channel to use for generating signal
LED_BRIGHTNESS = 10   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class LEDStrip:
    def __init__(self):
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, 
                               LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self.current_color = None
        
    def colorWipe(self, color):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def theaterChase(self, color, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)
    
    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)
        
    def rainbow(self, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
        
    def rainbowCycle(self, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel(
                    (int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()

    def theaterChaseRainbow(self):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                self.strip.show()
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)
            
    def turn_off(self):
        """Turn off all LEDs."""
        self.current_color = None
        self.colorWipe(Color(0, 0, 0))
        
    def turn_red(self):
        """Turn all LEDs red."""
        self.current_color = "red"
        self.colorWipe(Color(255, 0, 0))
        
    def turn_green(self):
        """Turn all LEDs green."""
        self.current_color = "green"
        self.colorWipe(Color(0, 255, 0))
        
    def turn_blue(self):
        """Turn all LEDs blue."""
        self.current_color = "blue"
        self.colorWipe(Color(0, 0, 255))
    
    def turn_yellow(self):
        """Turn all LEDs yellow."""
        self.current_color = "yellow"
        self.colorWipe(Color(255, 255, 0))
    
    def turn_purple(self):
        """Turn all LEDs purple."""
        self.current_color = "purple"
        self.colorWipe(Color(128, 0, 128))
    
    def turn_orange(self):
        """Turn all LEDs orange."""
        self.current_color = "orange"
        self.colorWipe(Color(255, 165, 0))
    
    def turn_white(self):
        """Turn all LEDs white."""
        self.current_color = "white"
        self.colorWipe(Color(255, 255, 255))