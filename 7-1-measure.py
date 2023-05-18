import RPi.GPIO as GPIO
import time
from matplotlib import pyplot

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
bits = len(dac)
levels = 2 ** bits
maxVoltage = 3.3
comp = 4
troyka = 17
comparatorValue = 0
start = 0

GPIO.setup(dac, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(leds, GPIO.OUT)
GPIO.output(dac, 0)
GPIO.output(leds, 0)

def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def num2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal

def adc():
    res = 0
    for value in range(7, -1, -1):
        res += 2**(value)
        num2dac(res)
        time.sleep(0.005)
        comparatorValue = GPIO.input(comp)
        if comparatorValue == 0:
            res -= 2**value
    return res 

try:
    GPIO.setup(troyka, GPIO.OUT, initial=GPIO.LOW)
    result = []
    counter = 0
    start = time.time()
    value = 0
    GPIO.output(leds, decimal2binary(value))
    print("Началась зарядка")
    #зарядка
    while value < 255*0.95:
        value = adc()
        GPIO.output(leds, decimal2binary(value))
        result.append(value)
        counter+=1
        print(value*3.3/256)
    
    GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
    print("Закончилась разрядка")
    #разрядка
    while value > 256*0.02:
        value = adc()
        GPIO.output(leds, decimal2binary(value))
        result.append(value)
        counter+=1
        print(value*3.3/256)
    
    finish = time.time()
    experiment = finish - start
    #запись данных в файл
    with open('data.txt', 'w') as f:
        for i in range(counter):
            f.write(str(result[i]))
            f.write('\n')

    with open('settings.txt', 'w') as f:
        d = counter/experiment
        k = 3.3/256
        f.write(str(d)+ '\n')
        f.write(str(k) + '\n')

    print("Продолджительность эксперимента ")
    print(experiment)
    print("Период одного измерения ")
    print(experiment/counter)
    print("Частота дискретизации ")
    print(d)
    print("Шаг квантования АЦП ")
    print(k)

    #график
    y = [i/256*3.3 for i in result]
    x = [i*experiment/counter for i in range(counter)]
    pyplot.plot(x,y)
    pyplot.xlabel('время')
    pyplot.ylabel('вольтаж')
    pyplot.show()

finally:
    GPIO.output(leds, 0)
    GPIO.output(dac, 0)
    GPIO.cleanup()



    
