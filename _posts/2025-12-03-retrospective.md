---
layout: post
title: "2025년 회고: 엔터프라이즈의 안정성과 스타트업의 속도, 그 사이에서"
subtitle: "하이브리드 프로덕트-플랫폼 아키텍트로의 진화를 꿈꾸며"
date: 2025-12-03
categories: [Retrospective, Career, Engineering]
tags: [Review, 2025, Growth, Product Engineer, Platform Engineer, FinOps, IAM]
author: jawsbaek
---

소프트웨어 엔지니어링 생태계에는 **'엔터프라이즈의 안정성(Enterprise Stability)'**과 **'스타트업의 민첩성(Startup Agility)'**이라는 두 가지 거대한 흐름이 존재합니다. 보통의 엔지니어는 커리어를 시작하며 이 중 하나의 생태계에 속하게 되고, 그곳의 DNA를 물려받습니다.

삼성 SDS라는 거대한 엔터프라이즈 IT 기업에서의 3년 차. 그리고 '케어링 노트(Caring Note)'라는 사이드 프로젝트를 통한 스타트업 방식의 질주. 2025년은 이 상반된 두 정체성이 충돌하고 융합하며, **'하이브리드 프로덕트-플랫폼 아키텍트(Hybrid Product-Platform Architect)'**라는 새로운 지향점을 발견한 해였습니다.

단순히 어떤 기술 스택을 썼느냐가 아닌, 엔지니어로서의 철학과 성장 가능성에 집중했던 저의 2025년을 회고합니다.

## 1. The Shark Persona: 127개의 커밋과 행동주의

팀 내 압도적 기여도 1위, 127개의 커밋.
저를 나타내는 닉네임 **'나는상어당(The Shark)'**처럼, 올해는 정말 쉴 새 없이 헤엄쳤습니다. 주니어 엔지니어에게 요구되는 것이 티켓을 처리하는 '수동적 수행'이라면, 저는 스스로 문제를 발굴하고 해결하는 **'높은 주도성(High-Agency)'**을 증명하고 싶었습니다.

하지만 이 지칠 줄 모르는 운동 에너지(Kinetic Energy)는 양날의 검이기도 합니다. 초기 스타트업 단계나 '케어링 노트'와 같은 프로젝트에서는 생존의 동력이었지만, 이제는 변화가 필요한 시점임을 깨닫습니다.

**2025년의 과제:**
단순한 개인의 속도(Velocity)를 넘어, 팀 전체의 레버리지(Leverage)를 높이는 방향으로 나아가려 합니다. '나의 코드'가 아닌 '우리의 아키텍처'를 고민하는 것, 그것이 'Shark'가 다음 단계로 진화하는 방법일 것입니다.

## 2. Platform Engineer: 엔터프라이즈에서 배운 '단단함'

삼성 SDS에서의 경험은 저에게 **'플랫폼 엔지니어'**로서의 단단한 기반을 만들어주었습니다. 특히 클라우드 보안(Cloud Security)과 IAM(Identity and Access Management) 영역은 제 커리어의 가장 강력한 해자(Moat)가 되었습니다.

### 🔑 IAM과 Keycloak: 인증은 단순한 로그인이 아니다
Keycloak을 활용한 SSO(Single Sign-On) 구현은 단순한 API 연동을 넘어 OAuth 2.0, OIDC 같은 복잡한 프로토콜의 상태 머신을 다루는 일이었습니다. 제로 트러스트(Zero Trust) 시대에 **"Identity is the New Perimeter(ID가 새로운 보안 경계)"**라는 명제를 몸소 체험하며, 핀테크나 글로벌 SaaS 수준의 인증 아키텍처를 이해하게 되었습니다.

### 🏗️ Multi-Tenancy와 인프라의 규율
SCP(Samsung Cloud Platform)의 IAM을 다루며 멀티 테넌시(Multi-Tenancy) 환경에서의 데이터 격리와 RBAC(Role-Based Access Control)의 성능 이슈를 고민했습니다. 또한, Helm과 Batch 처리를 통해 '선언적 인프라'와 대용량 트랜잭션의 안정성을 경험했습니다. 이는 스타트업 네이티브 엔지니어들이 쉽게 경험하기 힘든, **'규모(Scale)'와 '규율(Rigor)'**이라는 자산이 되었습니다.

