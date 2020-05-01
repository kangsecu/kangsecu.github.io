---

layout: post
title: "취약한 API 사용"
excerpt: "Try to know api & use it ~_~"
date: 2019-02-04
categories: [Web]
comments: true 

---

이번글의 주제도 역시 OWASP TOP10 중 하나인 취약한 api를 사용하므로써 발생하는 취약점입니다. 이번 취약점 또한 아주 고전적인 취약점입니다. 다룰 내용이 많이 없을 것 같지만... 시작해보도록 하겠습니다. 

------

### 취약한 API 사용 취약점이란?

이름에서 알 수 있듯이, 보안상으로 취약한 API(application programming interface)를 이용하거나, API가 의도되지 않는 방식으로 작동될 경우 발생할 수 있는 취약점입니다. 대표적으로 DNS lookup에 의존한 보안, 완전히 지워지지 않는 힙 메모리, 안전하지 않는 함수이용 등이 있습니다. 

### DNS lookup에 의존한 보안이란?

흔히 도메인 명에 의존하여 보안을 결정하는 경우를 말합니다. 

```
  InetAddress addr = InetAddress.getbyName(ip);
   if addr.getCanonicalHostName().endsWith(“trustme.com”){
 		truested = true;
}
```

이런 경우DNS스푸핑을 통하여 DNS서버 캐시 오염을 통한 공격이 가능해집니다.

```
 if (Ip.equals(trustedAddr)) {
 		trusted = true;
}
```

보안대책으로는 DNS결과를 조회하지 않도록 구현하는 방법이 있습니다. 

### 취약한 API 사용 보안

1. 보안기능을 제공하는 프레임워크 메소드 이용

```
URL url = new URL("http://www.test.com");
URLConnection test1 = url.OpenConnnection();
```

2. 기존의 취약한 API 사용 방지

```
try {

	}catch(Exception e){
    logger.info("Warning");
    }
```

------

### 마무리 

이번 주제는 다룰 내용이 그리 많지 않았어서 글을 짧게 마쳤습니다.  확실히 글을 작성하기 위하여 공부를 하면서 느끼는 것 이지만, XSS나 sqli같은 딱 정해진 기법이 아닌 이러한 류의 주제는 어떻게 글을 작성해야할지 항상 고민이 됩니다. 