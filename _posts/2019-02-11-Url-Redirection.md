---
layout: post
title: "Url Redirection"
excerpt: "Try to know url redirection & use it ~_~"
date: 2019-02-11
categories: [Web]
comments: true 
---

여러가지 사정으로 가상머신으로 환경구축 후 진행해야 하는 주제들은 좀 후에 다룰 예정입니다. 그래서 이번에 다뤄볼 주제는 URL Redirection입니다. 이번에 다뤄볼 URL Redirection은 OWASP에서 공개한 2017 TOP10중 하나입니다. 자체로도 매우 취약하지만 보통은 2차 공격을 진행하는 베이스로 많이 이용되는 기법입니다. 

------

### URL Redirection이란? 

URL Redirection은 URL Forwarding 이라고도 불리는 기술로, 클라이언트가 의도하지 않은 url로 접속시키는 공격 방식입니다. 신뢰되지 않은 URL주소로 자동연결 시키는 기법이라고 하며, 주로 피싱등에 이용되는 해킹 기법입니다. 대부분 로그인이나 다양한 이동 파라메터 등 크로스사이트스크립팅(XSS) 과 비슷하게 많이 발견되는 취약점입니다. 페이지를 이동하여 악성코드가 삽입되어 있는 페이지 등으로 강제 이동시켜 추가적인 공격을 성공시키기 위한 베이스로 사용합니다.



![img](https://k.kakaocdn.net/dn/5CTi3/btqAnxjLNoZ/1T6XqxAwLuWYt79r9tqeYK/img.png)평소 접속하는 익숙한 url주소로 접속하기에 자주 당함



### 어디서 왜 발생하나? 

위에서 언급한대로 보통 로그인, 로그아웃 등이나 페이지 이동 파라미터 등에서 검증을 수행하지 않은 경우 주로 발생합니다. 검증되지 않은 분기 페이지에서 주로 발생합니다. 거의 비슷한 패턴인데, 페이지를 이동 시키는 요청(정상적인 리다이렉션 요청)에 대해 공격자에 의해 변조된 URL 값을 넘겨주어 피해자가 다른 사이트로 넘어가도록 유도하는 과정에서 발생합니다. location헤더 등에서 주로 이용됩니다.

간단하게 php를 이용하여 예를 들어보도록 하겠습니다.

```
<?php

$redirect_url = $POST['url'];
header("Location : .$redirect_url");

?>
```

위와 같이 리다이렉션을 수행하는 함수가 웹사이트 내의 존재할때, 해커는 간단하게 [http://example.com/redirect?url=http://hacekr.com ](http://example.com/)을 이용하여 공격을 할 수 있습니다.  또한, 간단하게 php를 이용하여 아래와 같이 리다이렉트 코드를 작성할 수 있습니다.

```
<?php
header("HTTP/1.1 301 Moved Permanantly");
header("Location : http://hackertest.com");
?>
```

 

### 보안 방법

간단하게 외부 사이트로 리다이렉션되는 함수나 메소드가 있는지 확인하면 됩니다. 또, 리다이렉트 하는 함수가 외부 입력값을 이용하는지 확인하고, 외부 입력값의 주소가 신뢰가는지 확인하면 됩니다.  다른 방법으로는 시큐어코딩이 있습니다.

화이트리스트를 이용하는 시큐어코딩을 보겠습니다. 

```
String Url = request.getParameter("url");
response.sendRedirect(url);
```

이러한 방식의 Url 파라미터에 대한 검증을 수행하지 않는 코드는 매우 취약할 수 있습니다. 위의 코드이 경우 해커는

<a href="http://example.com/redirect?url="http://hackertest.com">button</a> 등의 코드를 이용하여 피해 클라이언트를 해커가 유도하는 url로 리다이렉트 시킬 수 있습니다. 

```
String allowURL[] = {"http://site1.com", "http://site2.com"};
String nurl= request.getParameter("nurl");
try{  
Integer n = Integer.parseInt(nurl)
if (n>=0 && n=<2)
response.sendRedirect(allowURL[n]);
}
catch (numberformatexpection nfe)
```

하지만 이렇게 코드를 접속될 url들을 지정해주면 더욱 안전해집니다. (완전 안전한건 아님)

### 우회 기법

여러가지 보안방법이 있다면 그에 대항하는 우회 기법도 있기 마련입니다.제가 자주 참고하는 블로거인 [https://www.hahwul.com](https://www.hahwul.com/) 님께서  아주 자세히 다뤄주셨습니다! 들어가셔서 읽어보시면 아주 큰 도움이 될 것 같습니다. 

------

###  

### 마무리

“OWASP Top 10 한글 설명서” 요약 페이지의 마지막을 보면 알 수 있는데, 취약점 분포가 드물고, 탐지 가능성 쉬움으로 평가가 되어 있는 취약점입니다. 그래서인지 기술적으로 탐지가 편리해서 관심이 높지 않습니다. 파라미터에 어플리케이션명 이나 도메인 주소가 포함되어 있는지 육안으로 구분이 되기 때문에 분석을 한 후 공격이 가능합니다. 하지만 그렇다고 해서 절대 무시하고 넘길 취약점은 아닙니다. 사소한것 하나에서부터 정보수집이 시작되기 때문에 하나하나 신경을 써야합니다. 실제로 많이들 이용하는 네이버 사이트도 이러한 리다이렉트 취약점이 많이 제보되고 있습니다. 애초에 Url Redirection자체가 편리한 웹사이트 이용을 위해서 개발된거긴 하지만, 해커들은 절대 의도 그대로 사용하지 않습니다.  빨리 환경구축이 되서 직접 테스트를 하고 실습하는 내용을 올리고싶습니다.