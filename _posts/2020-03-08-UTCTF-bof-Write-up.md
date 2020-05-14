---
layout: post
title: "2020 UTCTF bof * Write up"
excerpt: "굉장히 간단했던 문제"
date: 2020-03-08
categories: [system, ctf]
comments: true 
---

포너블을 공부해봐야겠다고 생각한 이후로 처음으로 CTF에서 문제를 푼 것 같지만... 너무 쉬운 문제라 별로 감흥이 없다.

이전 워게임들이 더 어려운 것 같다.

아무튼.. 그래도 기념삼아,,

binay :



![img](https://k.kakaocdn.net/dn/ca20p9/btqCAP8j4mh/niK9o76AvgHidgKihHxvwK/img.png)



여기서부터 RTL의 느낌이 강하다고 생각했다.

main.c :



![img](https://k.kakaocdn.net/dn/byzezV/btqCtYfldoP/kzCaIlQmKLWP3KTTSC9PZ1/img.png)



get_flag :



![img](https://k.kakaocdn.net/dn/zGFKs/btqCuYMS5ZG/HBgMEz6nLKTuUGw2n9XMB1/img.png)



a1값이 죽은소고기가 되면 해결인데 main이랑 호출관계가 없다. -> RTL

exploit :



![img](https://k.kakaocdn.net/dn/PB9O8/btqCy4yp1up/5jvuYhDRUSBrZHqaFE1De1/img.png)



0x4005ea는 get_flag의 주소이고, 0x400693은 pop_rdi; ret 로 rop가젯이다. 그리고 그 뒤에 인자로 죽은소고기를 넣고 get_flag를  실행

main에서 바로 get_flag를 호출할 수  없고, get_flag를 호출하기 전에 a1값에 인자로 죽은소고기를 넣어줘야하기 때문에 ropgadget이 사용된다. 

페이로드의 순서구성이 저런 이유는 우선 더미와 sfp를 채우고, pop_rdi에서 인자를 먼저 던져줘야 다음 리턴하면서 get_flag에 적절한 반응

x64 익스는 거의 오랜만인데,, dummy(112)+sfp(8)+ret(6)이라고 한다.. 

p.s

rop에 대하여 더 자세히 공부할 예정이다.  

그리고 지금까지 gdb나 ida에서 하나하나 주소를 알아냈는데 그냥 pwntools에서

e.ELF("pwnable")

flag_addr = e.symbols["get_flag"] 하면 알아서 get_flag의 주소가 따인다. 앞으로 잘 써먹어야겠다.
