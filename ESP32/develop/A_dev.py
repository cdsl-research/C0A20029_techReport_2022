
import utime
import socket
import _thread
import network

sensor_data = "20221226 000000 00.00"
count = 1
label = "A"
add_ip = ""
port = 80

wifiStatus = True

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

def receive_socket():
    global conn
    global addr
    global listenSocket
    global port

    listenSocket = socket.socket()
    listenSocket.bind(('', port))
    listenSocket.listen(5)
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    print('tcp waiting...')

def receive_data():
    #---データ待ち---
    while True:
        print("accepting.....ソケット通信待機中......")
        conn, addr = listenSocket.accept()
        
        add_ip = addr[0]
        data = conn.recv(1024)
        #conn.close()
        str_data = data.decode()
        print(f"{addr} からの接続 ---> 受信データ : {str_data}")

        if len(str_data) != 0:
            wifi.disconnect()
            p2.off()
            print(f"受信したデータ : {str_data}")
            str_data = ""

def a_dev():
    #espのwi-fiに接続
    if wifi.ifconfig()[0].split(".")[0] != "192":
        connect_esp_wifi()
        print("connected to esp wi-fi")

    utime.sleep(5)
    #キー送信
    key = "request"
    message(key)
    print("sent key")

def main():
    while True:
        a_dev()
        for i in range(5):
            print(".")

if __name__ == "__main__":
    main()