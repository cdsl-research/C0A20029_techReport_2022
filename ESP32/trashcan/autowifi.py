

import webrepl
from machine import Pin
import machine
import network
import utime
SSID_NAME_AUTO = ["CDSL-A910-11n", "Buffalo-G-4A30", "Xperia1234"]
SSID_PASS_AUTO = {"CDSL-A910-11n": "11n-ky56$HDxgp"}


N = ''

p2 = Pin(2, Pin.OUT)
red = Pin(13, Pin.OUT)
blue = Pin(4, Pin.OUT)
green = Pin(5, Pin.OUT)

wifiStatus = True

wifi = network.WLAN(network.STA_IF)
wifi.active(True)


def wifiscan():
    global wifi
    wifiList = wifi.scan()
    wifiAPDict = []
    for wl in wifiList:
        if wl[0].decode("utf-8") != "":
            wifiAPDict.append(wl[0].decode("utf-8"))
    
    return wifiAPDict


# APに接続する場合
def connect_wifi(ssid, passkey, timeout=10):
    count = 0
    while count < 3:
        try:
            wifi.connect(ssid, passkey)
            break
        except:
            utime.sleep(3)
            count += 1
    while not wifi.isconnected() and timeout > 0:
        print('.')
        utime.sleep(1)
        timeout -= 1

    if wifi.isconnected():
        p2.on()
        print(ssid, 'Connected')
        webrepl.start(password='cdsl')
        return wifi
    else:
        print(ssid, 'Connection failed!')
        return ''


def main():
    global wifi
    flag_end = False
    wifiName = wifiscan()
    print(wifiName)
    endFlag = False
    if SET_AP == True:
        for wn in wifiName:
            if wn in SSID_NAME_AUTO:
                #print(f"--- 研究室のWi-Fi ---")
                print(f"[{wn}]に接続します")
                while True:
                    wifi = connect_wifi(wn, SSID_PASS_AUTO[wn])
                    if wifi.ifconfig()[0].split(".")[0] == "192":
                        endFlag = True
                        print("----  wifi is connected -----")
                        print(f"----[{wifi.ifconfig()[0]}]に接続----")
                        break
                    else:
                        utime.sleep(1)
                if endFlag == True:
                    break
            if endFlag == True:
                break
    else:
        print("--- ESP Wi-Fi ---")
        for w in wifiName:
            for ssid in espSsidList:
                if w == ssid:
                    print(f"[{ssid}]に接続",end="")
                    #wifi = esp_connect_wifi("w")
                    wifi = network.WLAN(network.STA_IF)
                    wifi.active(True)
                    wifi.connect(ssid)
                    count = 0
                    for _ in range(10):
                        if wifi.isconnected():
                            p2.on()
                            print(f"接続完了\n>>>>>>{wifi.ifconfig()}")
                            flag_end = True
                            break
                        else:
                            print(" . ",end="")
                            utime.sleep(0.5)
                    if flag_end == True:
                        break
            if flag_end == True:
                print("autowifi.pyを終了します")
                break
            
    
        
                            
if __name__ == "__main__":
    while True:
        if wifi.ifconfig()[0].split(".")[0] == "192":
            print("autowifi.pyを終了します")
            break
        else:
            print("再度Wi-Fiのスキャンを実行")
            main()
    
