import time
from r2r_adc import R2R_ADC
import adc_plot

# Настройки эксперимента
MY_DYNAMIC_RANGE = 3.3
DURATION = 3.0

# Создаем объект АЦП. Убедитесь, что в r2r_adc.py есть метод get_sc_voltage!
adc = R2R_ADC(dynamic_range=MY_DYNAMIC_RANGE, compare_time=0.0001)

voltage_values = []
time_values = []

try:
    print(f"Начинаю запись данных на {DURATION} секунды...")
    start_time = time.time()

    while (time.time() - start_time) < DURATION:
        # Фиксируем текущее время относительно начала
        current_relative_time = time.time() - start_time
        time_values.append(current_relative_time)

        # Вызываем метод измерения напряжения
        current_voltage = adc.get_sc_voltage()
        voltage_values.append(current_voltage)

    print("Сбор данных завершен. Построение графика...")
    # Используем имя модуля adc_plot, как указано в импорте
    adc_plot.plot_voltage_vs_time(time_values, voltage_values, MY_DYNAMIC_RANGE)

    print("Построение гистограммы периодов дискретизации...")
    # ИСПРАВЛЕНО: передаем список time_values вместо модуля time
    adc_plot.plot_sampling_period_hist(time_values)

finally:
    # Очистка
    if 'adc' in locals():
        del adc
    print("Программа завершена, GPIO очищены.")
