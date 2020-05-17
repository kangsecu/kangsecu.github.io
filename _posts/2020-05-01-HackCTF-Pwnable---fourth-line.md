---
layout: post
title:  "HackCTF Pwnable - fourth line"
excerpt: "for All Clear HackCTF"
date:   2020-05-01
categories: [wargame]
comments: true
---



<h3>1. Poet

binary :



![img](https://k.kakaocdn.net/dn/cjadyR/btqDNmYDU83/ikPmyIZcPjEcsrtLP4lmp1/img.png)



get_poem.c :



![img](https://k.kakaocdn.net/dn/tVgAw/btqDJLTiOY8/JDTLMpQBajktep9SjkRnk0/img.png)



rate_poem.c :



![img](https://k.kakaocdn.net/dn/dfoIh3/btqDNnXAhWh/9UCQNSNU7KyrFOpXbnWXU0/img.png)



reward.c : 



![img](https://k.kakaocdn.net/dn/cfr22T/btqDKqVTl8d/ktjguPC0C0r8OQNBkVRJo0/img.png)



대충 보면 그냥 poem을 입력받아서 1000000점을 넘기면 플래그를 준다. 위에 rate_poem.c 에 있는 문자들을 입력하면

100점을 주는데 저걸로 1000000점을 채울 수 없다. 근데 점수를 저장하는 변수인 dword_6024E0이 bss영역에 있다.

gdb로 rate_poem를 보면 100점을 늘려주는 부분이 strcmp를 하고 나서 rip + 0x201bae에 존재하는걸 알 수 있다. 즉

rip + 0x201bae == dword_6024E0이다. 그리고 get_author를 보면 unk_6024A0과 dword_6024E0의 거리를 구해서 만족할 점수를 넣어주면 된다는것을 알 수 있다. 그리고 두 변수 사이의 거리는 64bytes이다. 

exploit :



![img](https://k.kakaocdn.net/dn/kP48H/btqDL4LbBgf/bxnoUUKSatIVDSGu6i65a0/img.png)



간단하게 처음에 아무거나 입력하고 두번째에서 author을 물을때 값을 넘겼다. 

<h3> 2. 1996

binary :



![img](https://k.kakaocdn.net/dn/FsCh0/btqDOjHq9Le/x2KKK7KNXp8N8X6CmlKFB1/img.png)



main.c :



![img](https://k.kakaocdn.net/dn/lCogu/btqDL3S2lxG/IxwVpD30vJDf8BdAG09Yrk/img.png)



shell.c : 



![img](https://k.kakaocdn.net/dn/9RP7D/btqDMjg6D5X/QsP90SZkXPftKJCYNLbrQ0/img.png)



그냥 간단한 rtl문제이다. getenv에서 bof를 일으켜서 ret를 shell함수로 overwrite하면된다.

exploit :



![img](https://k.kakaocdn.net/dn/cX0dh4/btqDLD1ouzq/kwYlfvFVl15cKu7Rgwkxs0/img.png)



### 3. Random key

binary :



![img](https://k.kakaocdn.net/dn/vQU1b/btqDPYRQWb0/pRhGs6WqpWU0JU9fKUrExk/img.png)



main.c :



![img](https://k.kakaocdn.net/dn/b6COaE/btqDQUnDD5y/FWKgmjwm4JmfviB1GgkO4K/img.png)



그냥 rand값으로 생성하는걸 맞춰주면 된다. 우리도 파이썬 CDLL을 이용하여 난수를 생성하자.

exploit :



![img](https://k.kakaocdn.net/dn/blHMtE/btqDQTbboDY/QwkNSlOTAgKNQZcY7tpgcK/img.png)



### 4. RTL_core

binary :



![img](https://k.kakaocdn.net/dn/ebdet2/btqEcn4Ydqy/zmKAZ8ovMEMninwH6fg48K/img.png)



main.c :



![img](https://k.kakaocdn.net/dn/chq7iq/btqEcmygz4a/9VkKHiQOUwIBKyX3MwUcCK/img.png)



입력한 값을 hashcode랑 비교한 후 core실행

core.c :



![img](https://k.kakaocdn.net/dn/BjL1i/btqEeYbqQEE/n8tDAkshrAXWof0OQyKAA0/img.png)



후에 조건문을 맞추면 printf의 주소를 릭해준다.

check_passcode.c :



![img](https://k.kakaocdn.net/dn/Acw2f/btqEdkzIFef/7NlhxzEMoNVZOLSIjg6wJK/img.png)



이걸 구하는게 사실 문제푸는것보다 오래걸렸다. 5번을 돌리면서 0C0D9B0A7h을 5로 나누고 다시 5를 곱하면 값이 부족하니까 그냥 4번을 곱하고 부가적으로 부족한 값을 더해줬다.

exploit :



![img](https://k.kakaocdn.net/dn/bHbiug/btqEeXQ8i6k/YZ6cCQNvhKss8vsP2Ne3ik/img.png)



끝. 