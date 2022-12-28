---

layout: post
title:  "HackCTF Pwnable - second line"
excerpt: "for All Clear HackCTF"
date:   2020-02-25
categories: [wargame]
comments: true

---

### 1. x64 Buffer Overflow

binary :



![img](https://k.kakaocdn.net/dn/oXm1W/btqCDlMOSw4/c1kRzojKAmp5ik7TtPv6H0/img.png)



main.c : 



![img](https://k.kakaocdn.net/dn/KHZ4H/btqCDk1qOon/AtKqNRDZICk6WNNbWrJcFK/img.png)



callmemaybe.c :



![img](https://k.kakaocdn.net/dn/bRxCZM/btqCAOIXoe4/pW7k3nVK6MdZJ3YQIwMh31/img.png)



exploit :



![img](https://k.kakaocdn.net/dn/bS8qKa/btqCB8714Wo/2gv0CfWSjt3x0MlN0IDki1/img.png)



 

### 2. x64 Simple_size_BOF

binary :



![img](https://k.kakaocdn.net/dn/c3ILRX/btqCBw89ed1/vkHn2agqtxmYG0aIt3KcL1/img.png)



main.c :



![img](https://k.kakaocdn.net/dn/tTPQk/btqCynlgyRK/OkZTUKyVjeHAdwAIEXNlkk/img.png)



exploit :



![img](https://k.kakaocdn.net/dn/KQ0Pc/btqCB8NIHai/os8zobshVkQKiDkr3SqiAK/img.png)



총 shell_code(31) + dummy(27929) + ret(buf_addr)

### 3. Simple_Overflow_ver_2

binary :



![img](https://k.kakaocdn.net/dn/sGDiX/btqCclneS2f/lARKy0VCztsaXoityNWjK1/img.png)



main :



![img](https://k.kakaocdn.net/dn/b1rexn/btqCafVTALE/jSdXHmtHQ8nxZwvdKKXr41/img.png)



이번 문제는 매우 간단하다.(사실 지금까진 다 간단하다.) 그냥 scanf에서 취약점이 발생한다. 0x88 = 136이고, sfp  4를 합치면 140이다.

payload :

shellcode(25) + dummy(115) + ret_addr 



![img](https://k.kakaocdn.net/dn/d2xqrq/btqCbTR7ZzO/r1LQFrTrqXvOu1VNsRqAiK/img.png)



### 4. Offset

binary  : 



![img](https://k.kakaocdn.net/dn/kIu1k/btqCagtCka7/WzuXMt8TpmWtljErLpAPik/img.png)



main :



![img](https://k.kakaocdn.net/dn/B1Y6g/btqCafO5MXw/kcTeSYr0zEdBChkbe9iGQK/img.png)



select_func :



![img](https://k.kakaocdn.net/dn/Yh5pf/btqCaeQbZsR/4yHcOLxgPKyTDkeISFqKxK/img.png)



print_flag :



![img](https://k.kakaocdn.net/dn/52kCT/btqCcku8r9B/ZzltVv3UKJ5Lo5psLDDgX0/img.png)



main에서 gets로 &s를 입력받아서 select_func함수의 인자로 전달한다. v3변수는 처음엔 two의 주소값을 갖지만, 인자로 전달받은 src의 값이 one이면 one의 주소값을 갖게된다. > 바로 이 점이 우리가 공략할 것 이다.

보호기법들 때문에 뭐 할 수 있는게 없다. 하지만 PIE가 있어도 오프셋값만 맞춰주면 되기 때문에 문제 이름이 Offset인 것 같다.

함수들을 뒤져보니 print_flag라는 함수가 있었고, 누가봐도 select_func에서 리턴될 때 마지막 값을 print_flag함수를 가르키게 하면 해결 되는 것 같았다.  그래서 gdb를 이용하여 dummy가 30인걸 구했다.  

payload :

dummy(30) + print_falg_addr 



![img](https://k.kakaocdn.net/dn/ecKPOn/btqCafn0GF5/aYkRxvpWzylOEFnkM1nZxK/img.png)



해결 한 후, 확인하기 위하여 이것저것 봤는데 보통은 strncpy함수에서 src의 1byte만 덮을 수 있어서 31바이트중에 dummy(30) + "\xd8"로 하는 풀이들도 봤는데 그게 더 현명한 것 같다,,,
