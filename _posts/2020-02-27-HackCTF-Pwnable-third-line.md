---

layout: post
title:  "HackCTF Pwnable -  third line"
excerpt: "for All Clear HackCTF"
date:   2020-02-27
categories: [wargame]
comments: true

---

### 1. bof_pie

binary :



![img](https://k.kakaocdn.net/dn/xwtER/btqCpQmF5ON/51YHdf8J6ql75AwsmC2SrK/img.png)문제 이름답게 pie,ㅋㅋㅋ



main은 볼게 없다. 들어가자마자 welcome이 실행됨

welcome :



![img](https://k.kakaocdn.net/dn/ZZEer/btqCrkOkBmO/qv3ckGnT0H8wKqBhcF4oW1/img.png)welcome의 주소를 출력



j0n9hyun :



![img](https://k.kakaocdn.net/dn/r3NUG/btqClzfaKWO/FKH4RafCdOynzsnupWlXJk/img.png)flag를 출력한다.



대충 페이로드가 생각이났다. 근데 PIE가 걸려있어서 base주소로 할 수가없다. 그러므로 welcome_addr에서 welcome_offset을 빼서 base_addr을 구하고 거기에 j0n9hynun_offset을 더해서 j0n9hyun을 실행시킬 것이다.

exploit :



![img](https://k.kakaocdn.net/dn/zF05n/btqCoQtEFi3/a7948tzPFCn5LOmunAiyJk/img.png)bof를 하는데 필요한건 따로 구했다.



### 2. yes or no

binary :

 

 

### 3. RTL_world

binary :



![img](https://k.kakaocdn.net/dn/cOKVh6/btqCpPPBC1q/vvPBr5LxGvLC209knD67dk/img.png)NX , partial Relro 



NX가 있으니가,, RTL 을 하자 > 그냥 문제 이름도 RTL이다.

main :



![img](https://k.kakaocdn.net/dn/bQGDw4/btqCl897IGA/Tw3yQkwUhwEhQKKVc4ocnK/img.png)option 5



이 부분에서 bof가 발생하고 우린 여기서 rtl을 해주면 된다. 

exploit :



![img](https://k.kakaocdn.net/dn/CjmBo/btqCoRz3mFo/AgYuKcOi360xn4TCWIPQ4k/img.png)ex.py



바이너리를 확인해서 dummy(144) + sys_addr + dummy(4) + sh_addr로 페이로드를 구성했다.

p.s  이외에도 코스에서 돈을 벌어서 shell sword를 구입하면 주소를 던져주는데 이건 libc에 /bin/sh주소니까 딱히 신경 안써도 될 것 같다. 그리고 나는 문제를 풀 때 도커환경에서 gef를 사용하는데 원래는 페다에서 start > find "/bin/sh" 했던게 gef에서는 start > grep "/bin/sh"을 해서 주소를 찾아야한다. 그리고 sys_addr은 그냥 info func에서 system@plt주소로 찾았다.

 

### 4. g++ pwn

binary :



![img](https://k.kakaocdn.net/dn/b3vZYf/btqCz6b8mpY/aCZHyPrl5EQkc3VwvoTM50/img.png)Nx, Partial Relro



vuln.c :



![img](https://k.kakaocdn.net/dn/bfSscm/btqCDkmRRvA/hEAPZFS5lmICZucelbVW50/img.png)32개 입력받고 I를 you로 replace



get_flag.c : 



![img](https://k.kakaocdn.net/dn/tckjH/btqCy5xVsAF/0va1AN17FlAnv6krcHD4x0/img.png)이거 호출하자



exploit :



![img](https://k.kakaocdn.net/dn/o3Hc8/btqCB8NKfeE/PMh4UbfWOkK3MGTprFB2E1/img.png)ez



우리는 dummy(60)+sfp(4) 총 64개를 채우고 ret에 get_flag를 넣어야하는데 위에 vuln.c를 보면 32개 밖에 입력을 못받는다.

그래서 I가 You로 치환되는걸 이용하여 I를 21개 > You 63개  + A해서 64개를 맞춰주고 뒤에 flag_addr을 넣었다.