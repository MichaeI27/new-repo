import matplotlib.pyplot as plt

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
