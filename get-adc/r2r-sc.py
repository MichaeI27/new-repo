import time
from adc_class import R2R_ADC
import adc_plot

MY_DYNAMIC_RANGE = 3.3
DURATION = 3.0

adc = R2R_ADC(dynamic_range=MY_DYNAMIC_RANGE, compare_time=0.0001)

voltage_values = []
time_values = []

try:
    print(f"Начинаю запись данных на {DURATION} секунды...")

    start_time = time.time()

    while (time.time() - start_time) < DURATION:
        current_relative_time = time.time() - start_time
        time_values.append(current_relative_time)

        current_voltage = adc.get_sc_voltage()
        voltage_values.append(current_voltage)

    print("Сбор данных завершен.")

    adc_plot.plot_voltage_vs_time(time_values, voltage_values, MY_DYNAMIC_RANGE)

    print("Построение гистограммы периодов дискретизации...")

    adp.plot_sampling_period_hist(time)

finally:
    del adc
    print("Программа завершена, GPIO очищены.")
