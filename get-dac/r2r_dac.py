import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):

        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)

        if self.verbose:
            print(f"R2R_DAC инициализирован с пинами {gpio_bits}")
            print(f"Динамический диапазон: {dynamic_range} В")

    def deinit(self):

        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

        if self.verbose:
            print("R2R_DAC деинициализирован, GPIO очищены")

    def set_number(self, number):


        if number < 0:
            number = 0
            if self.verbose:
                print("Предупреждение: число меньше 0, установлено 0")
        elif number > 255:
            number = 255
            if self.verbose:
                print("Предупреждение: число больше 255, установлено 255")

        binary_str = bin(number)[2:].zfill(8)

        for i in range(8):
            GPIO.output(self.gpio_bits[i], int(binary_str[i]))

        if self.verbose:
            print(f"Установлено число: {number} (0x{number:02X}) -> двоичный код: {binary_str}")
            print(f"Теоретическое напряжение: {number / 255 * self.dynamic_range:.3f} В")

    def set_voltage(self, voltage):
        """
        Устанавливает напряжение на выходе ЦАП
        :param voltage: желаемое напряжение (от 0 до dynamic_range)
        """

        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage:.3f} В выходит за динамический диапазон ЦАП")
            print(f"Допустимый диапазон: 0.00 - {self.dynamic_range:.3f} В")
            print("Устанавливаем 0.0 В")

            if self.verbose:
                print("Используется значение по умолчанию: 0 В")

            self.set_number(0)
            return


        number = int(voltage / self.dynamic_range * 255)

        if self.verbose:
            print(f"Преобразование напряжения {voltage:.3f} В -> число {number}")

        self.set_number(number)


if __name__ == "__main__":
    try:

        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)

        print("\n" + "="*50)
        print("Программа управления 8-битным R2R ЦАП")
        print("Для выхода нажмите Ctrl+C")
        print("="*50 + "\n")

        while True:
            try:

                voltage = float(input("Введите напряжение в Вольтах: "))

                dac.set_voltage(voltage)
                print()


    finally:
        dac.deinit()
        print("Завершение работы программы")
