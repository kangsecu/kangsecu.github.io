<h1>메모리 보호기법(Memory Mitigation) for Pwn</h1>

메모리 보호기법들을 공부중이다.. 문제풀이 하면서는 아직 NX bit , ASLR, stack canary 이 정도밖에 겪어보지 못했다. 그래서 그때마다 보호기법들 설명이랑 바이패스 등을 공부해본 내용을 여기에 정리하려한다. 그때 그때 공부하면서 정리할거라 처음엔 내용이 하찮을 수 있다.

근데 보통 pwntool이나  peda같은거 쓰면 보호기법 일일이 확인안해도 편하게 보여줘서 좋다...

<hr>

### 1. ASLR

ASLR(Address Space Layout Randomization)이다. 아마 가장 많이 듣는 보호기법중 하나가 아닐까 생각한다. 대충 이름에서 알 수 있듯이 익스를 하기 어렵게 스택이나 힙 등의 주소를 랜더마이징해서 실행시 마다 주소가 바뀌게 하는 기법이다. 

아직 LOB까지밖에 안해봐서 보통은 randomize_va_space 파일을 통하여 ASLR을 제거하고 문제를 해결했다. 

뭐 공부하면서 여러 글 보다보니 실제로 heap영역이랑 뭐 메모리 주소 출력해주는 프로그램 만들어서 주소값 변화하는거 보여주는데, 이건 지극히 나의 문제풀이를 위한 글이니 그런건 생략- 

무식하게 브루트포싱을 통해서 주소가 맞을 때 까지 돌려주면 성공할수도 있다. - 확률은 매우 낮다.

아니면 Nop sled기법(0x90)으로 주소가 맞을 때 까지 굴려도 되는데 이건 요세 잘 안먹힌다고 한다. (왤까?)

심볼릭링크로 고정된 주소에서 함수가 실행되게 하면 된다. > 이건 나중에 글을 따로 작성해봐야겠다. 

그 외에 imagebase나 setarch 등의 요소가 있다고 하는데 알아봐야겠다. 



### 2. NX bit / DEP

처음 RTL을 공부하면서 본 것 같다. NX는 Non-Excutable의 약자로 코드가 저장되는 영역을 제외한 모든 영역에서의 실행권한을 제한하는 기법이다. DEP는 Data Excution Prevention으로 결국 둘이 같은 의미이다. 아마 대부분 lob문제를 해결하면서 RTL을 처음 접할 때 볼 것 같다. 

bof로 익스를 할 때 ret를 쉘코드 주소로 덮었을 때 NX가 없으면 바로 실행되지만 NX가 있으면 쉘을 딸 수 없다.  그래서 NX와  DEP를 우회하기 위해서 RTL을 하는 것이다. 

그냥 RTL하자 , ROP 등등 

<새로 알아낸거>

아니면 그냥 system()이 없을때를 대비하여 mprotect()를 이용하여 실행권한을 부여하자



### 3. Stack Canary

*** stack smashing detected *** 우엑

canary는 SFP나 RET에 공격자가 원하는 주소를 덮어씌우는 것을 방지하기 위하여 버퍼와 SFP사이에 추가되는 메모리 영역이다. 이 canary가 변조되는 값을 감지해서 프로그래밍 자체적으로 종료시킨다.  공격자는 RET를 수정해야 하는데 이 때 Canary가 먼저 채워지면서 보호를 하는 것 이다.

Canary는 프로그램이 종료될 때 코드 실행 전 스택에 저장된 Canary값과 종료될 때의 값을 비교하여 다를 경우 공격으로 판단한다.

아래 코드를 간단하게 보자



![img](https://k.kakaocdn.net/dn/TUcri/btqCQnMAAf8/d6j7hMPPP2DpS5uIbwLvOK/img.png)



보면 v4가 canary라는걸 알 수 있다,

fsb가 발생하는 printf(format)에 브포를 걸고 값을 넘겨주고 봤다.



![img](https://k.kakaocdn.net/dn/ervFv8/btqCSYkD5Zm/SIVLUMxUuSqd4IRhNFqec1/img.png)



그럼 rbp가 가르키는게 sfp가 되고 그 뒤인 $rbp-8인 0x7fffffffdfb8이 카나리가 된다.

아니면

64비트에서는 rdi rsi rdx rcx r8 r9 그 다음 스택이 릭이 되기 때문에 %p를 6개를 넣어서 총 48bytes를 우선 릭하면 그 다음에 format이 릭된다 . 그 후  v4 = rbp -8이고 format = rbp -60이니까 오프셋 88을 구해서 format이 릭되기 시작할때를 기준으로 %p를 11개를 추가해주면 카나리까지 릭이 된다. 그럼 총 %p * 17개가 된다.

우회하는 방법은 대충 브루트포싱을 통하여 카나리값을 알아내는 방법이 있다. 카나리 값은 4바이트라 브포 가능이다. 범위는 256가지로 4번만 브포를 돌리면 된다 > 대충 자동화툴 짜서 돌리면 그렇게 오래걸리진 않는 것 같다.(?)

카나리 루틴이 노출된 경우에는 역연산을 통하여 우회도 가능하다.

fsb가 발생하는 곳에 브포를 걸고 실행 후 i r $rbp 하면 거기가 가리키고잇는게 sfp인데  sfp 뒤에잇는값이 왠만해선 카나리이고 아닐땐, ret넘어가지 않는 범위 내에서 첫바이트가 \x00으로 시작되는 값 찾으면 거의 카나리

pthread를 이용하여 Canary Leak이 가능하다. > 이것도 카나리릭 자세하게 글 한번 쓸 예정



### 4. PIE

PIE는 Position Independent Executable의 약자로 바이너리 주소를 상대적인 주소로 랜덤하게 매핑시키는 기법이다. 사실 문제를 풀면서 그럼 ASLR이랑 다를게 뭔가 싶었는데 ,PIE는 모든영역을 보호하는게 다르다. 

ASLR은 데이터영역의 주소는 고정되지만 PIE는 모든영역을 랜더마이징하기 때문에 데이터영역의 주소도 바뀐다.

하.지.만 오프셋은 바뀌지 않는다. 그러므로 base주소를 대상으로 오프셋을 이용하여 상대적인 주소를 잡아줘야한다.

memory leak을 하거나 ,,, ROP기법을 이용하여 우회가 가능하다.

 

### 5.Relro

Relocation Read-Only의 약자로 메모리가 변경되는걸 방지하는 기법이다. partial과 Full로 나뉘는데 ,, 

Partial의 경우  got가 wirtable이고, 함수를 호출하면 해당 함수의 주소를 받아온다.

Full은 got가 read-only상태로 ELF를 실행하면 got에 모든 lib주소가 바인딩된다. 

Relro가 적용되어 있으면 ctors, .dtors, .jcr, .dynamic, .got 섹션에 데이터를 쓸 수 없어진다..  > GOT Overwrite가 안됨.. 

근데 이것도 Partial Relro 와 Full Relro가 다르다. 

------

공부한 것들 까지는 적어봤는데 뭐 적을 내용이 없다. 