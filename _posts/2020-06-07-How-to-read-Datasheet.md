---
layout: post
title: "How to read Datasheet"
excerpt: "Try to know datasheet & use it ~_~"
categories: [Embedded]
comments: true 
---

임베디드를 공부하기 위하여 이제 데이터시트를 읽는 법을 포스팅하려 한다.  정구홍 멘토님의 발표를 임베디드 보안을 공부하는 지표로 삼고 그 트랙을 따라서 공부를 하려고 한다. 

### 0x0 Datasheet?

데이터시트는 제조사에서 해당 부품(주로 칩)의 메뉴얼이다. 주로 전자공학도들이 많이 접하게 되며, 임베디드는 데이터시트로 시작해서 데이터시트로 끝난다고 봐도 무방할 정도이다.  보통 데이터시트에 들어가는 정보는 아래와 같다.

* 제조사
* 모델명
* 간단한 기능 설명
* 추천 동작 환경
* 검증 회로
* 제품의 특성
* 핀 접속 다이어그램

### 0x1 Example

데이터시트는 어떻게 생겨먹었나 보자. 우선 예시로 들 데이터시트는 Atmel 89C1051 이다. 보통 데이터시트를 구해서 열어보면 바로 우리가 원하는 모델명이 있을 수 있지만, 그 외에 다양한 모델명이 공존할 수 있다. 이를 family datasheet라고 하고, 동일한 계열의 데이터시트를 한 곳에 적어놓은 경우도 있으니 잘 보고 읽자.

<img src="/img/dt1.png" alt="dt1" style="zoom:80%;" />

우선 처음으로  Features는 해당 부품의 가장 중요한 특징들이 적혀있어서 시간이 없다면 이것만 확인하고 넘기기도 한다. 

<img src="/img/dt2.png" alt="dt2" style="zoom:80%;" />

다음으로 Description은 위에서 말한 중요한 특징들을 줄글로 자세하게 서술한 것이다.

<img src="/img/dt3.png" alt="dt3" style="zoom:80%;" />

다음으로 Absolute Maximum Ratings는 해당 부품에 가할 수 있는 최대전격을 나타낸다. 그 이상으로 전력을 가할 경우 제품이 손상을 입을 수 있다. 주의하자. 

reverse는 역방향 , voltage는 전압, rectified는 정류, forward는 순방향, surge는 급전 , current는 전류, junction은 접합을 말한다. 

그럼 위를 간단하게 읽어보면 작동가능한 온도는 -55에서 +125도 까지이다. 또 저장 가능한 온도는 -65도에서 +150도이다.

<img src="/img/dt4.png" alt="dt4" style="zoom:80%;" />

이번에는 전기적 특성을 나타낸 정보다. 보통은 Electrical Characteristics라고 적어주는데 여기선 DC 라고 적었다.  

저 심볼들에 대한 내용에 더 자세한 내용들은 추가적으로 글을 작성할 예정이다 . 

<img src="/img/dt5.png" alt="dt5" style="zoom:80%;" />

다음으로는 Pin Configuration인데 말 그대로 해당 부품의 핀 구성을 보는것이다. 핀 내용들에 관한 내용은 밑에 자세하게 다룬다. 이번엔 그냥 생김세만 보고 넘어가도록 하자. 

<img src="/img/dt6.png" alt="dt6" style="zoom:80%;" />

이렇게 바로 다음에 Pin Description에서 각각 핀들의 역할과 정보를 다뤄준다. 아마 가장 많이 볼 내용일 것이다.

<img src="/img/dt7.png" alt="dt7" style="zoom:80%;" />

이번에는 Block Diagram이다. Pin의 번호는 아니고 Pin의 이름만 적혀있고, 내부 구조를 보여주고 있다. 

이외에도 다양하게 Special Function Registers 처럼 본 부품에만 존재하는 특별 함수의 기능들을 정리해놓은 글이나,  Flash Programming Modes라고 플래시 프로그래밍 모드에 관한 내용을 적어준 내용도 있다. 그리고 Test Circuit라고 시험회로 조건도 있고, Package information이라고 PCB Library를 만들 때 중요한 자료이다.
