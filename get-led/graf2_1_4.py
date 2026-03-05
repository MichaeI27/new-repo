import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def process_lab_file(file_path, label, color, heating_range=(100, 300)):
    # 1. Загрузка данных
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    # 2. Обработка времени
    def to_sec(t_str):
        t_obj = datetime.strptime(t_str.strip('" '), '%H : %M : %S')
        return t_obj.hour * 3600 + t_obj.minute * 60 + t_obj.second

    df['Seconds'] = df['Time'].apply(to_sec)
    df['Seconds'] -= df['Seconds'].iloc[0]

    # 3. Линейная аппроксимация на участке нагрева
    # Выбираем диапазон (например, с 100-й по 300-ю секунду), где нагрев линеен
    mask = (df['Seconds'] > heating_range[0]) & (df['Seconds'] < heating_range[1])
    x_reg = df['Seconds'][mask]
    y_reg = df['Value'][mask]

    # Получаем наклон (slope) и свободный член (intercept)
    slope, intercept = np.polyfit(x_reg, y_reg, 1)

    # 4. Построение
    plt.plot(df['Seconds'], df['Value'], label=f'{label} (исходные)', color=color, alpha=0.3)
    plt.plot(x_reg, slope * x_reg + intercept, '--', color=color,
             label=f'Аппроксимация {label}: dT/dt = {slope:.5f} °C/с')

    return slope

plt.figure(figsize=(12, 7))

# Обработка файла 1 (Пустой калориметр)
slope1 = process_lab_file('НужныхОлег1.csv', 'Пустой калориметр', 'blue', (50, 250))

# Обработка файла 2 (С образцом)
slope2 = process_lab_file('НужныхОлег2.csv', 'С образцом', 'red', (50, 250))

plt.title('Анализ скорости нагрева калориметрической системы', fontsize=14)
plt.xlabel('Время $t$, с', fontsize=12)
plt.ylabel('Температура $T, ^\circ C$', fontsize=12)
plt.legend()
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('result_plot.png')
plt.show()

print(f"Производная для опыта 1: {slope1:.5f} C/sec")
print(f"Производная для опыта 2: {slope2:.5f} C/sec")
