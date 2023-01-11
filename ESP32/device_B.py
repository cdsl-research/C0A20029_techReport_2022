import socket
import _thread
import network
import machine
from machine import Pin
from password import *


p2 = Pin(2,Pin.OUT)
red = Pin(13, Pin.OUT)
blue = Pin(4, Pin.OUT)
green = Pin(5, Pin.OUT)

port = 80

wifiStatus = True
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

socket_to_A = None
address = None
msg = "20230111 01"


def B():
    global port
    global socket_to_A
    global address
    global msg

    s = socket.socket()
    s.bind(("", port))
    s.listen(5)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    while True:
        socket_to_A, address = s.accept()
        print("accepting......")
        print(address[0], "connected")

        while True:   
            key = s.recv(1024)
            print(key.decode("utf-8"))

            if (len(key) != 0):
                print(key)
                socket_to_A.send(msg)
                socket_to_A.close()
                print("sent message")
            break
        break

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

def ap_mode():
    global ap
    ap = network.WLAN(network.AP_IF) #アクセスポイントのインターフェースを作成
    # ap.config(ssid = "ESP-AP") #アクセスポイントのSSIDを設定
    # ap.config(maxclients = 1) #ネットワークに接続できるクライアント数

    ap.active(True) #インターフェースアクティブ化

    green.on()
    config = ap.ifconfig()

    print("enabled ap mode")
    print(config)

def ap_off():
    ap.active(False)
    green.off()

def main():
    while True:
        ap_mode()
        B()
        ap_off()
        utime.sleep(10)
        

if __name__ == "__main__":
    main()

