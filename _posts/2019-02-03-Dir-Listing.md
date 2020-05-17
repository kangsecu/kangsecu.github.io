---
layout: post
title: "Dir Listing"
excerpt: "Try to know dir listring & use it ~_~"
date: 2019-02-03
categories: [Web]
comments: true 
---


### Dir Listing이란?

디렉토리 리스팅 취약점으로, 웹 어플리케이션의 브라우징하는 모든 페이지를 보여준다. 최초 제작 목적은 문서 탐색기처럼 원하는 문서와 페이지를 바로 접근할 수 있도록 만든것이지만, 해킹에서는 공격자가 강제 브라우징을 통해 서버내의 모든 디렉토리를 인덱싱할 수 있게되어 웹어플리케이션 및 서버내의 주요 정보가 노출될 수 있는 취약점.



![img](https://k.kakaocdn.net/dn/Rzoe0/btqz6tH6nLC/Jd1dthe0k0XJUrmvCN94e1/img.png)webhacking.kr 문제 풀이과정 중



위의 이미지는 실제 운영중이 아닌 워게임 사이트중 하나인 webhacking.kr 문제를 해결하는 도중에 Dir Listing을 시도한거다. 보다싶이 해당 경로내의 모든 문서등이 드러나서 서버의 구조를 파악할수 있고, 더욱 취약점에 빠르게 접근할 수 있다.

### Dir Listing 발생 이유?

 보통은 노출되지 말아야할 웹 서버 경로에 대한 접근을 차단하지 않아서 발생하는 경우가 많다. 가장 대표적인 예시를 들자면 예를들어 [https://kangsecu.github.io/user/rank/rank.php?~](https://kangsecu.tistory.com/) 의 경로가 있다고 가정해보자  이 상황에서 만약 https://kangsecu.github.io/blog/user/ 까지만 입력을 한다면 user디렉토리의 하위 디렉토리와 보유 파일들이 출력이 된다. 이러한 과정에서 서버 내부의 데이터가 유출되게된다.

### Dir Listing 공격 패턴? 

가장 많이 사용되는 공격패턴은 url에서 해당 파일명을 제외하고 상위 Dir만 검색을 하는 것이다.또한, 구글 고급 검색에 Parent Dirctory를 추가하여 검색하는 방법, intitle:"index of"등을 검색하여 찾는 방법등이 있다.



![img](https://k.kakaocdn.net/dn/c36rBu/btqz73n5Ibm/dsepqXh2R9GdUiN2NiIDjk/img.png)구글에 검색



위의 이미지는 구글에 직접 검색해본 것. 이렇게 수동적으로 하는 방법 이외에도 OWASP에서 보안 점검용으로 제공한 DirBuster같은 프로그램을 이용하는 방법도 존재



![img](https://k.kakaocdn.net/dn/7JmFa/btqz7pFng7F/ruiRvrON3GBgbw7SskrniK/img.jpg)DirBuset 실행화면


[ Category:OWASP DirBuster Project - OWASPThis historical page is now part of the OWASP archive. This page contains content that is outdated and is no longer being maintained. It is provided as a courtesy for individuals who are still using these technologies. This page may contain URLs that werewww.owasp.org](https://www.owasp.org/index.php/Category:OWASP_DirBuster_Project)

 

### Dir Listing 보안 방법?

여러가지 보안 방법이 존재하지만 그중에 간단하게 두가지만 다뤄보자

1. 우선 가장 대표적인 방법으로 아파치의 http설정 파일을 수정하는 방법. vi/etc/httpd/conf/httpd.conf 파일을 접근하면 Options Indexes FollowSymLinks 라는 부분이 있는데 이 부분에서 Indexes를 삭제하면 된다 . 그렇다면 위와 같은 방법으로 시도를 했을때, 하위 디렉토리나 데이터가 표시되지 않고, 403(접근 거부 메시지)/Forbidden등의 에러가 발생한다. 하지만 존재하지 않는 Dir로 시도를 했을때는 보통 404에러 메시지가 나오는데 위와 같은 방법을 적용했을때 403에러 메시지가 발생한다면 해당 Dir이 존재하긴 한다는 정보를 주게된다. 또한 403에러 메시지 하단에 몇몇 정보를 제공해주기 때문에 여러모로 취약

2. 위의 방법이 공격자들에게 최소한의 정보라도 제공을 해주기 때문에, 아예 이러한 공격을 대비한 페이지를 따로 제작을 해두거나, 서버내의 다른 경로로 리다이렉트를 시켜버린다. 대표적으로 네이버 같은 경우는 존재하지 않는 경로로 접근을 시도하면 아예 메인 페이지로 접근을 하게 설정되어있다. 이러한 방법또한 아파치 설정파일에서 수정을 하는것. 마찬가지로 vi/etc/httpd/conf/httpd.conf 파일에 접근하여 ErrorDocument 403과 404를 리다이렉트 시키고자 하는 url로 수정하면 된다.
