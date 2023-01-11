import network
import utime
import webrepl
import socket
import machine
from machine import Pin
from password import *

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

#wifiをスキャンしてessidをリスト化
def wifiscan():
    global wifi
    wifiList = wifi.scan()
    wifiAPDict = []
    for wl in wifiList:
        if wl[0].decode("utf-8") != "":
            wifiAPDict.append(wl[0].decode("utf-8"))
    return wifiAPDict

#研究室wifiに接続する
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
    
#ESPwi-fiに接続する
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

#APモード起動
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

#APモード停止
def ap_off():
    ap.active(False)
    green.off()

#データ送信
def send_data(data):
    
    s = socket.socket() #ソケットを作成
    host = wifi.ifconfig()[2]
    port = 80

    s.connect(socket.getaddrinfo(host,port)[0][-1])

    utime.sleep(5)

    s.send(data)
    s.close()

#ソケット通信初期化
def init_socket():
    global listenSocket
    port = 80

    listenSocket = socket.socket() #1回限り ソケットを作成 2回目は再定義
    listenSocket.bind(("",port)) #ソケットを特定のIpアドレスとポートに紐づけ ここから↓が2回やるとエラー
    listenSocket.listen(5) #接続の待ち受けを開始
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #指定されたソケットオプションの値を設定
    print("初期化済み")
    print(type(listenSocket))
    return listenSocket
    
def received_socket():
    global listenSocket
    port = 80

    listenSocket = socket.socket()
    listenSocket.bind(('', port))
    listenSocket.listen(5)
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    print('tcp waiting...')
    while True:
        print("accepting.....ソケット通信待機中......")
        conn, addr = listenSocket.accept()
        addr = addr[0]
        add_ip = addr[0]
        data = conn.recv(1024)
        key  = conn.recv(1024)
        conn.close()
        str_data = data.decode()
        key = key.decode()
        print(f"{addr} より接続 ---> 受信データ : {str_data}")
    
#データ受信
def receive_data(timeout=2):

    count = 0
    while count < timeout:
        # tryの中でエラーがおきたらexcept
        try:
            print("accepting......")
            print(type(listenSocket))
            conn, addr = listenSocket.accept()
            #addr = listenSocket.accept()[0] #受信待機中
            print(addr[0], "connected") #接続した相手のipアドレスを表示

            data = conn.recv(1024)
            if(len(data) != 0):
                conn.close()
                data = data.decode()
                
                print(data, type(data))
                print("データを受信しました")
            else:
                pass
            break

        except Exception as e:
            count += 1
            print(f"count : {count}  receive_data()内のエラー")
            print(e)
            pass
                

#データ受信改
def receive():
    port = 80
    listenSocket = None
    while True:
        print("accepting......")
        conn, addr = listenSocket.accept() #接続を受信
        print(addr, "connected")

        while True:
            data = conn.recv(1024)
            if(len(data) != 0):
                print("close socket")
                conn.close()
                break
            print(data)

#キーワードマッチング用
def matching():
    while True:
        
        print("accepting......")
        conn, addr = listenSocket.accept() #受信待機中
        add_ip = addr[0] #送信先ipアドレスを取得(add_ip)
        print(add_ip, "connected")

        while True:
            data = conn.recv(1024) #受信データ
            data = data.decode()
            print(data)
            if data == "request":
                return add_ip
            else:
                pass
        
            # conn.close() #コネクションclose
            # data = data.decode() #受信データをデコード
            # print(data)
            # print(type(data))
            # return data ,add_ip #受信メッセージと送信先ipアドレスを返す

#タイマー
def timer(time):
    utime.sleep(time)

#-------------------------------------
#データを受信するだけ(接続確認用)
def socket_accept():
    
    port = 80
    listenSocket = None

    ip = wifi.ifconfig()[0]
    listenSocket = socket.socket()
    listenSocket.bind((ip,port))
    listenSocket.listen(5)
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    while True:
        
        print("accepting......")
        conn, addr = listenSocket.accept() #受信待機中
        print(addr[0], "connected")

        while True:
            data = conn.recv(1024)
            if(len(data) == 0):
                print("close socket")
                conn.close()
                break
            print(data)
            

#データを送信するだけ(接続確認用)
def message(msg):
    
    s = socket.socket()
    host = wifi.ifconfig()[2]
    port = 80

    s.connect(socket.getaddrinfo(host,port)[0][-1])

    s.sendall(msg)
#-------------------------------------

#csvファイル書き込み(新規作成)
def writeFile(text,number):
    data = text + "," + str(number) + "\n"
    filename = "ktest.csv"
    f = open(filename,"a")
    f.write(data)
    f.close()

def main():
    print("hello")

if __name__ == "__main__":
    main()