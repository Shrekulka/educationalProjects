import socket

target_host = "127.0.0.1"
target_port = 9997

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# отправляем какие-нибудь данные, передать ей данные и сервер, которому вы хотите их отправить.
client.sendto(b"AAABBBCCC", (target_host, target_port))

# принимаем какие-нибудь данные
# Поскольку протокол UDP не поддерживает соединения, перед взаимодействием нет вызова connect(). В конце нужно вызвать
# recvfrom(), чтобы получить ответные UDP-данные.
data, adr = client.recv(4096)

print(data.decode())
client.close()
