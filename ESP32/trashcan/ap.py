#アクセスポイントモード起動
import network
import socket
import wifi

ap = None
port = 80
listenSocket = None

ip = wifi.ifconfig()[0]
listenSocket = socket.socket()
listenSocket.bind((ip,port))
listenSocket.listen(5)
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def main():
    global ap
    ap = network.WLAN(network.AP_IF)

    ap.active(True)
    SSID = ap.config("essid")
    print(SSID)

    while True:
        print("accepting......")
        conn, addr = listenSocket.accept() #受信待機中
        print(addr, "connected") 

        while True:
            data = conn.recv(1024)
            if data == "request": #リクエストが飛んで来たら
                s = socket.socket()
                host = addr
                port = 80

                s.connect(socket.getaddrinfo(host, port)[0][-1])

                #メッセージ(データ)を送る
                msg = "message was sent successfully"
                s.sendall(msg)

            elif(len(data) == 0): #送られてきたメッセージ長が0だったらソケット通信終了
                print("close socket")
                conn.close()
                break

if __name__ == "__main__":
    main()