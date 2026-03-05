import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import time

buttons = [9, 10]
leds = [16, 12, 25, 17, 27, 23, 22, 24]

GPIO.setup(buttons, GPIO.IN)
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)

counter = 0
light_time = 0.2

while True:
	for i in leds:
		GPIO.output(i, 1)
		time.sleep(light_time)
		GPIO.output(i, 0)
	for i in reversed(leds):
		GPIO.output(i, 1)
		time.sleep(light_time)
		GPIO.output(i, 0)
