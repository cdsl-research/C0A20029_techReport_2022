import esp_dev
import utime
import socket
import _thread

#センサーデータ 日付 時間(時分秒) 水量
sensor_data = ("20221220 000000 00.00")
count = 1
label = "B"
key = ""
add_ip = ""



#実行
def B_sequence():
    global key
    global add_ip
    msg = label + str(count) + "," + sensor_data

    #APモード起動
    esp_dev.ap_mode()

    #接続確認メッセージ
    print("accepting......")
    
    #add_ip = addr[0]
    print(add_ip)
    print(add_ip, "connected")
    print(key)

    if key == "request":
        key = ""
        try:
            s = socket.socket()
        except:
            s = socket.socket()
        port = 80
        print(add_ip, port)
        print(f"送信データ  : {msg}")
        utime.sleep(5)
        
        s.connect(socket.getaddrinfo(add_ip,port)[0][-1])
            
        s.send(msg) 
        s.close()
        print("sent data")
        esp_dev.ap_off()
        

def main():
    global count
    global listenSocket
    #listenSocket = esp_dev.init_socket() #初手龍舞

    _thread.start_new_thread(esp_dev.received_socket,())

    print(type(listenSocket))
    while True:
        B_sequence()
        count += 1
        print("completed B_seq")
        utime.sleep(30)
    

if __name__ == "__main__":
    main()