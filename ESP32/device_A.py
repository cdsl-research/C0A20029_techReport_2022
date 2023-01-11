import utime
import socket
import _thread
import network
from machine import Pin
from password import *

SSID_NAME_LAB = ["CDSL-A910-11n"]
SSID_ESP = {"ESP_D38A19"} #ノードB

p2 = Pin(2,Pin.OUT)
red = Pin(13, Pin.OUT)
blue = Pin(4, Pin.OUT)
green = Pin(5, Pin.OUT)

wifiStatus = True
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

port = 80

def A():
    global host
    global port
    key = "request"

    host = wifi.ifconfig()[2] #怪しい
    s = socket.socket()
    s.connect(socket.getaddrinfo(host,port)[0][-1])
    utime.sleep(5)
    s.send(key)
    s.accept()
    msg = s.recv(1024)
    print(msg.decode("utf-8"))
    wifi.disconnect()
    p2.off()

def wifiscan():
    global wifi
    wifiList = wifi.scan()
    wifiAPDict = []
    for wl in wifiList:
        if wl[0].decode("utf-8") != "":
            wifiAPDict.append(wl[0].decode("utf-8"))
    return wifiAPDict

def connect_lab_wifi(timeout = 10):
    global wifi
    if wifi.ifconfig()[0].split(".")[0] == "192":
        wifi.disconnect()
    else:
        pass
    
    endFlag = False
    wifiName = wifiscan()
    print(wifiName)

    for wn in wifiName:
        if wn in SSID_NAME_LAB:
            print(f"[{wn}]に接続します")
            wifi.connect(wn, lab_wifi_pass)
            while True:
                
                if wifi.ifconfig()[0].split(".")[0] == "192":
                    p2.on()
                    endFlag = True
                    print("----  wifi is connected -----")
                    print(f"----[{wifi.ifconfig()[0]}]に接続----")
                    webrepl.start(password = webrepl_pass)
                    break
                else:
                    utime.sleep(1)
            if endFlag == True:
                break
        if endFlag == True:
            break

def connect_esp_wifi(timeout = 10):
    global wifi
    if wifi.ifconfig()[0].split(".")[0] == "192":
        wifi.disconnect()
    else:
        pass
    
    wifiName = wifiscan()
    print(wifiName)

    for wn in wifiName:
        if wn in SSID_ESP:
            print(f"---ESPのWi-Fi[{wn}]に接続します---")
            wifi.connect(wn)
            while True:

                if wifi.ifconfig()[0].split(".")[0] == "192":
                    p2.on()
                    endFlag = True
                    print("---- wifi is connected ----")
                    print(f"----[{wifi.ifconfig()[0]}]に接続----")
                    return True

                else:
                    utime.sleep(1)
            if endFlag == True:
                break
        if endFlag == True:
            break



def main():
    while True:
        connect_esp_wifi()
        A()
        utime.sleep(10)


if __name__ == "__main__":
    main()



