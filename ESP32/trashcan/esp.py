import network
import machine
import utime
import webrepl
import socket
import password 

SSID_NAME_LAB = ["CDSL-A910-11n"]
SSID_ESP = {"ESP_D38A19"} #ノードB

N = ""

p2 = Pin(2,Pin.OUT)
red = Pin(13, Pin.OUT)
blue = Pin(4, Pin.OUT)
green = Pin(5, Pin.OUT)

wifiStatus = True

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

ap = None
port = 80
listenSocket = None

ip = wifi.ifconfig()[0]
listenSocket = socket.socket()
listenSocket.bind((ip,port))
listenSocket.listen(5)
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

#wifiをスキャンしてessidをリスト化
def wifiscan():
    global wifi
    wifiList = wifi.scan()
    wifiAPDict = []
    for wl in wifiList:
        if wl[0].decode("utf-8") != "":
            wifiAPDict.append(wl[0].decode("utf-8"))
    return wifiAPDict

#研究室wifiに接続する場合
def connect_lab_wifi(timeout = 10):
    global wifi
    wifiName = wifiscan()
    print(wifiName)

    for wn in wifiName:
        if wn in SSID_NAME_LAB:
            print(f"---研究室のWi-Fi[{wn}]に接続します---")
            count = 0
            while count < 3:
                try:
                    wifi.connect(wn,lab_wifi_pass)
                    break
                except:
                    utime.sleep(3)
                    count += 1
            while wifi.ifconfig()[0].split(".")[0] != "0": #wifiに繋がっていない間
                print(".")
                utime.sleep(1)
                timeout -= 1
                if wifi.ifconfig()[0].split(".")[0] == "192": #wifiに繋がったら
                    p2.on()
                    print(wn,"Connected")
                    print(f"---[{wifi.ifconfig()[0]}]に接続---")
                    webrepl.start(webrepl_pass)
                    return wifi
                else:
                    print(wn, "Connection Failed")
                    return ""
    
#ESPに繋げる場合
def connect_esp_wifi(timeout = 10):
    global wifi
    wifiName = wifiscan()
    print(wifiName)

    for wn in wifiName:
        if wn in SSID_ESP:
            print(f"---ESPのWi-Fi[{wn}]に接続します---")
            count = 0
            while count < 3:
                try:
                    wifi.connect(wn)
                    break
                except:
                    utime.sleep(3)
                    count += 1
            while wifi.ifconfig()[0].split(".")[0] == "0": #wifiに繋がっていない間
                print(".")
                utime.sleep(1)
                timeout -= 1

            if wifi.ifconfig()[0].split(".")[0] == "192": #wifiに繋がったら
                p2.on()
                print(wn, "Connected")
                print(f"---[{wifi.ifconfig()[0]}]に接続---")
                return wifi
            else:
                print(wn, "Connection Failed")
                return ""

def accept():
    global ap
    port = 80
    listenSocket = None
    ap = network.WLAN(network.AP_IF)

    ip = wifi.ifconfig()[0]
    listenSocket = socket.socket()
    listenSocket.bind((ip,port))
    listenSocket.listen(5)
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    ap.active(True)
    SSID = ap.config("essid")
    print(SSID)

    while True:
        print("accepting......")
        conn, addr = listenSocket.accept() #受信待機中
        print(addr, "connected")

        while True:
            data = conn.recv(1024)
            print(data)

if __name__ == "__main__":
    print("hello")



