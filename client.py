from socket import *
from ourAES_lib import *
# (A) socket()
client_socket = socket(AF_INET, SOCK_STREAM)

# (B) connect()
client_socket.connect(('127.0.0.1',7878))

#==================connect====================
block = [0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f]

key = [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff]

in_state = block2state(block)
key_state = block2state(key)

print("\n[*] plaintext = ")
hex_print(in_state)

print("\n[*] key = ")
hex_print(key_state)

###### Encryption ######
print("\n[*] Encryption!!!")
enc_state = AES_ENC(in_state, key_state)
print("\n[*] ciphertext = ")
hex_print(enc_state)

###### state -> block -> string -> bytes

#state to block
enc_block = state2block(enc_state)
print("\n[*] enc_block= ")
hex_block_print(enc_block)

#block to string
enc_string= block2str(enc_block)
print("\n[*] enc_string = ")
print(enc_string)

#string to bytes
data = enc_string.encode()
print("\n[*] data = ")
print (data)

###### send ######
print("\n[*] send!!")
client_socket.sendall(data)

#===============disconnect=======================
# (C)
client_socket.close()
