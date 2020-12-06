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

#key shared!
key = [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff]

key_state = block2state(key) 
print("\n[*] key=")
hex_print(key_state)

#recv
data = client_socket.recv(1024)
print("\n[*] Received data =",data.decode())

####### bytes -> string -> block -> state

#byte to string
enc_string = data.decode()
print("\n[*] enc_stirng = ")
print(enc_string)

#string to block
enc_block = str2block(enc_string)
print("\n[*] enc_block =")
hex_block_print(enc_block)


#block to state
enc_state = block2state(enc_block)
print("\n[*] enc_state=")
hex_print(enc_state)

######### Decryption ####################
print("\n[*] Decryption!!!")
result_state= AES_Dec(enc_state ,key_state)

print("\n[*] Recovered Plaintext =")
hex_print(result_state)

#====================disconnect============================
# (E)
client_socket.close()
server_socket.close()
