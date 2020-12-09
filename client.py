from socket import *
from ourAES_lib import *
# (A) socket()
client_socket = socket(AF_INET, SOCK_STREAM)

# (B) connect()
client_socket.connect(('127.0.0.1',7878))

#==================connect====================

plaintext = 'welcome to eureka porject!'
pt_block = []

for i in range(len(plaintext)):
	pt_block.append(ord(plaintext[i]))

#keyshared!
key = [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff]

#Encryption
print("\n[*] Encryption now!")
enc_block = ECB_Enc(pt_block,key)
print("\n[*] Ciphertext : ")

for i in range(len(enc_block)):
	print(enc_block[i], end =' ')
print("")

#block -> string
enc_string = block2str(enc_block)
print("\n[*] enc_string : ", enc_string)

#string -> bytes
data = enc_string.encode()
print("\n[*] data : ",data)

#send to server
print("\n[*] Send to server!")
client_socket.sendall(data)

#===============disconnect=======================
# (C)
client_socket.close()
