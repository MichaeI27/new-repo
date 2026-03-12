import matplotlib.pyplot as plt

def plot_sampling_period_hist(time_values):
    # Проверка на наличие данных (минимум 2 точки для расчета интервала)
    if len(time_values) < 2:
        print("Недостаточно данных для построения гистограммы")
        return

    # Расчет интервалов между измерениями (dt)
    sampling_periods = [time_values[i+1] - time_values[i] for i in range(len(time_values) - 1)]

    plt.figure(figsize=(10, 6))
    plt.hist(sampling_periods, bins=50, color='skyblue', edgecolor='black')

    plt.title("Распределение периодов дискретизации (jitter)")
    plt.xlabel("Интервал времени между измерениями [с]")
    plt.ylabel("Количество измерений")

    # Устанавливаем разумный предел по X, чтобы видеть основной пик
    plt.xlim(0, 0.06)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

def plot_voltage_vs_time(time_values, voltage_values, max_voltage):
    if not time_values or not voltage_values:
        print("Нет данных для построения графика напряжения")
        return

    plt.figure(figsize=(10, 6))

    # ИСПРАВЛЕНО: добавлен label, чтобы plt.legend() не выдавал ошибку
    plt.plot(time_values, voltage_values, label='Напряжение U(t)', color='blue', linewidth=1.5)

    plt.title("Зависимость напряжения от времени")
    plt.xlabel("T, с")
    plt.ylabel("U, В")

    # Задаем границы по осям
    plt.xlim(0, max(time_values))
    plt.ylim(0, max_voltage + 0.5)

    plt.grid(True, linestyle=':', alpha=0.6)

    # Теперь легенда будет работать правильно
    plt.legend()

    plt.show()
