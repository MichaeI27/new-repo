import RPi.GPIO as GPIO

dec_pins = [16, 20, 21, 25, 26, 17, 27, 22]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dec_pins, GPIO.OUT)
GPIO.output(dec_pins, 0)

dynamic_range = 3.3

def number_to_dac(number):
    binary_str = bin(number)[2:].zfill(8)

    for i in range(8):
        GPIO.output(dec_pins[i], int(binary_str[i]))



def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 {dynamic_range:.2f} B)")
        print("Устанавливаем 0.0 B")
        return 0

    return int(voltage / dynamic_range * 255)


try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)

        except ValueError:
            print("Вы ввели не число. Попробуйте ещё раз\n")

finally:
    GPIO.output(dec_pins, 0)
    GPIO.cleanup()
