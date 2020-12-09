from socket import *
from ourAES_lib import *
# (A)
# AF_INET = ipv4
#sock_STREAM : tcp etc..
server_socket = socket(AF_INET,SOCK_STREAM)

# error
server_socket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

# (B)
server_socket.bind(('127.0.0.1',7878))

# (C)
server_socket.listen()

# (D)
print ("[*] Waiting Connection ...")
client_socket,addr = server_socket.accept()

#=====================connect=============================

key = [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff]

#Receive from client
data = client_socket.recv(1024)
print("\n[*] Received data : ",data.decode())

#bytes -> string
enc_string = data.decode()
print("\n[*] enc_string : ",enc_string)

#string -> block
enc_block = str2block(enc_string)
print("\n[*] enc_block : ",enc_block)

#Decryption
print("\n[*] Decryption now!")
result_block = ECB_Dec(enc_block,key)

print("\n[*] Recovered Plaintext : ")
for i in range(len(result_block)):
	print(chr(result_block[i]), end=' ')
print("")

#====================disconnect============================
# (E)
client_socket.close()
server_socket.close()
