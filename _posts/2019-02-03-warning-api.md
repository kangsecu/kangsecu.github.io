---

layout: post
title: "취약한 API 사용"
excerpt: "Try to know api & use it ~_~"
date: 2019-02-04
categories: [Web]
comments: true 

---

### 취약한 API 사용 취약점이란?

이름에서 알 수 있듯이, 보안상으로 취약한 API(application programming interface)를 이용하거나, API가 의도되지 않는 방식으로 작동될 경우 발생할 수 있는 취약점. 대표적으로 DNS lookup에 의존한 보안, 완전히 지워지지 않는 힙 메모리, 안전하지 않는 함수이용 등이 있다.

### DNS lookup에 의존한 보안이란?

흔히 도메인 명에 의존하여 보안을 결정하는 경우를 말함

```
  InetAddress addr = InetAddress.getbyName(ip);
   if addr.getCanonicalHostName().endsWith(“trustme.com”){
 		truested = true;
}
```

이런 경우DNS스푸핑을 통하여 DNS서버 캐시 오염을 통한 공격이 가능하다.

```
 if (Ip.equals(trustedAddr)) {
 		trusted = true;
}
```

보안대책으로는 DNS결과를 조회하지 않도록 구현하는 방법이 있다.

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
