---
layout: post
title: "Threat Modeling Base"
excerpt: "Try to know Threat Modeling Base"
categories: [consulting]
comments: true 
---

이번에는 컨설팅의 필수 중 하나인 위협 모델링에 관하여 공부를 해보자.

<h3>0x0. Threat Modeling</h3>

위협 모델링이란 IT분야에서만 사용되는 단어는 아니며, 말 그대로 목표에 대한 시스템을 조사하여 잠재적인 위협을

모델링하고, 이를 보완할 수 있게 하는 프로세스를 말한다.  또한 이러한 모델링을 기반으로 실제 공격을 시행해보는 것

또한 위협 모델링에 포함된다.



<h3>0x1. STRIDE</h3>

STRIDE란, 각 위협의 앞 글자를 딴 위협 유형 기준으로, MS에서 1999년에 개발.

- 인증, 무결성, 부인 방지, 기밀성, 가용성, 권한 부여같은 보안 속성 고려
- DFD(Data Flow Diagram)의 개체, 프로세스 등에 존재하는 위험 식별

| STRIDE                     | 의미                                                         | 대처 방안                                        |
| -------------------------- | ------------------------------------------------------------ | ------------------------------------------------ |
| **S**pooping Identity      | 공격자가 특정 권한이 있는 사용자인척 위장하는 행위의 공격 방식 | Authentication(인증), 전자 서명                  |
| **T**ampering with data    | 목적을 위해 시스템 내부 데이터를 악의적으로 수정하는 공격 방식 | Integrity(무결성 검증), 해쉬, 전자 서명          |
| **R**epudiation            | 악의적 활동 이후에 해당 활동에 대해 부인하는 것              | Non-Repudiation(부인 봉쇄), 전자 서명, 감시 로그 |
| **I**nformation Disclosure | 보호된 정보에 대한 노출                                      | Confidentiality(기밀성 검증), 암호화             |
| **D**enial of Service(DoS) | 서비스에 대한 신뢰되지 않은 접근을 통한 서비스 거부 공격     | Availability(가용성 검증), 필터링                |
| **E**levation of Privilege | 권한이 없는 사용자가 다른 사용자의 권한 습득                 | Authorization(권한 검증)                         |



<h3>0x2. DREAD</h3>

DREAD는 각 위험의 앞 글자를 딴 위험도 분류로, MS-SDL에서 사용하는 모델링 방식이다.

- 각 항목에 대한 보안 위험도를 1~10점으로 평가
- 1에서 10으로 갈수록 심각성 또는 발생 확률이 상승
- 위험도 = 전체의 산술평균(전체를 더한 값/5)

| DREAD                                  | 피해 의미                                      | 위험도                                                       |
| -------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------ |
| **D**amage potential(예상 피해)        | 공격의 피해가 얼마나 클 것인가?                | 0 = 없음 , 5 =개별 사용자 데이터가 손상되거나 영향을 받음, 10 = 전체 시스템의 데이터가 피해 |
| **R**eproducibility(재현 확률)         | 공격을 성공할 확률이 얼마나 되는가?            | 0 = 없음, 5 = 이전의 스텝을 필요로 하며, 일부 사용자만 가능, 10 = 모든 사용자가 아무 인증 없이 가능 |
| **E**xploitability(공격 용이도)        | 공격을 위해 어느정도의 노력과 기술이 필요한가? | 0 = 없음, 5 = PoC코드가 인터넷 상에 존재하거나, 공격 가능한 툴 이용, 10 = 단순히 웹 브라우저만을 이용 |
| **A**ffected users(영향을 받는 사용자) | 공격에 어느정도의 인원이 영향을 받는가?        | 0 = 없음, 5 = 일부의 사용자, 10 = 전체 사용자                |
| **D**iscoverability(발견 용이도)       | 취약점을 발견하기 쉬운가?                      | 0 = 없음, 5 = 추측 or 로그기록 , 모니터링을 통한 발견, 10 = 웹 브라우저에서 그냥 출력 or 검색 엔진을 통하여 확인 가능 |



<h3>0x3. VAST</h3>

VAST는 Visual, Agile, Simple Threat modeling의 약어로 인프라 및 시스템 전체에 대한 모델링으로, 과거의 개발 방법론에 내제된 보안적 결함을 제거하는 모델링 방법론 



<h3>0x4. P.A.S.T.A</h3>

PASTA는 The Process for Attack Simulation and Threat Analysis의 약어로 리스크 기반의 위협 모델링 프레임워크이다. PASTA의 목적은 방어자가 자산 중심의 완화 전략을 개발할 수 있는 인프라에 대한 오펜시브의 관점으로 모델링을 하는 것이다.

