---
title: "SK AI SUMMIT 이모 저모"
categories:
  - ai 
tags: 
  - ai
  - SK
  - AWS
  - Microsoft
  - Lambda
  - allganize
  - penguin solutions
  - openAI
  - Perplexity
---
11월 4일 SK AI SUMMIT 참석 후 키노트 세션, 부스 등 내용을 정리한 글입니다. 오전에는 주로 부스를 참석했고, 오후에는 두 개의 키노트 세션을 참석했습니다.
개인적인 감상 내용을 정리한 것으로, 행사 전체의 내용을 담지 못하는 점 참고바랍니다.


# Interesting booths
- [Nvidia AI Enterprise](https://www.nvidia.com/en-us/data-center/products/ai-enterprise/): AI 아키텍처 구축 플래폼
- [Microsoft phi silica](https://learn.microsoft.com/ko-kr/windows/ai/apis/phi-silica): 윈도우 로컬 NPU 언어 모델
- [allganize](https://www.allganize.ai/ko/home): 5년 동안 쌓은 VOC를 통한 rule based model로 전세계 최고 성능 RAG
- [AWS outposts](https://aws.amazon.com/ko/outposts/servers/): 온프레미스 서버에 AWS 하드웨어 서버를 추가해 온프레미스-클라우드를 낮은 latency로 연결하는 서비스
- [EventCAT](https://www.eventcat.com/): 41개 국어 AI 동시통역 서비스(AI SUMMIT 통역도 이 서비스로 이루어졌다)
- [Starburst](https://www.starburst.io/): Trimo 기반 데이터 분석 플랫폼
- [Lambda](https://lambdalabs.com/): Gaas(Gpu as a service) 내년 3월 H200 2000대 도입 회사


# EXHIBITION
Exhibition의 경우에는 질의응답 내용을 주로 기록했습니다.
### Microsoft
Physical device (npu pc) + microsoft server 기반 Edge hybrid AI computing 서비스를 소개했다.
1. 윈도우는 사실 개발자 입장에서, 발열과 속도 면에서 거부감이 있는데, 어떻게 생각하는지?
* NPU를 윈도우 pc에 도입하게 되면서, AI와 같은 고성능 컴퓨팅의 발열을 1/10이하로 줄였고, 이러한 부분들이 개발자에게도 메리트를 줄 수 있을 것이라고 생각한다.
2. 가격정책은 어떻게 되는지?
* 로컬 AI는 다운로드 형태로 사용하고, 서버가 필요할 시에 구독되어 있는 마이크로소프트 코파일럿을 호출하는 형태로 가격과 성능 모두를 해결할 수 있을 것으로 보인다.


### Moloco
몰로코는 머신러닝 기반 모바일 광고 솔루션을 제공하는 글로벌 테크 기업입니다. 2013년 실리콘밸리에서 창업했으며, 웹 사이트에서 구글, 유튜브 광고 등에 솔루션을 제공하고 있습니다. 현재는 국내에서 티빙에서도 OTT추천 서비스를 제공하고 있습니다.
1. 몰로코가 이번 부스 참여에서 목표로 한 것은?
* 몰로코는 두몰센으로 묶여서 회사 자체로서는 유명하지만, 서비스나 기술력에 대해서 알려진 점이 적어서 이번에 참여하게 되었다. 특히 개발자들이 이름만 아는 경우가 많아서 채용 문의나 뭐하는 회사인지 질문이 많았다.
2. 광고 솔루션의 효과는 어떻게 증명하는지?
* 매출, 다운로드 수, 배너 클릭 등 다양한 지표를 통해 몰로코가 제공하는 서비스가 유저에게 주는 실제 효과를 보여준다.


### Allganize
1. 어떻게 본인들의 솔루션이 가장 뛰어난 RAG 모델이라고 답할 수 있는지?
* 우리는 2017년 일본 금융 회사의 RAG 모델을 서비스하면서 출발했다. 미국과 일본, 한국의 여러 법률 금융 회사와 계약을 하면서, 우리는 모델의 성능이 부족해질 때 부터 계속해서 rule-based로 모델을 발전시켜 왔다. LLM 모델이 발전하는 와중에도, 우리는 계속해서 정확도를 높이기 위한 작업에 몰두했고, 지금 우리가 공개한 [hugging face dataset](https://huggingface.co/allganize)에서 우리를 앞서는 모델은 없다.
2. 자체적인 Foundation model을 만들지는 않는지?
* 자체적인 모델을 만들긴 하지만, 이는 보안상 외부 AI 모델을 사용할 수 없는 고객들에 한해서 제공한다. 컨설팅할 때, 웬만하면 비공개 모델들을 사용하도록 가이드하고 있다.


### EventCAT
1. 기술 기반에 대해서 설명해달라.
* 우리는 구어체 기반 데이터셋을 자체 구축하고, 이 기반으로만 학습한 모델을 사용하고 있다. 특히, 데이터셋 구축과 모델 평가에서 전문 통역사들에게 검수를 받아 고품질의 모델이 될 수 있도록 보장한다.
2. ChatGPT에서도 동시 통역이 되는데, 차별점을 얘기한다면?
* 우리는 화자의 뉘앙스까지도 반영해서 통역하고, UI적으로 미팅을 하는 사람들에게 편의성을 줄 수 있도록 최적화시키고 있다. 레이턴시, 편의성, 구어체 기반 통역 등 전문 통역 서비스로서의 고유한 입지를 가지고 있다고 생각한다.


### Lambda
1. GPU as a service가 이미 시장에 있는 CSP들에서 제공하는 gaas에 비해서 경쟁이 쉽지 않을 것 같다.
* 람다가 제공하는 것은 우선 가격적인 측면에서 가장 큰 이점을 준다. 일반적인 GPU 시장에서 컴퓨팅 코스트는 지나치게 비싸고, 이 부분에서 이점을 주는 것이 가장 큰 매력이다. 또 하나는, 완전히 GPU 컴퓨팅 최적화를 위한 모든 지원을 한다는 것이다. 성능이 완전히 중요한 회사 입장에서는, 엄청난 메리트가 된다.
2. 만들어진 모델을 서비스에 붙이려면 다른 CSP들과 연계가 되어야 할 것 같은데,
* 람다는 3개의 대형 CSP (Azure, AWS, GCP)와 클라우드 커넥트라는 기능을 통해서 직접적인 연결을 제공한다. 


### SK


#### A.(에이닷)
1. 에이닷의 화자 인식 능력이나, 일상 대화 인식 능력이 떨어진다고 생각한다. 이러한 의견에 대해서 어떻게 생각하는지?
* 이러한 VOC가 많았다. 예를 들어, 부부간 대화를 자매로 인식하거나 남편과 아내를 뒤 바뀌는등의 VOC가 많았다. 현재 집중적으로 발전시키는 부분이고, 대화 컨텍스트 인식 향상에 집중하고 있다.
2. 에이닷의 향후 목표가 무엇인가? 단순 요약은 클로바+chatgpt로 대체되지 않는가?
* 에이닷의 목표는 첫 번째로, 핵심 컨텍스트를 소멸시키지 않고 인식해 유저에게 전달하는 것이고, 두 번째는 향후 일정을 제안하는 것이다. 할 일이나 미팅 등의 스케쥴링 추천과 UI를 집중할 예정이다.


#### AI agent
1. AI agent에 personal한 정보들을 장기기억으로 제공하는가?
* 앞으로 목표이지만 현재는 지원하지 않는다.


#### Starburst (데이터 분석 플랫폼)
1. 오픈소스와의 차별점은 무엇인가?
* Starburst는 플랫폼과 Saas를 모두 지원하며, 현재 글로벌 상품으로서 AWS 데이터 분석 플래폼에도 쓰이고 있다. 특히 DB를 여러 개 쓰는 경우, 클라우드와 온프레미스 DB를 모두 integrate하여 정보 분석을 제공한다.


#### SASE(클라우드 자원 보안 프로그램 솔루션)
1. 아키텍처 상에 Agent설치가 필수로 보이는데, 그러면 새로운 OS에 맞추어서 계속해서 agent를 개발해야 한다. Agentless를 고려하지는 않는가?
* 고려하고 있으나 현재는 agent방식으로 통제하고 로그를 수집한다.


# Keynote session
키노트 세션의 주 내용은, AI의 현재와 미래입니다. 특히, 하드웨어 측면에서 지금 마주하고 있는 세 가지 챌린지 (인프라, 하드웨어, 환경) 측면에서 주로 얘기가 나왔습니다. 저는 제가 주로 관심있는 분야인 AI 기술에 대해서 주로 정리하였습니다. 

ARM, AMD, SK등 반도체 혹은 소자 회사들에서 가장 초점으로 맞추고 있는 점은 전력 효율입니다. 더 작은 사이즈의 칩, 더 짧은 전달 거리, 더 타이트한 공간 사용을 통해서 저항을 줄이고 에너지 효율을 올리고자 합니다. 다른 측면에서, 구축 업체들은 대형 데이터센터 구축을 위한 최적의 환경을 조성하고자 합니다. 전력, 냉각, 안정성이 주요한 이슈입니다. 


### The Vision for the Future of AI (Rani Borakr)
이 강연에서, Rani Borkar는 현재의 AI 혁명을 아폴로 프로젝트에 비견되는 새로운 세상과 혁신의 장으로 비유했다. 

AI는 지금 이 세대로부터 시작되고, 앞으로 어떤 변화를 일으킬지 모르는 상황이다.
impossible became possible
AI is the opportunity of the lifetime
Consequential industry at a consequential time
AI 산업에서는 현재 하드웨어가 밀리는 상황이고, 3s 혁신이 필요하다.
- speed
- scale
- sustantibillity

1. speed
속도, 플롭스, 대역폭 등 모든 속도를 개선할 수 있는 혁신이 총 투입되고 있다. HBM 발전도 그 궤도와 같이한다.
2. quality of scale
AI 에 의한 에너지 소비는 2026년까지 2022년 데이터센터의 전력 수요의 두 배를 사용할 것으로 예측된다. 마이크로소프트는 2030년까지 탄소중립을 목표로 하고 있다. 지속가능한 디자인과 에너지 효율, 탄소 발자국 추적은 이 과정에서 굉장히 중요한 역할을 한다. 
세 가지 혁명을 필요로 하는 지금 상황에서는, 지금 이 과정에 참여하는 모두가 탐구자이자 선구자가 될 수 있다.


### A Roadmap to Unleash the Power of GenAI and Build a Healthier Ecosystem(Kai Fu Lee)
PC era, Mobile era, AI era로 나는 3개의 IT 시대가 있다고 본다. 현재 우리는 새로운 단계에 도달해 있다. AI era는 다시 
1. productivity
2. search
3. Entertain
4. Social

로 나눠진다고 생각하고, 올해와 내년은 gpt의 productivity에서 search로 태동하는 단계이다. gpt search, Beago, perplexity와 같은 AI search engine들이 출시되고 있다.

[Beago](https://play.google.com/store/apps/details?id=com.beago.ai&hl=ko&pli=1)는 유저에게 선택권을 주기보다, 하나의 질문에 하나의 완벽한 답을 주도록 설계되었다. 앞으로 점점 더, AI는 더 이상 링크나 더 복잡한 개입 대신에, 완벽한 답을 줄 것이다.

현재 Gen AI는 아직 반도체>인프라>어플리케이션 순서로, 아직 어플리케이션이 반도체를 중심으로 더 많은 돈과 가치를 생산하고 있는 시장이 아니다. 이는 유지가능한 에코시스템이 아니다. 현재 성숙한 모바일 시장의 경우에는 반도체에서 더 높은 가치의 하드웨어로, 그리고 더 큰 시장의 어플리케이션 시장을 열었다. AI는 이런 점에서 아직 하드웨어 생태계 위에서 적절한 어플리케이션 환경이 갖추어지지 않았다. 아직 수 많은 AI영역의 앱들과 비즈니스들이 나와야만 한다.마치 아이폰처럼 인프라, 데이터베이스, 하드웨어, AI가 모두 합쳐져 완벽한 하나의 생태계를 이루게 되는 것이다.

AI는 모든 반복적이고 일상적인 업무에서 5년안에 해방시킬 것이고, 이 시간을 되돌아보게 될 것이다.

LLM -> Multimodal -> Agents -> Embodied(vitual world, interaction, phyiscal environment)의 5년간의 그림을 그리고 있다.
2026년에 도달하면 AI가 물리적으로 사용자와 상호작용하고 도움을 주는, 상품까지도 나올 것이라고 본다.


### AI Infra Market(Mark Adams) 
[Penquin solutions](https://www.penguinsolutions.com/)은 25년동안 고성능 컴퓨팅 분야에 종사한 회사입니다. 고성능 컴퓨팅 데이터센터 구현했던 기술들을 기반으로 현대 AI 데이터센터를 구현하고 있다. 

AI의 파도에 대해서 얘기해보자면,
1. 마이크로소프트, 메타와 같은 거대 기업들과 암호화폐나 금융권 기업들에 의해서 하이퍼스케일 AI 수요가 폭증했다.
2. 기업 AI fine tuning이 이루어지고, 비공개 모델이 만들어지고, 수익성이 재고되고 있다.
3. 이제 AI는 엣지에서, 보호되고 비공개적인 영역에서 작동할 것이라고 믿는다.
2023년에는 5%의 기업에서 AI를 사용했다. 그러나, 2026년까지는 80%에 사용될 예정이고, 현재 이를 위한 데이터센터, 인프라, GPU는 수요를 만족시키지 못하고 있다. 이러한 수요를 감당하기 위해서는 다음과 같은 혁신이 필요하다.

하드웨어적인 혁신이 첫 번째이다. GPU와 반도체를 괄시하던 거대 기업들은 순식간에 AI 액셀러레이터에 미친듯이 돈을 퍼붓고 있다. 그러나, 근본적으로 하이퍼스케일 데이터센터는 부지 확보, 전력, 냉각인프라, 보안 측면에서 많은 챌린지를 마주하고 있다. GPU안정성에서 70%만의 안정성이 있고, 나머지 인프라에서도 70%정도의 효율을 내고 있는 상황이다. 대부분의 기업들을 이러한 효율성을 높이고자 하고, 이 과정에서 펭귄 솔루션은 혁신을 만들어내고자 한다.


### Take Control of AI with Open Models and GPUs As-A-Service(Stephen Balaban)
[Lambda](https://lambdalabs.com/) 는 image recognition와 face recognition회사로 출발했고, AlexNet이 세상에 나오는 시점과 회사 창립 시점이 맞물려 거대한 GPU 클러스터를 만들 수 있었다. 이제 수십만 명의 유저가 람다를 통해서 GPU컴퓨팅을 한다. 현재는 회사의 목표는 AI 개발자를 위한 회사를 만드는 것이다.

 지금 AI는 우리가 어떻게 똑똑하게 사용하느냐가 아니라, 얼마나 많은 컴퓨팅 용량을 사용하냐에 달려있다. 지난 몇 년간, 수 많은 모델이 출시되고 있고 특히 더 짧은 시간동안 더 많은 모델들이 나오고 있다. 이제 모델을 잘 파인 튜닝하고, 사용하는 환경에 맞게 웨이트를 조정하는 것이 곧 그 회사의 미래를 결정하게 될 것이다.

- He who controls the weights controls the universe
- And Open models mean you control the models
- So you want to make your model smarter

#### training time vs testing time
시간을 더 많이 들일 수록 더 정확도가 높아지고, 또한 추론에 많은 시간을 투자할수록 더 높은 정확도를 기록한다. 이 때 training을 위해서 시간을 늘리는 것은 수억 달러를 수십억 달러로 높이지만, 대신에 우리는 정답을 위해서 0.1달러짜리 쿼리를 수 달러짜리 쿼리로 바꿔 사용할 수 았습니다. 즉, 우리는 추론 모델을 통해서 더 엄청만 모델이 아니더라도 좋은 답안을 만들어 낼 수 있는 것입니다.
- Reasoning makes smarter models affordable


### Building a More Curious and Efficient World with Perplexity`s AI-Powered Search(Arvaind Srinivas)
20년간 정체되어 있는 검색엔진 시장을 바꾸고자 하는 목표에서, 인터넷에 대한 접근성을 높이고자 2년 . 전이 프로젝트를 시작했다. 지난 10년간 검색 시장은 SEO, 광고 등의 복잡한 요소들이 결합되어 있는 검색 시장이었다. Peplexity는 개인화된 추천을 기반으로 검색하고 결과를 출력한다. Perplexity는 단순 정보 제공을 넘어서, 가장 유용하고 이해하기 쉬운 방식으로 제공하도록 설계됐다. 질문을 작은 부분으로 나누고, 각각의 부분의 답변을 찾아내고, 합쳐서 원래의 질문을 답변한다. 또한 가장 중요한 기능 중에 하나는, 검색의 출처를 밝히는 것이다. 이를 통해서 오답을 내는 경우에도 유저에게 가장 근접한 정보에 다가갈 수 있도록 유도한다. 이제는 더 나아가서 자신의 자료를 검색할 수 있도록 계속해서 발전시키고 있다. 금융리서치 분야에서 이러한 데이터 소스를 가지고 perplexity를 활용하는 경우가 발생하고 있다. 
- 최종적으로 perplexity는 웹을 통해 시러치하고, 자체 데이터를 리서치하고, 독점 데이터를 가져올 수 있는 리서치 플래폼을 목표로 한다.

#### perplexity는 곧 **광고** 키워드를 탑재한다. (충격적인 발표)
