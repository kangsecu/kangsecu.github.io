---
layout: post
title: "32bit calling convection"
excerpt: "Try to know calling convention & use it ~_~"
categories: [system]
comments: true 
---

공부를 하다가 왜 64bit rop는 가젯을 먼저 넣는지 궁금해서 친구에게 물어봤더니 호출 규약을 공부해보라고 해서 이렇게 정리글을 적기로 하였다. Thankgs to Shot_gh(http://ipwn.kr/)

### 0x0 함수 호출 규약?

함수 호출 규약이란 함수를 호출할 때 어떤 방식으로 함수에 파라미터를 전송하는지를 다루는 규약이다. 이뿐만 아니라 함수를 호출한 이후에 스택 포인터를 어떻게 처리하는지에 대해서 다루는 규약이기도 하다.

이 호출규약은 32bit와 64bit가 다른데, 그래서 내가 64bit rop를 할 때랑 32bit rop를 할 때, 가젯을 넘겨주는 방법이 다른 것이다.  이번글에선 32bit를 다루고 다음글에서 64bit를 다루자. 



### 0x1  Intel Architecture 32 bit / x86 -32 Architecture

32bit의 호출규약중 cdecl , stdcall , fastcall 세가지를 알아보자.

#### 0x0 cdecl

C언어에서 사용되는 방식으로, caller에서 스택을 정리하는 특징이 있다.

| 파라미터를 스택에 넣는 순서 | 스택정리 | 표기     | 장점               |
| --------------------------- | -------- | -------- | ------------------ |
| righit > left               | caller   | _(fname) | 가변인자 전달 가능 |

```c
#include <stdio.h>
int sub(int a, int b){
return (a- b);
}
int main(int argc, char *argv[]){
 return sub(2,1);
}
```

위의 코드를 보면 main이 caller가 되고 sub는 callee가 된다.  

![image-20200604142801806](C:\Users\kangs\AppData\Roaming\Typora\typora-user-images\image-20200604142801806.png)

위의 코드의 main을 아이다로 확인해보면 파라미터는 스택에 push하여 호출시 전달되고, main이 함수에서 add esp,8으로 스택을 처리한다.  더 자세히 보자. 

push ebp로 ebp를 스택값에 넣고, mov ebp,esp로 esp값을 ebp로 이동시킨다.  그 후 push 1,2를 통해서 두개의 파라미터를 역순으로 넣는다. 다음으로 call sub로 sub함수를 호출한다. 

![image-20200604143027405](C:\Users\kangs\AppData\Roaming\Typora\typora-user-images\image-20200604143027405.png)

이제 sub함수를 보자. push ebp로 함수가 변경되어서 새로운 스택 프레임을 생성하고, mov ebp,esp로 main과 동일하다. 다음은 mov eax, [ebp+arg_0]로 ebp+arg_0의 값을 eax로 보낸다.  그 후, sub eax, [ebp+arg_4]로 ebp+arg_4의 값을 eax와 마이너스연산을 한다. 그 후 pop ebp로 ebp를 스택에서 꺼낸다.  이제 다시 main을 확인해보자.

![image-20200604143456185](C:\Users\kangs\AppData\Roaming\Typora\typora-user-images\image-20200604143456185.png)

add esp,8로 스택에 8의 공간을 정리하고 pop ebp로 ebp를 스택에서 꺼낸다. 그 후 함수가 종료된다. 



#### 0x1 stdcall 

주로 win32 API에서 사용되며, cdecl방식과는 반대로 callee에서 스택을 처리한다. cdecl방식이 아닌 stdcall을 하고싶을 때는 _stdcall(fname)을 적어주면 된다.

| 파라미터를 스택에 넣는 순서 | 스택정리 | 표기                | 장점          |
| --------------------------- | -------- | ------------------- | ------------- |
| righit > left               | callee   | _(fname) , (fname)@ | 코드가 짧아짐 |

이것도 코딩을 해서 보려했는데 왜 vim에서 int _stdcall sub()를 선언하면 에러가 나는지 모르겠다... 

뭐 아무튼 이 방식도 스택에 파라미터를 push하고 함수 호출 시 전달하는건 동일하고 callee에서 스택을 처리하는 방식이 다르다. cdecl에서는 main함수에서 호출 한 후 add esp,8을 했는데 stdcall에서는 sub()함수의 retn명령에 처리할 스택의 사이즈를 포함해서  retn 8(retn+ pop8)로 스택을 처리한다. > 스택을 처리하는 코드가 없어서 코드가 짧아짐

#### 0x2 fastcall

함수에 전달하는 파라미터를 스택이 아니고 레지스터를 이용하여 전달한다는 것만 빼면 stdcall과 모두 동일하다.

| 파라미터를 레지스터에 넣는 순서             | 스택정리 | 표기                            | 장점          |
| ------------------------------------------- | -------- | ------------------------------- | ------------- |
| 두개는 ECX,EDX에 전달 나머지는 right > left | callee   | @(fname) , (fname)@,바이트 표기 | 코드가 짧아짐 |

레지스터를 이용해서 함수를 더 빠르게 호출이 가능하지만, ECX, EDX에 다른 중요한 값이 저장되어 있을 경우 이를 백업해놔야한다. 