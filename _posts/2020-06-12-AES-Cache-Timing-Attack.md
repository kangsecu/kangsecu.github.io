---
layout: post
title: "AES Cache Timing Attack(CVE-2016-7440)"
excerpt: "Try to know AES Timing Attack & use it ~_~"
categories: [system,crypto,1-day]
comments: true 
---

이번에는 부채널분석 중 하나인 timing attack을 통해서 AES 암호화를 분석해보자. 이번에 다루는 내용은 CVE-2016-7440에 속해있다.

### 0x0 AES?

우선 AES에 대해서 간단하게 설명을 하면 128bit 암호화 블록에 128bit , 192bit, 256bit의 다양한 키 길이를 가진 대칭 암호 알고리즘이다.  AES는 구조상 캐시를 이용한 timing attack에 취약하다. 

### 0x1 AES Analysis & Theory

AES는 원래 4단계의 연산을 한 라운드로 10라운드를 반복 연산하는데 이러한 과정에서 리소스가 과다하게 소요되어 실제 기기에 적용되는 AES 모듈은 경량화를 거친다. 그 중 하나를 보면 SubBytes, ShiftRows, MixColumns를 계산해두고 후에  이용하는 것이다. 

4×4 행렬 A를 A= (a_i)_{i=0,1,⋯,15}로 표현하자. 그렇다면 A를 입력하고 한 라운드를 거쳤을 때의 출력값 A′는 다음과 같이 계산된다.
$$
A′[0]:=M[0]⋅X[a0]⊕M[1]⋅X[a5]⊕M[2]⋅X[a10]⊕M[3]⋅X[a15]⊕k[0]\\
A′[1]:=M[0]⋅X[a1]⊕M[1]⋅X[a6]⊕M[2]⋅X[a11]⊕M[3]⋅X[a12]⊕k[1]\\
A′[2]:=M[0]⋅X[a2]⊕M[1]⋅X[a7]⊕M[2]⋅X[a8]⊕M[3]⋅X[a13]⊕k[2]\\
A′[3]:=M[0]⋅X[a3]⊕M[1]⋅X[a4]⊕M[2]⋅X[a9]⊕M[3]⋅X[a14]⊕k[3]\\
A'[4]:=M[0]⋅X[a4]⊕M[1]⋅X[a3]⊕M[2]⋅X[a7]⊕M[3]⋅X[a13]⊕k[4]\\
$$
이 과정에서 M[t]는 MixColumns 과정에서 사용되는 행렬의 t번째 열이고,  X[t]는 SubBytes 에서 사용되는 S-Box로 t를 치환한 값. 이제  Bi:=M[i]⋅X[a]를 미리 계산해놓으면 아래와 같다.
$$
A'[0]:= B_0[a_0]⊕B_1[a_5]⊕B_2[a_{10}]⊕B_3[a_{15}]⊕k[0]\\
A'[1]:= B_0[a_1]⊕B_1[a_6]⊕B_2[a_{11}]⊕B_3[a_{12}]⊕k[1] \\
A'[2]:= B_0[a_2]⊕B_1[a_7]⊕B_2[a_{8}]⊕B_3[a_{13}]⊕k[2]\\
A'[3]:= B_0[a_3]⊕B_1[a_4]⊕B_2[a_{9}]⊕B_3[a_{14}]⊕k[3]\\
A'[4]:= B_0[a_4]⊕B_1[a_3]⊕B_2[a_{7}]⊕B_3[a_{13}]⊕k[4]\\
$$
이러면 많이 경량화가 되었으므로 모든 과정을 거치지 않고 미리 계산되어 메모이제이션 되어있는 결과값만 찾으면 된다.

