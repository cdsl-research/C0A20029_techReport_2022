#サーバに直接繋がるノード用boot.py
#研究室wifiに自動で接続される

import network
import machine
from machine import Pin, SoftI2C
import utime
import webrepl

ap_flag = False
machine.freq(240000000)


Lab_or_ESP = True #Trueの時は研究室wifiに接続を試みる

red = Pin(13, Pin.OUT)
blue = Pin(4, Pin.OUT)
green = Pin(5, Pin.OUT)

p21 = Pin(21, Pin.IN, Pin.PULL_UP)
p22 = Pin(22, Pin.IN, Pin.PULL_UP)
p2 = Pin(2, Pin.OUT)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

ap = None

ID = machine.unique_id()
listenSocket = None


print("boot is ok")
utime.sleep(1)

#execfile("esp_dev.py")
#connect_lab_wifi()

