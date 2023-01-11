#メッセージ送信
#データ送信側
import socket

s = socket.socket()
host = "192.168.4.2"
port = 80

s.connect(socket.getaddrinfo(host, port)[0][-1])

if __name__ == '__main__':
    while True:
        
        #msg = input("--->>>")
        msg = "message was sent successfully"
        s.sendall(msg)
    