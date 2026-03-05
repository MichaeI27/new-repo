import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage):
    # Создаем окно для отображения графика
    plt.figure(figsize=(10, 6))

    # Размещаем график зависимости напряжений от времени
    plt.plot(time, voltage, label='Measured Voltage')

    # Задаем название графика и осей
    # plt.title("Зависимость напряжения от времени")
    plt.xlabel("T, с")
    plt.ylabel("U, В")

    # Задаем границы по осям X и Y
    plt.xlim(0, max(time) if time else 1)
    plt.ylim(0, max_voltage + 0.5)

    # Включите отображение сетки
    plt.grid(True)

    # Добавляем легенду
    plt.legend()

    # Отображаем график
    plt.show()
