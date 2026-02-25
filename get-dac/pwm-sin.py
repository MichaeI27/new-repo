import pwm_dac as pwm
import signal_generator as sg
import time

# Параметры сигнала (аналогично предыдущему заданию)
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

try:
    # Создаём объект PWM ЦАП
    dac = pwm.PWMDAC()

    print(f"Генерация синусоиды PWM: {signal_frequency}Гц, амплитуда {amplitude}В, "
          f"дискретизация {sampling_frequency}Гц")

    while True:
        # Текущее время
        current_time = time.time()

        # Амплитуда синусоиды (0..1)
        sin_amplitude = sg.get_sin_wave_amplitude(signal_frequency, current_time)

        # Напряжение = амплитуда * коэффициент (нормализуем к 0..1 для PWM)
        voltage_normalized = sin_amplitude * (amplitude / 3.3)  # предполагаем 3.3В max

        # Выдаём на PWM ЦАП
        dac.set_voltage(voltage_normalized)

        # Ждём период дискретизации
        sg.wait_for_sampling_period(sampling_frequency)

except KeyboardInterrupt:
    print("\nОстановка PWM генератора по Ctrl+C")

finally:
    # Закрываем PWM ЦАП
    dac.deinit()
    print("PWM ЦАП отключён")
