---
layout: post
title: "libc-database"
excerpt: "Try to know libc-database & use it ~_~"
categories: [system]
comments: true 
---



이번에는 libc가 같이 제공이 안될경우 libc를 찾아서 문제를 해결하는 방법에 대하여 알아보자.

### libc-database 다운 : 

$git clone https://github.com/niklasb/libc-database.git

### libc data 다운 :

library download / pwd : libc-database > $./get

### 사용법 :

 1. 함수로 libc 파일 찾기 : ./libc-database/find/ [함수이름] [함수주소]

 2. 함수 offset 찾기 : ./libc-databse/dump [id] [함수 이름]

 3. ./libc-database/find/ [함수이름] [offset 3 bytes]

------

function_addr = libc-base_addr + offset인데 ASLR이 걸려있으면 이 libc-base_addr이 랜덤으로 변한다.

하지만 offset은 변하지 않기 때문에 우리는 이 offset을 이용하여 실제 함수의 주소를 구한다. 
