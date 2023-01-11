import esp_dev
import utime

#センサーデータ 日付 時間(時分秒) 水量
sensor_data = ("20221220 000000 00.00")
count = 1
label = "A"

data = label + str(count) + "," + sensor_data


#実行
def A_sequence():
    #esp wifiに接続
    esp_dev.connect_esp_wifi()
    print("connected to esp wifi")

    #キー送信
    utime.sleep(5)
    key = "request"
    esp_dev.message(key)
    print("sent key")

    #データ受信待ち/受信
    esp_dev.receive_data()

    esp_dev.wifi.disconnect()
    esp_dev.p2.off()
    


def main():
    global count
    global listenSocket
    listenSocket = esp_dev.init_socket() #初手龍舞
    print(type(listenSocket))
    while True:
        A_sequence()
        count += 1
        print("completed A_seq")
        utime.sleep(30)
    
        

    

if __name__ == "__main__":
    main()
