import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import time

buttons = [9, 10]
leds = [16, 12, 25, 17, 27, 23, 22, 24]

GPIO.setup(buttons, GPIO.IN)
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)

counter = 0
sleep_time = 0.2

def dec2bin(value):
	return [int(element) for element in bin(value)[2:].zfill(8)]

while True:
	counter += GPIO.input(buttons[0])
	counter -= GPIO.input(buttons[1])
	if counter > 255 or counter < 0:
		counter = 0
	if GPIO.input(buttons[0]) and GPIO.input(buttons[1]):
		counter = 255

	print(counter, dec2bin(counter))
	time.sleep(sleep_time)
	GPIO.output(leds, dec2bin(counter))
