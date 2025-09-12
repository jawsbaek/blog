# AI야, 돈 다 줄테니 제대로 만들어줘: BMAD-METHOD

## **💻 Developer James - Story 1.5 Implementation**

Greetings! I'm James, your Full Stack Developer. I've loaded the story and development standards. I can see Story 1.5 is approved and ready for implementation.

### **Available Commands:**

1. **develop-story** - Implement the story tasks sequentially
2. **explain** - Detailed explanation of implementation decisions
3. **review-qa** - Apply QA fixes from quality gate results
4. **run-tests** - Execute linting and tests
5. **exit** - Exit developer mode

I can see Story 1.5: "JSON Import/Export with Dry‑Run" is approved and contains comprehensive technical context. The story has 5 main tasks with detailed subtasks covering import/export endpoints with transaction handling, auth, and audit logging.

**Current project structure check:** Let me verify the existing codebase structure before beginning implementation.

Bob이 스토리를 작성하고, Quinn이 검증하며, Sarah가 approve합니다. James가 저에게 인사하고, 개발을 시작합니다.  Agentic agile 개발 방법론에 기반을 둔, 혁신적 애자일 AI 주도 개발(Breakthrough Method of Agile AI-Driven Development)방법론이자 프레임워크를 이 글에서 소개시켜드리고자 합니다.

여러분들은 LLM이 혹은 AI가 코드를, 테스트를, 기능을 제대로 만들어주었나요? 바이브 코딩이라고 해서 막 해보면 뭔가 되는 것 같은데 막상 코드는 지저분한 상황, 다들 겪으셨을 거라고 생각합니다. 특히 최근에, 디자이너 분이 바이브 코딩으로 웹사이트를 만드시는 걸 보면서, 저라면 사용하지 않았을 코드들이 마구 들어가는 것을 보았습니다. 그냥 LLM과 커서 혹은 클로드 코드만으로는 문제가 해결되지 않는 다는 것은 당연했습니다. 저는 커서 룰을 세팅해서 사용했지만 이것도 완벽한 해결책은 아니었습니다.

# AI 개발의 가장 큰 문제점 : 개인기 의존

AI 개발을 할 때 가장 큰 문제는, 사람이 개발할 때의 프로세스를 지키지 않는다는 점입니다.

우리가 개발을 한다면,

1. 명세를 읽고 기능 파악
2. 기존 코드 분석
3. 좋은 예시, 혹은 공식 문서 참고
4. 코드 작성
5. 테스트 작성
6. 코드 리뷰

를 거칠 것입니다.(예시이므로 몇 가지 단계가 생략된 부분은 이해 부탁드립니다.) 그러나, LLM을 사용할 때 우리는 의례 “인증 기능 만들어줘”, “netlify 배포 설정해줘”와 같이 단순하게 명령을 내리게 됩니다. 이는 두 가지 문제를 일으키는데요, 

1. 잘못된 코드 생성
2. AI 자율성에 따른 비용 발생

이런 문제들을 해결하고자 커서 룰, 에이전트 세팅 등 다양한 방식의 LLM 효율 및 정확성 상승 방법이 제시되고 있었습니다.

# AI agent Agile team: AI 개발의 정규화

BMAD-Method는 인간 팀이 애자일 개발하는 프로세스를 LLM이 그대로 따라하도록 만들었습니다.

총 8개의 agent(pm, po, sm, dev, architect, bmad-master, bmad-orchestrator, qa, ux-expert, analyst)를 구성해 개발을 진행하고, 각각의 역할에서 필요한 기능과 제약조건들을 걸어두었습니다. 이를 통해, 개발 혹은 문서의 퀄리티를 보장하고 누구나 작은 아이디어도 엔터프라이즈 급의 확장 가능성으로 고려할 수 있습니다.

# BMAD METHOD- 핵심 알아보기

## 프로젝트 시작 단계

## Analyst/Mary: 아이디어 분석 및 프로젝트 개요 작성

개발을 시작하기 전에, BMad는 정규화된 계획 단계를 거칩니다. 먼저 Analyst Mary가 이 업무를 담당합니다. 유저와 함께 brainstorming을 진행하고, 시장을 분석하고, 경쟁자 분석을 진행합니다. 분석이 모두 끝난 뒤에는 프로젝트 개요로 지금까지의 모든 분석을 종합하여 작성합니다.

### Mary의 강점 : 본질 파악

Mary agent의 프롬프트에는 왜라는 질문을 던져 유저의 의도를 파악하고, 사실 기반 중심의 분석을 진행해 마구잡이로 상상이 진행되는 것을 방지합니다. 따라서, 저 같은 개발자가 그냥 좋은데? 하고 만드는 것을 방지하는 것인데요. 그러면서도 여러 아이디어와 분석을 진행해 아이디어가 적절하게 다듬어질 수 있도록 합니다.

## PM/John: PRD 작성

