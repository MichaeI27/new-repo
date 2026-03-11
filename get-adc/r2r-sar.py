import time
import r2r_adc as adc_mod  # Ваш модуль с классом R2R_ADC
import adc_plot as adp     # Ваш модуль с функцией гистограммы

# Параметры эксперимента
MY_DYNAMIC_RANGE = 3.3
EXPERIMENT_DURATION = 5  # Продолжительность в секундах

def main():
    # Создаем объект АЦП
    adc = adc_mod.R2R_ADC(dynamic_range=MY_DYNAMIC_RANGE, verbose=False)

    voltages = []
    timestamps = []

    try:
        print(f"Запуск записи данных (SAR) на {EXPERIMENT_DURATION} сек...")
        start_time = time.time()

        while (time.time() - start_time) < EXPERIMENT_DURATION:
            # Считываем напряжение методом SAR
            v = adc.get_sar_voltage()
            voltages.append(v)

            # Фиксируем метку времени относительно начала
            timestamps.append(time.time() - start_time)

        print(f"Запись окончена. Обработка {len(voltages)} точек...")

        # --- МОДЕРНИЗАЦИЯ: Вызов гистограммы из adc_plot ---
        # Эта функция построит распределение интервалов dt между замерами
        adp.plot_sampling_period_hist(timestamps)

    except KeyboardInterrupt:
        print("\nПрервано пользователем.")

    finally:
        # Явный вызов деструктора для очистки GPIO
        if adc is not None:
            del adc
        print("Работа завершена.")

if __name__ == "__main__":
    main()