## 3. Product Engineer: '케어링 노트'로 증명한 문제 해결력

회사가 '수비(Defense)'라면, 사이드 프로젝트인 **[케어링 노트(Caring Note)](https://caring-note.framer.website/)**는 '공격(Offense)'이었습니다. 여기서 저는 백엔드 개발자를 넘어, **프로덕트 엔지니어(Product Engineer)**로 변모했습니다.

### 🚀 4배의 효율성(4x Efficiency)
가장 자랑스러운 성과는 "상담 효율성을 400% 증대시켰다"는 비즈니스 지표입니다.
* **Full-Stack Pivot:** Java/Spring에 갇히지 않고 React, TypeScript, Zustand를 도입해 프론트엔드까지 영역을 확장했습니다.
* **Business Impact:** 약사들의 워크플로우를 분석하고 병목을 찾아내 기술로 해결했습니다. 코드가 아닌 '비즈니스 문제'를 해결하는 데 집중했습니다.

### 🛠️ Lefthook과 엔지니어링 문화
혼자 하는 프로젝트일수록 '시스템'이 필요했습니다. Lefthook을 도입해 커밋 단계에서 린트와 타입 체크를 강제하고, 상세한 문서화를 통해 "미래의 나"와 "잠재적 동료"를 위한 배려를 시스템화했습니다. 이는 제가 지향하는 테크 리드(Tech Lead)의 모습이기도 합니다.

## 4. Strategic Differentiators: 차별화된 무기들

올해 저는 남들과 다른 '한 끗'을 만들기 위해 세 가지 전략적 투자를 감행했습니다.

1.  **AI Top 100 Bronze 수상:** AI를 단순한 붐으로 보지 않았습니다. ["Bmad Method(AI야 돈 줄게, 제대로 해)"](https://bsh998.github.io)와 같은 글을 통해, AI를 '확률적 도급업자'로 정의하고 이를 실무 워크플로우에 통합하는 방법을 고민했습니다.
2.  **FinOps Certified Practitioner:** "돈을 아는 엔지니어"가 되고 싶었습니다. 고금리 시대, 클라우드 비용 최적화는 선택이 아닌 필수 역량입니다. 기술과 재무의 가교 역할을 할 준비를 마쳤습니다.
3.  **SAFe Agilist:** 엔터프라이즈급 조직이 어떻게 민첩성을 유지하는지(Scaled Agile)를 배웠습니다. 이는 대규모 조직의 언어로 소통할 수 있음을 의미합니다.

## 5. 2026 Roadmap: 도약을 위한 전략

2025년이 **'축적(Accumulation)'**의 시간이었다면, 2026년은 **'변환(Transformation)'**의 시간이 될 것입니다.

* **Identity:** "SDS 3년 차 개발자"에서 **"풀스택 프로덕트 아키텍트"**로 리브랜딩합니다.
* **Focus:** 개인의 기여(Commit)보다 팀의 임팩트(Impact)에 집중합니다.
* **Action:** * Caring Note에 RAG(검색 증강 생성) 기술 도입 및 FinOps 원칙 적용
    * 기술적 깊이(Deep Dive)와 비즈니스 임팩트를 연결하는 아티클 발행
    * 네이버, 카카오, 라인, 쿠팡, 토스(NKLCB) 등 탑티어 서비스 기업으로의 도전

## 마치며

삼성 SDS의 방패(보안, 규정, 규모)와 케어링 노트의 창(속도, 사용자 경험, 실행력), 그리고 FinOps라는 지도.
이 세 가지를 갖춘 저는 이제 단순한 코더(Coder)가 아닌, 비즈니스와 기술을 잇는 **'하이브리드 아키텍트'**로서 2025년의 바다로 나아갑니다.

상어는 멈추면 가라앉습니다. 하지만 이제는 무작정 빨리 헤엄치는 것이 아니라, 더 넓은 시야로 더 큰 흐름을 타는 법을 배웠습니다. 2026년, 더 큰 파도를 기대해 봅니다.

---
*If you are interested in my journey or want to discuss Product Engineering & Cloud Security, feel free to connect!*
