import time
import r2r_adc as adc_mod  # Ваш модуль с классом R2R_ADC
import adc_plot as adp     # Ваш модуль с функцией гистограммы

# Параметры эксперимента
MY_DYNAMIC_RANGE = 3.3
EXPERIMENT_DURATION = 5  # Продолжительность в секундах

def main():
    adc = None

    try:
        adc = adc_mod.R2R_ADC(dynamic_range=MY_DYNAMIC_RANGE, compare_time=0, verbose=False)

        voltages = []
        timestamps = []
        print(f"Запуск записи данных на 5 сек")
        start_time = time.time()

        while (time.time() - start_time) < EXPERIMENT_DURATION:
            v = adc.get_sar_voltage()
            voltages.append(v)

            timestamps.append(time.time() - start_time)

            if len(voltages) % 50 == 0:
                print(f"Текущее напряжение: {v:.3f} V")

        print(f"Запись окончена. Обработка {len(voltages)} точек...")

        if len(voltages) > 0:
            adp.plot_voltage_vs_time(timestamps, voltages, MY_DYNAMIC_RANGE)

            adp.plot_sampling_period_hist(timestamps)

    except KeyboardInterrupt:
        print("\nПрервано пользователем.")

    finally:
        if adc is not None:
            del adc
        print("Работа завершена.")

if __name__ == "__main__":
    main()
