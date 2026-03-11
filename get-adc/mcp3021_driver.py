import smbus
import time

class MCP3021:
    def __init__(self, dynamic_range, verbose=False):
        """
        Инициализация АЦП MCP3021.
        :param dynamic_range: Опорное напряжение (измеренное на контакте PWR).
        :param verbose: Флаг для вывода отладочной информации.
        """
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D  # Стандартный I2C адрес устройства
        self.verbose = verbose

    def deinit(self):
        """Освобождение ресурсов шины I2C."""
        self.bus.close()
        if self.verbose:
            print("Шина I2C закрыта.")

    def get_number(self):
        """
        Чтение 10-битного числа из микросхемы.
        Согласно даташиту, данные приходят в 2 байтах (MSB первым).
        """
        # Читаем слово (2 байта).
        # smbus.read_word_data меняет байты местами (младший байт становится первым).
        data = self.bus.read_word_data(self.address, 0)

        # Разделяем на байты, исправляя порядок для smbus
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF

        # Формируем 10-битное число:
        # Старший байт содержит 6 значимых бит [X, X, D9, D8, D7, D6, D5, D4]
        # Младший байт содержит 4 значимых бита [D3, D2, D1, D0, X, X, X, X]
        number = ((upper_data_byte & 0x3F) << 4) | (lower_data_byte >> 4)

        if self.verbose:
            print(f"Принятые данные: {data}, "
                  f"Старший байт: {upper_data_byte:08b}, "
                  f"Младший байт: {lower_data_byte:08b}, "
                  f"Число: {number}")

        return number

    def get_voltage(self):
        """Преобразование цифрового значения в напряжение."""
        number = self.get_number()
        # 10-битный АЦП имеет 2^10 = 1024 уровня
        voltage = (number / 1024.0) * self.dynamic_range
        return voltage

# --- Основной блок (Main Guard) ---

if __name__ == "__main__":
    # ВАЖНО: Измерьте напряжение мультиметром на контакте PWR (блок AUX)
    # и впишите его сюда для точности измерений.
    REAL_DYNAMIC_RANGE = 5.0

    adc = None
    try:
        # Создаем объект АЦП
        adc = MCP3021(dynamic_range=REAL_DYNAMIC_RANGE, verbose=True)

        print("--- Мониторинг напряжения MCP3021 ---")
        print("Нажмите Ctrl+C для остановки...")

        while True:
            # Читаем напряжение
            val_v = adc.get_voltage()

            # Печатаем результат
            print(f"Напряжение: {val_v:.3f} V")

            # Задержка 1 секунда согласно инструкции
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nИзмерение остановлено пользователем.")

    finally:
        # Вызываем "деструктор"
        if adc is not None:
            adc.deinit()
