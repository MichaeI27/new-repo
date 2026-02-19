import RPi.GPIO as GPIO

leds = [16, 20, 21, 25, 26, 17, 27, 22]

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)

dynamic_range = 3.3



def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 {dynamic_range:.2f} B)")
        print("Устанавливаем 0.0 B")
        return 0
    
    return int(voltage / dynamic_range * 255)
