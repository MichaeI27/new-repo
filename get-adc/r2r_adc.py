import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.001, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        # Пины GPIO: [MSB ... LSB]
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False) # Чтобы не спамило предупреждениями
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def __del__(self):
        # Перед выходом обнуляем ЦАП, чтобы не греть резисторы
        self.number_to_dac(0)
        GPIO.cleanup()
        if self.verbose:
            print("GPIO cleaned up and DAC set to 0")

    def number_to_dac(self, number):
        # Преобразование числа в список битов (8 бит)
        # Ограничиваем число диапазоном 0-255
        number = int(max(0, min(255, number)))
        bits = [int(bit) for bit in bin(number)[2:].zfill(8)]
        GPIO.output(self.bits_gpio, bits)

    def sequential_counting_adc(self):
        """Метод последовательного счета (медленный)"""
        for value in range(256):
            self.number_to_dac(value)
            time.sleep(self.compare_time)
            # Если напряжение ЦАП стало ВЫШЕ входного (компаратор сработал)
            if GPIO.input(self.comp_gpio) == GPIO.HIGH:
                return value
        return 255

    def get_sc_voltage(self):
        value = self.sequential_counting_adc()
        return (value / 255.0) * self.dynamic_range # Делим на 255 для точности

    def successive_approximation_adc(self):
        """Метод поразрядного уравновешивания (быстрый)"""
        value = 0
        for i in range(7, -1, -1):
            bit_weight = 1 << i
            value += bit_weight
            self.number_to_dac(value)

            # Ждем стабилизации напряжения на R2R матрице
            time.sleep(self.compare_time)

            # ПРОВЕРКА ЛОГИКИ:
            # Если ЦАП > Входа, компаратор выдает LOW (в классической схеме)
            # В таком случае мы "отменяем" установку этого бита
            if GPIO.input(self.comp_gpio) == GPIO.LOW:
                value -= bit_weight

        return value

    def get_sar_voltage(self):
        value = self.successive_approximation_adc()
        return (value / 255.0) * self.dynamic_range

if __name__ == "__main__":
    MY_DYNAMIC_RANGE = 3.3
    adc = None
    try:
        adc = R2R_ADC(dynamic_range=MY_DYNAMIC_RANGE, compare_time=0.001, verbose=True)
        print("Запуск теста. Нажмите Ctrl+C для выхода.")

        while True:
            # Снимаем показания обоими методами
            v_sar = adc.get_sar_voltage()
            v_sc = adc.get_sc_voltage()

            # Вывод в одну строку с возвратом каретки
            print(f"\rSAR: {v_sar:.3f}V | SC: {v_sc:.3f}V", end="", flush=True)
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nПрограмма остановлена.")
    finally:
        if adc is not None:
            del adc
