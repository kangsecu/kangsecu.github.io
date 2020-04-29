---
layout: post
title:  "One_gadget"
excerpt: "Try to know One_gadget & use it~_~"
date:   2020-03-21
categories: [system]
comments: true
---



One_gadget이란 하나의 가젯만을 이용해서 쉘을 딸 수 있는 가젯이다.got overwrite를 할 경우 많이 사용되며 /bin/sh을 립시 파일 내에서 실행하는 가젯이다.

one_gadget install : 

```
> apt install ruby
> gem install one_gadget
```

사용법 : 

```
one_gadget "libc file"
ex) one_gadget /lib/x86_64-linux-gnu/libc.so.6
```