import http.client

conn = http.client.HTTPSConnection("www.uci.edu")
conn.request("GET", "/")
r1 = conn.getresponse()
print(r1.status, r1.reason)
data1 = r1.read()
print(data1)
conn.close()

#referencia = https://docs.python.org/3/library/http.client.html
