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
        bits = [int(bit) for bit in bin(number)[2:].zfill(8)]
        GPIO.output(self.bits_gpio, bits)

    def sequential_counting_adc(self):
        for value in range(256):
            self.number_to_dac(value)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == GPIO.HIGH:
                return value
        return 255

    # --- ДОБАВЛЕННЫЙ МЕТОД, КОТОРОГО НЕ ХВАТАЛО ---
    def get_sc_voltage(self):
        """Возвращает напряжение в Вольтах для последовательного счета"""
        value = self.sequential_counting_adc()
        return (value / 256.0) * self.dynamic_range

    def successive_approximation_adc(self):
        value = 0
        for i in range(7, -1, -1):
            bit_weight = 1 << i
            value += bit_weight
            self.number_to_dac(value)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == GPIO.LOW:
                value -= bit_weight
        return value

    def get_sar_voltage(self):
        value = self.successive_approximation_adc()
        return (value / 256.0) * self.dynamic_range

if __name__ == "__main__":
    MY_DYNAMIC_RANGE = 3.3
    adc = None
    try:
        adc = R2R_ADC(dynamic_range=MY_DYNAMIC_RANGE, verbose=False)
        print("Тест SAR...")
        print(f"Voltage: {adc.get_sar_voltage():.4f} V")
    except KeyboardInterrupt:
        print("\nВыход")
    finally:
        if adc is not None:
            del adc
