import time
from r2r_adc import R2R_ADC  # Предполагается, что класс R2R_ADC в файле adc_class.py
import adc_plot

# Настройки
MY_DYNAMIC_RANGE = 3.3  # Измеренный диапазон вашего ЦАП
DURATION = 3.0          # Продолжительность измерений в секундах

# Создание объекта АЦП с малым временем сравнения для ускорения процесса
adc = R2R_ADC(dynamic_range=MY_DYNAMIC_RANGE, compare_time=0.0001)

voltage_values = []
time_values = []

try:
    print(f"Начинаю запись данных на {DURATION} секунды...")

    # Сохраняем момент начала эксперимента
    start_time = time.time()

    # Цикл сбора данных
    while (time.time() - start_time) < DURATION:
        # Добавляем в список текущий момент времени (относительно старта)
        current_relative_time = time.time() - start_time
        time_values.append(current_relative_time)

        # Измеряем и добавляем значение напряжения
        current_voltage = adc.get_sc_voltage()
        voltage_values.append(current_voltage)

    print("Сбор данных завершен. Построение графика...")

    # Отображаем график подготовленной функцией
    adc_plot.plot_voltage_vs_time(time_values, voltage_values, MY_DYNAMIC_RANGE)

finally:
    # Вызываем "деструктор" (очистка GPIO и обнуление ЦАП)
    del adc
    print("Программа завершена, GPIO очищены.")
