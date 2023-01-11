#apモードのノードに接続する
import network

wifi = None

def connect():
    global wifi
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    #wifi.connect("ESP_D356F5")
    wifi.connect("ESP_D38A19") #適宜書き換える
    wifi.ifconfig()

if __name__ == "__main__":
    connect()
    print(f"[{ssid}]に接続",end="")
    execfile("server.py")