import RPi.GPIO as GPIO


class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits    
        self.dynamic_range = dynamic_range 
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
            return

        max_number = 2 ** len(self.gpio_bits) - 1
        if not (0 <= number <= max_number):
            print(f"Число выходит за разрядность ЦАП (0..{max_number})")
            return

        for i, pin in enumerate(self.gpio_bits):
            bit = (number >> i) & 1
            GPIO.output(pin, bit)

        if self.verbose:
            print(f"Число: {number}, двоичный вид: {number:0{len(self.gpio_bits)}b}\n")

    def set_voltage(self, voltage):
        if voltage < 0 or voltage > self.dynamic_range:
            print(f"Напряжение {voltage} В выходит за диапазон 0..{self.dynamic_range} В")
            return

        max_number = 2 ** len(self.gpio_bits) - 1
        number = int(round((voltage / self.dynamic_range) * max_number))
        self.set_number(number)


if __name__ == "__main__":
    try:
        dac = R2R_DAC([22, 27, 17, 26, 25, 21, 20, 16], 3.183, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()
