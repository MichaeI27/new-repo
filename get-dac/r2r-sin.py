import r2r_dac as r2r
import signal_generator as sg
import time

# Параметры сигнала
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

dec = None

try:
    # Создаём объект R2R ЦАП
    dac = r2r.R2R_DAC(
        gpio_bits=[22, 27, 17, 26, 25, 21, 20, 16],
        dynamic_range=3.183,
        verbose=True



    )

    print(f"Генерация синусоиды: {signal_frequency}Гц, амплитуда {amplitude}В, "
          f"дискретизация {sampling_frequency}Гц")

    while True:
        current_time = time.time()

        sin_amplitude = sg.get_sin_wave_amplitude(signal_frequency, current_time)

        voltage = amplitude * sin_amplitude

        dac.set_voltage(voltage)

        sg.wait_for_sampling_period(sampling_frequency)

except KeyboardInterrupt:
    print("\nОстановка генератора по Ctrl+C")

finally:
    if dac is not None:
        dac.deinit()
        print("ЦАП отключён")
