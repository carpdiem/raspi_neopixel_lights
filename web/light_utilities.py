#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse
import numpy as np

# LED strip configuration:
LED_COUNT      = 240      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


def plancksLaw(t):
    lambda_red = 630. * 10**-9
    lambda_green = 530. * 10**-9
    lambda_blue = 475. * 10**-9
    def planck(l, t):
        hc = 1.98644568 * 10**-25
        kb = 1.38064852 * 10**-23
        return 1. / (l**5.0 * ( np.exp(hc / (l * kb * t)) - 1.0))
    red = planck(lambda_red, t)
    green = planck(lambda_green, t)
    blue = planck(lambda_blue, t)
    max = np.max([red, green, blue])
    return (red / max, green / max, blue / max)


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def colorWipeFast(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def try_all_color_temperatures(strip):

        colorWipe(strip, Color(147, 255, 41), wait_ms = 0.0)
        time.sleep(1.0)
        colorWipe(strip, Color(197, 255, 143), wait_ms = 0.0)
        time.sleep(1.0)
        colorWipe(strip, Color(214, 255, 170), wait_ms = 0.0)
        time.sleep(1.0)
        colorWipe(strip, Color(241, 255, 224), wait_ms = 0.0)
        time.sleep(1.0)
        colorWipe(strip, Color(250, 255, 244), wait_ms = 0.0)
        time.sleep(1.0)
        colorWipe(strip, Color(255, 255, 251), wait_ms = 0.0)
        time.sleep(1.0)
        colorWipe(strip, Color(255, 255, 255), wait_ms = 0.0)
        time.sleep(1.0)
        colorWipe(strip, Color(226, 201, 255), wait_ms = 0.0)
        time.sleep(1.0)
        colorWipe(strip, Color(156, 64, 255), wait_ms = 0.0)
        time.sleep(1.0)

def initialize_strip():
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    return strip

def logarithmic_intensity(x):
    return 255 * (2.**(5 * x) - 1) / (2.**5 - 1)

def lights_on(strip, temp, brightness):
    rgb = plancksLaw(temp)
    red =   int(rgb[0] * logarithmic_intensity(brightness))
    green = int(rgb[1] * logarithmic_intensity(brightness))
    blue =  int(rgb[2] * logarithmic_intensity(brightness))
    colorWipeFast(strip, Color(green, red, blue))

def lights_off(strip):
    colorWipeFast(strip, Color(0, 0, 0))


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-t', type=float, help='color temperature to simulate')
    parser.add_argument('-b', type=float, help='brightness value, range: [0.0, 1.0]')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        # NOTE - Color() is not RGB, but GRB
#        try_all_color_temperatures(strip)
#        colorWipe(strip, Color(0,0,0))
        #colorWipe(strip, Color(35, 128, 5), wait_ms = 0.0)
        #colorWipe(strip, Color(70, 128, 25), wait_ms = 0.0)
        try:
            t = args.t
            print(t)
            intensity = args.b
            print(intensity)
        except:
            t = 1900
            intensity = 0.5
        if t != 0:
            rgb = plancksLaw(t)
            red =   int(rgb[0] * logarithmic_intensity(intensity))
            green = int(rgb[1] * logarithmic_intensity(intensity))
            blue =  int(rgb[2] * logarathmic_intensity(intensity))
            print(red)
            print(green)
            print(blue)
            colorWipeFast(strip, Color(green, red, blue))
        elif t == 0:
            colorWipeFast(strip, Color(0, 0, 0))

#        while True:
#            print ('Color wipe animations.')
#            colorWipe(strip, Color(255, 0, 0))  # Red wipe
#            colorWipe(strip, Color(0, 255, 0))  # Blue wipe
#            colorWipe(strip, Color(0, 0, 255))  # Green wipe
#            print ('Theater chase animations.')
#            theaterChase(strip, Color(127, 127, 127))  # White theater chase
#            theaterChase(strip, Color(127,   0,   0))  # Red theater chase
#            theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
#            print ('Rainbow animations.')
#            rainbow(strip)
#            rainbowCycle(strip)
#            theaterChaseRainbow(strip)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
