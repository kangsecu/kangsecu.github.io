---
layout: post
title: "2018 Sunshine CTF Write up"
excerpt: "웹,,, 뭘까,,,"
categories: [Web,ctf]
comments: true
---

SunshineCTF write up입니다.

### 1.Evaluation

![img](https://t1.daumcdn.net/cfile/tistory/993AE74F5ACB7F010B)

이 문제는 50점으로, 매우 간단한 문제였습니다. 문제에 들어가면 아래와 같은 코드가 있습니다.

```php
<?php 
 
include "flag.php";
error_reporting(0);
show_source(__FILE__);
$a = @$_REQUEST['hello'];
eval("var_dump($a);");
 
?>
```


처음에는 hello파라미터에 ?hello=system("cat /flag.php");를 전송했는데, string(2) "?>" 라고 출력되고 flag가 나오지 않았습니다.
그래서 고민을 하다가 두번째 시도에서 ?hello=system(%22cat%20flag.php|base64%22)라고 전송을 하였더니 base64로 암호화된 PD9waHAgCiRmbGFnID0iTm9wZSI7CgovLyBzdW57YzBtbTRuRF8xTmozY3RpMG5faTVfRTRzWX07가 출력되어서 복호화를 하니 문제가 해결되었습니다.

```php
<?php 
$flag ="Nope";
 
// sun{c0mm4nD_1Nj3cti0n_i5_E4sY};
```



Solve!



### 2.Marceau

![img](https://t1.daumcdn.net/cfile/tistory/997BAE405ACB7F0101)

이 문제는 힌트가 나오기 전까진 고민을 많이했습니다. 힌트에서 mime이라는 단어를 보고 해결하였습니다.그저 프록시나 Burp같은 프로그램을 이용하여 HTTPheader를 변경해주면 되는 문제였습니다.

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8 라는 부분을 

Accept: text/php,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8 라고 수정해주면 문제가 해결됩니다.

```php
<?php
// sun{45k_4nd_y3_5h411_r3c31v3} (nice work!)
 
// */* won't work here- you'll have to be more assertive.
if(strpos($_SERVER['HTTP_ACCEPT'], "text/php") === false)
  echo "<marquee><h3>You specifically want my PHP source. Why did you accept anything else?</h3></marquee>";
else
  show_source(__FILE__);
?>
```



sun{45k_4nd_y3_5h411_r3c31v3} 

Solve!



### 3.Home sweet home

![img](https://t1.daumcdn.net/cfile/tistory/99CFBD4B5ACB7F0113)

이 문제는 상당히 쉬웠습니다. 처음에는 어렵게 생각하여서 삽질을 오래하였는데, 실제로 해결하고 나니 그렇게 쉬운 문제 인것같습니다.이 문제는 "과연 실제로 웹사이트에서 개인클라이언트의 IP에 제한을 둔거겠어?"하는 생각으로 삽질을 하다가 해결하지 못하고있었습니다. 그래서 실제로 제한을 두었다고 생각하고 시도하니 해결되었습니다. 그저 헤더에 X-Forwarded-For: 127.0.0.1를 수정하니 문제가 해결되었습니다.



**Host**: web1.sunshinectf.org:50005



**X-Forwarded-For**: 127.0.0.1



sun{Th3rEs_n0_pl4cE_l1kE_127.0.0.1}



Solve!





### 4.Search Box

![img](https://t1.daumcdn.net/cfile/tistory/99B51E4E5ACB7F0111)

이 문제는 상당히 어려웠던 문제였습니다. 이 문제에 관한 내용을 매우 많이 구글링과 삽질을 해봤습니다. 그 결과 본 문제가 curl를 이용한다는것을 알게되었습니다. 그래서 구글링을 하다가 php버그에서 본 문제와 아주 관련이 깊은 문서를 발견하였습니다. https://bugs.php.net/bug.php?id=68089 바로 이 자료인데, 이 자료를 확인하시면 "코드 내에서 사용자 입력이 Strpos를 사용하여 스키마에 대해 검사되는 경우, NULL바이트를 사용하여 이를 전복시킬 수 있고, 그런 경우에 로컬파일이 노출이 가능합니다." 라고 적혀있습니다. 그래서 이 링크의 자료를 이용하여 문제에서 제공해주는 google의 url뒤에 /etc/flag.txt를 추가하였습니다.

http://searchbox.web1.sunshinectf.org/submit=Submit&site=file://www.google.com/etc/flag.txt#

이라는 페이로드를 전송하면 문제가 해결됩니다.



오류지적이나 잘못된 사항은 댓글로 남겨주시길 바랍니다!!!
