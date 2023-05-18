import numpy as np
from matplotlib import pyplot
from textwrap import wrap
import matplotlib.ticker as ticker

with open('settings.txt') as f:
    d = float(f.readline())
    k = float(f.readline())

#Перевод показаний в вольты и секунды
data = np.loadtxt('data.txt', dtype = int) * k
time = np.array([i*d for i in range(data.size)])

fig, ax = pyplot.subplots(figsize=(16, 10), dpi=500)

#Настройка внешних параметров
ax.plot(time, data, c = 'black', linewidth = 1, label = 'U(t)')
ax.scatter(time[0:data.size:20], data[0:data.size:20], marker = 'd', c = 'red', s = 50)
ax.legend(shadow = False, loc = 'upper right', fontsize = 25)

#Максимальные и минимальные значения шкалы
ax.axis([data.min(), time.max(), data.min(), data.max()+0.2])

#Подпись осей
ax.set_ylabel("Напряжение, В", fontsize ='x-large')
ax.set_xlabel("Время, с", fontsize ='x-large')

#Название графика
ax.set_title("\n".join(wrap('Процесс заряда и разряда конденсатора в RC-цепочке', 70)), loc = 'center', fontsize ='xx-large')

#Настройка сетки
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))

ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

ax.grid(which='major', color = 'black')
ax.minorticks_on()
ax.grid(which='minor', color = 'gray', linestyle = ':')

#Время заряда и разряда
z_time = data.argmax() * d
r_time = len(data) * d - z_time
pyplot.text(8, 2.05, f'Время заряда = {round(z_time, 2)}c', fontsize ='x-large')
pyplot.text(8, 1.9, f'Время разряда = {round(r_time, 2)}c', fontsize ='x-large')

#Сохранение в svg
fig.savefig('graph.png')
fig.savefig('graph.svg')