하지만 S-Box 자체는 배열이라 결과 값을 찾을 때 배열 탐색을 해야하고, 이로 인해서 소요되는 시간이 발생하기 마련이다. 바로 이러한 점에서 Cache Timing Attack이 발생한다. 위의 모든 과정을 거친 최종 출력물 암호화된 C는 10번째 라운드의 키 k에 관하여 아래와 같다.
$$
C[0]:=X[a0]⊕X[a5]⊕X[a10]⊕X[a15]⊕k[0]\\
C[1]:=X[a1]⊕X[a6]⊕X[a11]⊕X[a12]⊕k[1]\\
C[2]:=X[a2]⊕X[a7]⊕X[a8]⊕X[a13]⊕k[2]\\
C[3]:=X[a3]⊕X[a4]⊕X[a9]⊕X[a14]⊕k[3]\\
C[4]:=X[a4]⊕X[a3]⊕X[a7]⊕X[a13]⊕k[4]\\
$$
이제 AES알고리즘을 실행할 때 X를 캐시에 로드 할것이다. 
$$
C_i=X[a_p]⊕K_iC_i=X[a_p]⊕K_i, C_j=X[a_q]⊕K_j
$$
이러한 환경에서  
$$
a_p = a_q
$$
이렇다면  이미 위에서 결과값이 캐시에 로드된 상태이므로 둘이 다른 경우보다 AES의 연산속도가 더 빠를 것이다. 이제 두가지의 속도차이 Δ는 아래와 같다.
$$
Δ:=c_i⊕c_j=k_i⊕k_j
$$
이제 공격자는 평균 암호화 시간보다 더 빠른 연산을 하는 (i,j)만 최대한 많이 찾으면 된다. 이를 계속해서 반복해주면 실제 Δ 값에 가까워지게 되고 10번째 라운드 키인 k를 유추할 수 있어진다. AES는 구조상 라운드 키를 알아내면 역연산을 통해 모든 키를 알아낼 수 있다.

### 0x2 S-Box

이번 공격의 포인트는 바로 S-Box이다.  S-Box는 Byte 값의 치환을 하기 위하여 key 확장 루틴과 여러 Subbytes변환에서 사용되는 비선형 대칭표다.

