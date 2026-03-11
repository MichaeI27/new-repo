import matplotlib.pyplot as plt

def plot_sampling_period_hist(time):
    sampling_periods = [time[i+1] - time[i] for i in range(len(time) - 1)]

    plt.figure(figsize=(10, 6))

    plt.hist(sampling_periods, bins=50, color='skyblue', edgecolor='black')

    plt.title("Распределение периодов дискретизации")
    plt.xlabel("Интервал времени между измерениями [с]")
    plt.ylabel("Количество измерений")

    plt.xlim(0, 0.06)

    plt.grid(True, linestyle='--', alpha=0.7)

    plt.show()

def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10, 6))

    plt.plot(time, voltage, label='Measured Voltage')

    plt.xlabel("T, с")
    plt.ylabel("U, В")

    plt.xlim(0, max(time) if time else 1)
    plt.ylim(0, max_voltage + 0.5)

    plt.grid(True)

    plt.legend()

    plt.show()
