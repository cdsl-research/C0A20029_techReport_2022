
import utime
import socket
import _thread

sensor_data = ("20230111 000000 00.00")
count = 1
label = "B"
key = ""
add_ip = ""
msg = label + str(count) + "," + sensor_data

def receive_socket():
    global conn
    global addr
    global listenSocket
    port = 8080

    listenSocket = socket.socket()
    listenSocket.bind(('', port))
    listenSocket.listen(5)
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    print('tcp waiting...')

    #---データ待ち---
    while True:
        print("accepting.....ソケット通信待機中......")
        conn, addr = listenSocket.accept()
        
        add_ip = addr[0]
        data = conn.recv(1024)
        #conn.close()
        str_data = data.decode()
        print(f"{addr} より接続 ---> 受信データ : {str_data}")

        #キーマッチング
        if str_data == "request":
            s = socket.socket()
            port = 8080
            print(add_ip, port)
            utime.sleep(5)

            #キーの送信元に接続
            s.connect(socket.getaddrinfo(add_ip,port)[0][-1])
            print(f"{socket.getaddrinfo(add_ip,port)[0][-1]}に接続")

            #データ送信
            print(f"送信データ : {msg}")
            s.send(msg)
            s.close()
            print("sent data")
            #esp_dev.ap_off()
            utime.sleep(10)
        else:
            pass

def b_dev():
    global key
    global ap_flag
    #apモード起動
    print(ap_flag)
    if ap_flag == False:
        ap_flag = True
        ap_mode()

def main():
    _thread.start_new_thread(receive_socket,())

    for i in range(2):
        b_dev()

if __name__ == "__main__":
    main()