![Mint & Latte_. :: Mint & Latte_. (410 Page)](https://t1.daumcdn.net/cfile/tistory/1559D6484E76DE9538)

이 이미지가 바로 AES 암호화에서 사용하는 S-Box인데, 간단하게 예를 들자면 가로와 세로의 조합에 의해서 다른 문자로 치환하는 표이다. 3C라는 값을 S-Box로 변환한다고 가정하면 행이 3과 열의 C의 행렬값으로 이를 치환해서 2E가 된다.

추가적으로 위의 S-box는 비선형적인 값들을 나타내는데, EEA를 공부하면 이 곱셈에 대한 역원을 찾는 방법을 알 수 있다. 

### 0x3 Main Code

```c
 for (round = 1; round<Nr; round++)
    {
        SubBytes();
        ShiftRows();
        MixColumns();
        AddRoundKey(round);
    }
 
    SubBytes();
    ShiftRows();
    AddRoundKey(Nr);
```

위의 코드가 AES의 중요 루틴이다. 위에서 말한 그대로 돌아가는데, 각 함수를 간단하게 보자. 처음으로 SubBytes()함수는 그냥 128bit AES라고 가정했을 때, 16바이트로 변환 후 배열 상태로 S-Box로 치환하는 함수고, ShiftRows() 함수는 

```c
void ShiftRows()
{
    unsigned char temp;
    // Rotate first row 1 columns to left
    temp = state[1][0];
    state[1][0] = state[1][1];
    state[1][1] = state[1][2];
    state[1][2] = state[1][3];
    state[1][3] = temp;
    // Rotate second row 2 columns to left
    temp = state[2][0];
    state[2][0] = state[2][2];
    state[2][2] = temp;
    temp = state[2][1];
    state[2][1] = state[2][3];
    state[2][3] = temp;
    // Rotate third row 3 columns to left
    temp = state[3][0];
    state[3][0] = state[3][3];
    state[3][3] = state[3][2];
    state[3][2] = state[3][1];
    state[3][1] = temp;
}
```

이 함수는 그냥 행을 계속 변환 해주는거다. 첫번째 행은 회전되지 않고 두번째 행은 1byte,  세번째는 2bytes , 네번째는 3bytes 만큼 왼쪽으로 로테이션한다. 다음으로 MixColumns() 함수는  아래와 같다.

```c
#define xtime(x)   ((x<<1) ^ (((x>>7) & 1) * 0x1b))
void MixColumns()
{
    int i;
    unsigned char Tmp, Tm, t;
    for (i = 0; i<4; i++)
    {
        t = state[0][i];
        Tmp = state[0][i] ^ state[1][i] ^ state[2][i] ^ state[3][i];
        Tm = state[0][i] ^ state[1][i]; Tm = xtime(Tm); state[0][i] ^= Tm ^ Tmp;
        Tm = state[1][i] ^ state[2][i]; Tm = xtime(Tm); state[1][i] ^= Tm ^ Tmp;
        Tm = state[2][i] ^ state[3][i]; Tm = xtime(Tm); state[2][i] ^= Tm ^ Tmp;
        Tm = state[3][i] ^ t; Tm = xtime(Tm); state[3][i] ^= Tm ^ Tmp;
    }
}
```

이 코드는 행렬 곱셈을 수행하는 함수다. 이를 이해하려면 대수학의 유한체에 대한 이해가 있어야 한다.  따로 다루지는 않겠다. +마지막 라운드에서는 MixColumns를 하지 않는다.  마지막으로 AroundKey()함수다.

```c
void AddRoundKey(int round)
{
    int i, j;
    for (i = 0; i<4; i++)
        for (j = 0; j<4; j++)
            state[j][i] ^= RoundKey[round * Nb * 4 + i * Nb + j];
}
```

이 함수는 암호화 과정에서 수행되는 함수인데, 맨 처음에 Subbytes들의 각각의 byte들이 각 라운드키들과 XOR연산을 수행한다. 

### 0x4  POC

이제 간단히 함수는 설명이 끝났으니 위에서 말한 가설대로 코드를 작성해보자. 우선 타이밍어택에서 가장 중요한 요소중 하나인 연산 속도를 측정하기 위한 시간비교 코드를 만들어야한다.  대충 코드는 AES알고리즘을 가상환경에 구현해두고, 한글자씩 값을 넘겨준 후에 모든 연산 시간을 기록하고 평균 시간을 측정한다. 그 후 평균 시간보다 길고 가장 연산 시간이 오래 걸리는 글자들을 기록해서 키값을 찾으면 된다. 

```python
def recv_result(p, string):
    result = ''
    while string not in result:
        result += p.recv(1)
    return result

```

이 코드로 우선 결과값을 받을 변수를 만들고 거기에 결과값을 하나씩 저장한다. 

```python
for y in range(128):
    for x in range(0x20, 0x80):
        for z in range(0,128):
            p = socket()
            test = resultkey + chr(x)
            stime = time.time()
            p.send(test+"\n")          
            data = p.recv_result(p,"key ")
            take = time.time() - stime

if data.find("key") >= 0:
	resulteky += chr(x)
	print resultkey
```

이번에는 위에서 말했듯이 값을 부르트포싱을 하며 넘겨주고 연산하는데 걸린 시간을 연산하는 함수다.

```python
if avg >= mytm:
	mytm = avg
	realkey = x

if avg >= (y+2)*5.04:     
	break
print resultkey
```

이제는 위의 시간보다 오래 걸리는 것들은 확실한 키값으로 인지하고 저장 후 출력을 한다.

코드를 작성하는데 bpsec 블로그의 글을 참고했다. 다음에는 직접 더 효율적인 코드를 작성해보고 싶다.

### 0x5 Reference

너무 어렵다.. 더 깊게 다뤄보고 싶지만 아직 많이 미숙해서 힘들다. 

+ . Bonneau and I. Mironov. Cache-collision timing attacks against AES. *In in Proc. Crypto-graphic Hardware and Embedded Systems (CHES) 2006. Lecture Notes in Computer Science,pages 201–215. Springer, 2006.*
+ Daniel J. Bernstein. Cache-timing attacks on AES. *April 2005.* *http://cr.yp.to/antiforgery/cachetiming-20050414.pdf.*
+ https://crypto.stackexchange.com/questions/26732/calculating-multiplicative-inverse-for-rijndael-s-box-using-eea
+ https://cr.yp.to/antiforgery/cachetiming-20050414.pdf

