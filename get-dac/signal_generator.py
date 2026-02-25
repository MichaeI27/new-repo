import numpy as np
import time

def get_sin_wave_amplitude(freq, time):
    """
    Возвращает нормализованную синусоиду (0..1) для заданной частоты и времени
    """
    sin_value = np.sin(2 * np.pi * freq * time)
    # Сдвиг -1..1 → 0..2, затем нормировка → 0..1
    normalized = (sin_value + 1) / 2
    return normalized

def wait_for_sampling_period(sampling_frequency):
    """
    Ждёт один период дискретизации для точной частоты дискретизации
    """
    period = 1.0 / sampling_frequency
    time.sleep(period)
