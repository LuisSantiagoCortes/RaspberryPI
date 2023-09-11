import socket

ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ainfo = socket.getaddrinfo('192.168.0.8',1234)
ms.bind(ainfo[0][4])
ms.listen(5)
               
conn, addr = ms.accept()
data = conn.recv(1000)
print(data)
conn.close()
ms.close()
   
#   c, addr = s.accept()     
#   print 'Got connection from', addr
#   c.send('Got a request!')
#   c.close() 
