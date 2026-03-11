import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def __del__(self):
        self.number_to_dac(0)
        GPIO.cleanup()
        if self.verbose:
            print("GPIO cleaned up and DAC set to 0")

    def number_to_dac(self, number):
        # Преобразуем число в список бит и подаем на GPIO
        bits = [int(bit) for bit in bin(number)[2:].zfill(8)]
        GPIO.output(self.bits_gpio, bits)

    # Метод последовательного счета (уже был у вас)
    def sequential_counting_adc(self):
        for value in range(256):
            self.number_to_dac(value)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == GPIO.HIGH:
                return value
        return 255

    # --- НОВЫЕ МЕТОДЫ ---

    def successive_approximation_adc(self):
        """Реализация алгоритма бинарного поиска (SAR)"""
        value = 0
        for i in range(7, -1, -1):
            # Пробуем установить i-й бит в 1
            bit_weight = 1 << i
            value += bit_weight

            self.number_to_dac(value)
            time.sleep(self.compare_time)

            # Если напряжение на ЦАП стало больше входного (компаратор выдал 0),
            # значит этот бит лишний — сбрасываем его
            if GPIO.input(self.comp_gpio) == GPIO.LOW:
                value -= bit_weight

        if self.verbose:
            print(f"SAR ADC Value: {value}")
        return value

    def get_sar_voltage(self):
        """Возвращает измеренное напряжение в Вольтах (метод SAR)"""
        value = self.successive_approximation_adc()
        # Для 8-битного АЦП формула: (value / 256) * range
        voltage = (value / 256.0) * self.dynamic_range
        return voltage

# --- ОСНОВНОЙ ОХРАННИК ---

if __name__ == "__main__":
    MY_DYNAMIC_RANGE = 3.3  # Напряжение питания (опорное)

    adc = None
    try:
        # Создаем объект класса
        adc = R2R_ADC(dynamic_range=MY_DYNAMIC_RANGE, verbose=False)

        print("Начинаю измерение методом SAR. Нажмите Ctrl+C для выхода.")
        while True:
            # Используем новый метод SAR для измерения
            voltage = adc.get_sar_voltage()
            print(f"Measured Voltage: {voltage:.4f} V")

    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем")
    finally:
        # Вызов «деструктора» объекта (сработает GPIO.cleanup())
        if adc is not None:
            del adc
