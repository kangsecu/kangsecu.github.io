---
layout: post
title: "2016 PlaidCTF unix_time_formatter Write up"
excerpt: "uaf를 공부하기 적합한 간단한 문제"
date: 2020-05-14
categories: [system, ctf]
comments: true
---

이번에는 Use After Free를 연습하기 좋은 문제인 2016 PlaidCTF에 unix_time_formatter를 가져왔다. codegate cat shop문제도 좋은 것 같은데 바이너리를 아직 못구했다...

exit함수에서 uaf취약점이 발생한다. N을 누르면 free chunk를 다시 사용할 수 있다. 

익스는 qword_602118에 값을 넣고 free를 한 후 set_timezone 변수를 덮어씌운다. 그리고 print_time을 콜하면 된다. 



exploit :

![utf.png](/img/utf.png)

지금은 로컬에서 돌린거라 flag.txt가 없지만 있었다면 출력이 되었을 것이다. 

uaf공부를 간단하게 했었는데 아직 부족한 느낌이다. 정리글도 한번 올려봐야겠다. 
