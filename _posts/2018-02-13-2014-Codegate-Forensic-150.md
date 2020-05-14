---
layout: post
title:  "2014 Codegate Forensic 150"
excerpt: "Try to know Packet & use it~_~"
date:   2018-02-13
categories: [Forensic,ctf]
comments: true
---

문제에 들어가면 pcap파일을 준다. 처음에 와이어샤크로 열었는데 EPB의 전체 블럭 길이 96이 4270407998byte의 패킷 데이터 길이에 비해 너무 작다는 에러가 났다.

헥스에디터로 열었는데 포맷 형식이 pcap헤더와 다름 > pcap은 헤더 맨처음 매직넘버가 0xa1b2c3d4이거나 0xd4c3b2a1여야하는데 다르다. 



pcap-ng(pcap next generation)라는 파일 포맷이고 EPB는 블럭의 한 종류로 Enhanced Packet Block라는 걸 알게됨 구글링엄청 했다. 

![img](https://t1.daumcdn.net/cfile/tistory/992EC13D5B5D837406)



그리고 헥스에디터로 보니까 토탈 길이가 캡쳐 길이보다 작음;; 토탈길이가 0x00000060 = 96이고 캡쳐길이가0xFE89413E = 4270407998임 이게 말이된다고 생각함? 그래서 캡쳐길이를 패킷길이랑 같게 3E00 0000으로 바끄니 pcap가 열림 

![img](https://t1.daumcdn.net/cfile/tistory/99BBCF335B5D837436)

이제 와이어샤크에서 pcap를 열어보니까 http패킷들이 있다. 좀 보다가 Export Object를 이용해서 몇몇 파일들을 축출했다.

![img](https://t1.daumcdn.net/cfile/tistory/9910D63E5B5D837517)

multiple.pdf를 다운받고 열어보니 flag가 있다.

![img](https://t1.daumcdn.net/cfile/tistory/998D46465B5D837421)

이상