- 동적인 위협을 식별 및 열거 및 수준에 맞는 7단계의 프로세스 구성

  | PASTA                             | 의미                                                         |
  | --------------------------------- | ------------------------------------------------------------ |
  | Define Objectives                 | 비즈니스 목적 정의 단계                                      |
  | Define Technical Scope            | 위협 분석할 인프라, 애플리케이션, 시스템의 범위를 정하는 단계 |
  | Application Decomposition         | DFD를 이용하여 애플리케이션을 분해하는 단계                  |
  | Threat Analysis                   | 공격 시나리오 분석을 통해 실제 위협을 분석하는 단계          |
  | Vulnerability & Weakness Analysis | 실제 취약점 벡터를 분석하는 단계                             |
  | Attack Modeling                   | Attack Tree등을 개발하는 공격 모델링 단계                    |
  | Risk & Impact Analysis            | 위협에 따른 정량적/정성적 리스크의 영향을 분석하는 단계      |

  

<h3>0x5. MS-SDL</h3>

MS-SDL은 추후에 따로 업로드 할 내용인데, Security Development Lifecycle로 MS사에서 개발한 보안 개발 수명 주기를 의미한다. Dev-ops를 하는 과정에서도 자주 사용되는 요소로, 비교적 쉽고 효과적으로 위협 모델링이 가능하고, 보안 문제를 인식하고 식별할 수 있어서 전체적인 개발 코스트가 현저히 줄어든다.

1. 교육
2. 계획/분석
3. 설계
4. 시험/검증
5. 배포/운영
6. 대응



<h3>0x6. OCTAVE</h3>

OCTAVE는 리스크 관리를 체계적으로 수행하기 위해 운영자 중심의 위협 모델링을 제공한다. 주로 내부TF를 구성하여 정보 수집 및 분석, 전략 개발등의 자가 진단을 추진하는 특징이 있다. 아래의 순서에 맞게 진행된다.

| OCTAVE                        | 의미                                               |
| ----------------------------- | -------------------------------------------------- |
| Organizational View           | 조직 자산에 기초하여 위협 프로파일을 구축하는 단계 |
| Technological view            | 인프라의 취약성을 정의하는 단계                    |
| Strategy and Plan Development | 보안전략 및 계획 개발 단계                         |



<h3>0x7. TVRA </h3>

TVRA는 통신 시스템의 위협 분석 및 리스크 평가를 위한 방법론으로, 위협 대상이 되느 주요 자산을 파악하고, 현장에서 개인의 안전과 주요 인프라의 운영에 미치는 영향에 대한 평가를 위한 시나리오를 도출한다.

시나리오 : 식별된 위협, 위협에 영향을 받는 개체 및 결과를 포함한 관련 조건으로 구성된 가상의 상황을 의미

| TVRA                                                       | 의미                                                   |
| ---------------------------------------------------------- | ------------------------------------------------------ |
| Identification of Target Of Evaluation                     | 평가 대상을 식별하는 단계                              |
| Identification of objectives                               | 해결해야 할 보안 목표를 식별하는 단계                  |
| Identification of functional security requirements         | 기능적 보안 요구사항을 식별하는 단계                   |
| Systematic inventory of the assets                         | 자산을 물리적, 인적, 논리적으로 분류하는 단계          |
| Systematic identification of vulnerabilities               | 취약점을 체계적으로 식별하는 단계                      |
| Calculation of the likelihood of the attack and its impact | 공격 가능성과영향도를 정량화하는 단계                  |
| Establishment of the risks                                 | 리스크를 결정하는 단계                                 |
| Security countermeasure identification                     | 리스크를 완화하기 위한 보안 대책을 식별하는 단계       |
| Countermeasure cost-benefit analysis                       | 리스크  보안 대책에 대해 코스트와 이점을 분석하는 단계 |
| Specification of detailed requirements                     | 상세한 보안 요구사항을 명세하는 단계                   |



<h3>0x8. STPA-sec</h3>

STPA-sec은 해저드 분석 기법을 적용한 방법론이다.

| STPA-sec                                             | 의미                                                         |
| ---------------------------------------------------- | ------------------------------------------------------------ |
| Establishing the systems engineering foundation      | Loss를 식별하는 단계                                         |
| Creating a model of the high level control structure | 상위 수준의 제어 구조도를 작성하는 단계                      |
| Identifying unsafe/unsecure control actions          | 명령이 로스로 이어질 수 있는 잘못된 경우를 식별하는 단계     |
| Developing security requirements and constraints     | 안전하지 않은 명령을 제거하기 위한 보안 사항을 개발하는 단계 |
| Identifying causal scenarios                         | 보안 사항을 위반할 수 있는 다양한 시나리오를 분석하는 단계   |



<h3>0x9. Attack Tree</h3>

Attack Tree는 자산이나 정해진 목표의 공격 시나리오를 제시하는 개념도이다.

<hr>

<h3> 0x. References</h3>

https://madeinjeon.tistory.com/33?category=645887

https://owasp.org/www-community/Application_Threat_Modeling

https://docs.microsoft.com/en-us/previous-versions/msp-n-p/ff648644(v=pandp.10)?redirectedfrom=MSDN

https://docs.microsoft.com/ko-kr/azure/security/develop/threat-modeling-tool-getting-started

https://ichi.pro/ko/post/160738763448166

https://docs.microsoft.com/ko-kr/azure/security/develop/threat-modeling-tool

