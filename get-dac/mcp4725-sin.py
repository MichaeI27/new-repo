import mcp4725_driver as mcp
import signal_generator as sg
import time

# Параметры сигнала
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

try:
    # Создаём объект MCP4725 ЦАП (диапазон 0-5В)
    dac = mcp.MCP4725(dynamic_range=5.0)

    print(f"Генерация синусоиды MCP4725: {signal_frequency}Гц, амплитуда {amplitude}В, "
          f"дискретизация {sampling_frequency}Гц")

    while True:
        # Текущее время
        current_time = time.time()

        # Амплитуда синусоиды (0..1)
        sin_amplitude = sg.get_sin_wave_amplitude(signal_frequency, current_time)

        # Напряжение = амплитуда * коэффициент
        voltage = amplitude * sin_amplitude

        # Выдаём на MCP4725 ЦАП
        dac.set_voltage(voltage)

        # Ждём период дискретизации
        sg.wait_for_sampling_period(sampling_frequency)

except KeyboardInterrupt:
    print("\nОстановка MCP4725 генератора по Ctrl+C")

finally:
    # Закрываем MCP4725 ЦАП
    dac.deinit()
    print("MCP4725 ЦАП отключён")
