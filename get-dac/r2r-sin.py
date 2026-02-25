import r2r_dac as r2r
import signal_generator as sg
import time

# Параметры сигнала
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

try:
    # Создаём объект R2R ЦАП
    dac = r2r.R2RDAC()

    print(f"Генерация синусоиды: {signal_frequency}Гц, амплитуда {amplitude}В, "
          f"дискретизация {sampling_frequency}Гц")

    while True:
        # Текущее время
        current_time = time.time()

        # Амплитуда синусоиды (0..1)
        sin_amplitude = sg.get_sin_wave_amplitude(signal_frequency, current_time)

        # Напряжение = амплитуда * коэффициент
        voltage = amplitude * sin_amplitude

        # Выдаём на ЦАП
        dac.set_voltage(voltage)

        # Ждём период дискретизации
        sg.wait_for_sampling_period(sampling_frequency)

except KeyboardInterrupt:
    print("\nОстановка генератора по Ctrl+C")

finally:
    # Закрываем ЦАП
    dac.deinit()
    print("ЦАП отключён")
