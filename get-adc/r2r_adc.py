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
                if self.verbose:
                    print(f"ADC Value found: {value}")
                return value

        return 255

    def get_sc_voltage(self):
        value = self.sequential_counting_adc()
        voltage = (value / 255) * self.dynamic_range
        return voltage

if __name__ == "__main__":
    MY_DYNAMIC_RANGE = 3.3

    adc = None
    try:
        adc = R2R_ADC(dynamic_range=MY_DYNAMIC_RANGE, verbose=False)

        print("Начинаю измерение напряжения. Нажмите Ctrl+C для выхода.")
        while True:
            voltage = adc.get_sc_voltage()
            print(f"Voltage: {voltage:.3f} V")

    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем")
    finally:
        if adc is not None:
            del adc