프로젝트 개요가 작성되면, John은 이 문서를 기반으로 PRD를 작성하기 시작합니다. 이 때, 기능적 요구사항(FR) 뿐만 아니라, 비기능적 요구사항(NFR)과 에픽, 스토리까지 존이 개략적으로 작성해둡니다.

## UX-expert/Sally: 프론트엔드 요구사항 작성

Sally는 PRD를 바탕으로 프론트엔드 스펙을 정의하고, V0와 같은 UI AI 서비스에 디자인을 맡기기 위한 프롬프트 작성을 진행합니다.

## Architect/Winston: 아키텍처, UX스펙 작성

이제 이 모든 매니저들이 작성한 문서들을 모아 플랫폼, 기술 스택, 아키텍처를 결정하는 작업을 아키텍트가 진행합니다. 아키텍트는 유저 경험을 고려하고, 조금 안전하고 지루한 기술을 선택합니다. 데이터 기반으로 디자인을 결정하는 확고한 아키텍트입니다.

이제 모든 문서들이 작성되었다면, 개발할 준비가 되었습니다. 지금까지의 과정은 IDE가 아닌 GPT나 Gemini같은 곳에서 해도 되지만, 이제 개발은 IDE로 넘어가서 해야합니다.

# 개발 사이클

## Scrum Master/Bob: 지난 스토리 리뷰 및 다음 스토리 구체화

밥은 지난 스토리들에 적힌 개발자들과 QA노트를 바탕으로, 현재 스토리의 진행 방식을 구체화 하고 개발 진행에서 발생가능한 리스크들을 적습니다. 개발자와 QA에게 넘기는 체크리스트입니다.

## Project Owner/Sarah: 스토리 초안 검증

사라는 문서에 빠진 부분은 없는지, 스토리가 개발자가 진행하기 용이한 상태인지 검증합니다. 몇 가지 요소를 보충한 뒤에, 스토리를 Approved상태로 치환하고 Sarah가 사인하면, 이제 개발에 들어갈 수 있습니다.

## Developer/James: 개발

이제 이 모든 준비가 제임스에게 주어졌습니다. 제임스는 개발을 해서 태스크를 소화할 뿐만 아니라, 주어진 테스트들도 만족해야 하고 Acceptance criteria또한 Qa를 통과할 수 있게 해야 합니다. 저의 많은 토큰과 비용을 소진한 뒤에 자신의 태스크를 완료 처리합니다. ㅠㅠ

![image.png](image.png)

## QA/Quinn: 모든 과정을 리뷰하고 감독하는 프로세스의 퀸

퀸은 사실 문서 작성과정부터 코멘트를 남겨오는 역할이 있지만, 역시 개발 과정에서 핵심적인 역할을 합니다. AI agent들의 작업물을 계속 리뷰하고, 평가하고 , 평가 문서를 작성해 남깁니다. 유저 설정에 따라서 퀸이 소모하는 시간이 가장 많을 수도 , 가장 적을 수도 있는 역할입니다. 실제 Agile 팀에서 가장 중요한 역할이 QA이듯이, Bmad에서도 가장 많은 기능과 역할, 설명을 Quinn에게 할당해두었습니다.

가장 까다로운 에이전트인 Quinn을 통과하면, 마침내 스토리를 끝내고 이제 다음 스토리로 넘어가게 됩니다.

# 장점: 문서화, 퀄리티 보장

개발에 사용되는 문서, 개발 이후 문서 등 AI사용 과정들이 모두 문서의 형태로 결과가 남기 때문에, 여러 사람이 바이브 코딩하더라도 같은 퀄리티의 결과물을 보장하게 됩니다. 특히, 개발 과정에서 테스트 시나리오에 많은 투자를 해서 어긋나는 부분이 없도록 하는 것이 이 방법론의 가장 큰 장점이라고 생각합니다.

# 단점: 엄청난 비용 발생

저는 고작 2일동안 커서 기본 사용량을 모두 소진하고 60달러를 더 사용했습니다. 많은 문서와 테스트 작성은 그만큼 많은 토큰 사용을 일으켰기 때문입니다. 단순한 poc나 가벼운 개발에 사용하기에는 적절치 않은 프레임워크라는 생각이 들었습니다.

# 우리가 Bmad method를 눈여겨 봐야 하는 이유

우리 회사는 이미 수 많은 프로세스가 개발의 퀄리티를 보장하기 위해 존재합니다. 그러나 AI 사용에 있어서는 아직 제대로 된 방법론이 갖춰지지 않았다고 생각합니다. 회사에서 개발하는 방법론을 이런 프레임워크와 조합해서, SDS agent들을 규정하거나 문서의 형태가 SDS에 딱 맞게 생산되도록 하면 좋을 것 같다는 생각이 들었습니다. 특히 PRD중심의 개발은 조금 비용이 많이 들더라도 기업 환경에 더 잘 맞는 개발방식이라는 생각이 들었습니다.

###
