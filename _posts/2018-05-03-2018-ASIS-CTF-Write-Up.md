---
layout: post
title: "2018 ASIS CTF Write Up"
excerpt: "너무너무 어렵다."
date: 2018-05-03
categories: [Web]
comments: true 
---

2018 Asis CTF Write up

웹문제만 해결하였고, GAME SHOP,Personal Website,Sharp eyes는 끝까지 해결하지 못하였습니다. 해결하신분 롸업 부탁드려요...

1. Buy Flag

![img](https://t1.daumcdn.net/cfile/tistory/9931FB465AEDB6CA25)

이미지를 확인해보면 http://46.101.173.61/image?name=asis.png 이라는 url을 포함하고 있습니다. 쿠키를 확인해봤는데 플라스크를 이용한 쿠키라고 확인이 되었습니다. 그리고 LFI를 통해 코드릭을 할 수 있습니다. http://46.101.173.61/image?name=app.py에 들어가보면 아래와 같은 코드가 있습니다.

```python
from flask import Flask, Response, render_template, session, request, jsonify
 
app = Flask(__name__)
app.secret_key = open('private/secret.txt').read()
 
flags = {
    'fake1': {
        'price': 125,
        'coupons': ['fL@__g'],
        'data': 'fake1{this_is_a_fake_flag}'
    },
    'fake2': {
        'price': 290,
        'coupons': ['fL@__g'],
        'data': 'fake2{this_is_a_fake_flag}'
    },
    'asis': {
        'price': 110,
        'coupons': [],
        'data': open('private/flag.txt').read()
    }
}
 
@app.route('/')
def main():
    if session.get('credit') == None:
        session['credit'] = 0
        session['coupons'] = []
    return render_template('index.html', credit = session['credit'])
    #return 'Hello World!<br>Your Credit is {}<br>Used Coupons is {}'.format(session.get('credit'), session.get('coupons'))
 
@app.route('/image')
def resouce():
    image_name = request.args.get('name')
    if '/' in image_name or '..' in image_name or 'private' in image_name:
        return 'Access Denied'
    return Response(open(image_name).read(), mimetype='image/png')
 
@app.route('/pay', methods=['POST'])
def pay():
    data = request.get_json()
 
    card = data['card']
    coupon = data['coupon']
 
    if coupon.replace('=','') in session.get('coupons'):
        return jsonify({'result': 'the coupon is already used'})
 
    for flag in card:
        if flag['count'] <= 0:
            return jsonify({'result':'item count must be greater than zero'})
 
    discount = 0
    for flag in card:
        if coupon.decode('base64').strip() in flags[flag['name']]['coupons']:
            discount += flag['count'] * flags[flag['name']]['price']
 
    credit = session.get('credit') + discount
 
    for flag in card:
        credit -= flag['count'] * flags[flag['name']]['price']
        
    if credit < 0:
        result = {'result': 'your credit not enough'}
    else:
        result = {'result': 'pay success'}
        result_data = []
        for flag in card:
            result_data.append({'flag': flag['name'], 'data': flags[flag['name']]['data']})
        result['data'] = result_data
        session['credit'] = credit
        session['coupons'].append(coupon.replace('=',''))
    return jsonify(result)
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

```



이걸 보고 해결하려던 찰나에... 코드를 분석하고 익스하기가 귀찮아서 다른 방법으로 문제를 해결하였습니다. 처음에 플래그를 구입하려하면 POST방식으로 {"card":[{"name":"asis","count":1}],"coupon":""}라고 요청을 하는걸 확인하였습니다.  그래서 CURL명령을 이용하여 복사를 하고 count를 음수로 다시 시도를 해봤습니다.  곱해서 음수를 처리하면 문제가 해결될줄 알았는데, 에러가 납니다. 그래서 여러가지를 입력해보다가 NAN을 시도했더니 문제가 해결되었습니다.

ASIS {th1 @ n_3xpens1ve_FI @ G}



2.Nice Code

![img](https://t1.daumcdn.net/cfile/tistory/990C7E3A5AEDBCE32F)

이번문제는 GET STARTED를 누르니 아래와 같은 코드를 줬습니다.

![img](https://t1.daumcdn.net/cfile/tistory/99DFED495AEDBD8427)

그래서 url에 http://167.99.36.112:8080/admin/index.php/index.php를 넘겼더니 아래와 같은 페이지가 출력됩니다.

![img](https://t1.daumcdn.net/cfile/tistory/99BE87385AEDBD8422)

그래서 코드를 확인해봤습니다.

```php
<?php
include('oshit.php');
$g_s = ['admin','oloco'];
$__ni = $_POST['b'];
$_p = 1;
if(isset($_GET['source'])){
    highlight_file(__FILE__);
        exit;
}
if($__ni === $g_s & $__ni[0] != 'admin'){
    $__dgi = $_GET['x'];
    $__dfi = $_GET;
    foreach($__dfi as $_k_o => $_v){
        if($_k_o == $k_Jk){
            $f = 1;
        }
        if($f && strlen($__dgi)>17 && $_p == 3){
            $k_Jk($_v,$_k_o); //my shell :)
        }
        $_p++;
    }
}else{    
    echo "noob!";
}

```



코드를 보면, 서버는 이 코드를X-Powered-By : PHP / 5.5.9-1ubuntu4.14로 돌리는데, PHP구버전은 배열의 비교의 취약점이 있습니다. 배열의 인덱스는 32비트 정수로 변환되서 intege overflow를 통하여 4294967296은 0이되고 여기서 우리는 b[4294967296]=admin&b[1]=oloco 라는 페이로드를 생각해냅니다.우리가 $K_jk에 저장되어있는 코드를 실행하려면 그 값을 게싱해서 GET전송을 해줘야 하는데, 이것은 ==이 작동할때 0이 정수가 아닌 문자열로 인식되는 PHP의 특징을 이용하였습니다. foreach가 루프로 돌아가며 우리가 GET으로 입력받은 값을 검사합니다.그리고 다음 조건은 x는 17글자보다 길어야합니다. 예를 들어 ?x=kangsecuisveryhandsome같은 값을 넘겨줍니다.  또한$_p == 3 는 우리에게 매개변수가 3개여야 한다는것을 알려줍니다. 두번째 매개변수는 쓸곳이 없지만 $ _k_o == $ K_Jk와 일치시키기 위해 사용할 수 있습니다. 또한 $K_Jk는 $K_Jk($ _v,$ _ k_o)처럼 사용되는데, 여기에서 선언된 함수를 게싱...그래서 우리는 ($ _ k_o == $ k_Jk)를 우회하기 위해 타입 저글링을 사용해야합니다. 다시 확인해보면, $ k_Jk ($ _ v, $ _ k_o)에서 $ _v는 실행될 예정인 시스템 명령, $ _k_o는 명령의실행으로 이어지는 함수입니다. 그러므로 우리는?x=kangsecuisveryhandsome&0=var&/var/flag=readfile을 통하여 플래그를 얻을 수 있습니다.

ASIS{f52c5a0cf980887bdac6ccaebac0e8428bfb8b83}

3.Good WAF

![img](https://t1.daumcdn.net/cfile/tistory/99D158395AEDCBB11B)

이문제는 처음에는 JSON을 이용하여 문제에서 하라는대로 WAF를 하려했으나, 시도를 해보니 WAF를 방지해놨습니다. 그래서 다시 생각을 해본 결과 간단한 SQLi라는 것을 알게되었습니다. 그래서, 로그인창을 찾아보려했으나 로그인 페이지를 몰라서, 아파치 로그에 /?action=log-in 가 있었습니다. http://167.99.12.110/?action=log-in&credentials[0]=valid_user&credentials[1]=password 이러한 페이로드를 통하여 해결하였습니다.

 하지만 이 문제는 그냥 스캐너를 돌려보면 .index.php.swp라는 url에 flag가 있는것을 알 수 있습니다. 

ASIS{e279aaf1780c798e55477a7afc7b2b18}



4.Personal Website

![img](https://t1.daumcdn.net/cfile/tistory/99DF19465AEDD12223)

못풀었어요... Mongo DB 공부중이랍니다. ㅎㅎ...



5.Sharp Eyes

![img](https://t1.daumcdn.net/cfile/tistory/99951A335AEDD2252A)

못풀었어요... 

로그인 페이지에서 계정이 잘못되면 error/1로, 암호가 잘못되거나 누락된 계정이면 error/2로 리다이렉션 됩니다. 처음에는 이문제를 XSS라고 생각하고 삽질을 하다가, 후에는 SQLi라고 생각하고 삽질을 하다 결국 다시 XSS를 이용하여 삽질을 했는데 결국 못풀었습니다...



더 열심히 공부해야겠네요.. 오류지적은 감사히 받겠습니다.