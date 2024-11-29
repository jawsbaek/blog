---
title: "How to make a good and easy architecture: caringnote"
categories: development 
tags: 
    - kubernetes 
    - git-action
    - ci/cd
    - infrastructure
    - nginx
---
어떻게 하면 확장성이 있고 좋은 아키텍처를 만들 수 있을까 하는 고민은 언제 어디서나 하는 일이다. 특히, 매일 작업하는 프로젝트가 아닐 수록 유지보수가 편하고 업데이트가 쉬운 구조를 만드는 것은 더욱 중요하다. 케어링노트 프로젝트를 진행하면서 이러한 고민을 어떻게 아키텍처에 반영하여 중장기적으로 개발될 수 있는 프로젝트가 되도록 했는지 설명하려 한다.

케어링노트 프로젝트는 회사 지원 프로젝트가 아닌 비영리 기구 지원 프로젝트이기 때문에, 환경 상의 제약을 가지고 있었다. 주어진 자원과 환경은 다음과 같다.
1. 카카오클라우드 VM
2. 소량의 기술 지원금

로드밸런서나 다른 클라우드 자원이 없는 상황에서, VM 하나에만 환경을 구축할 경우 scailing이나 확장성은 물론 유지보수에서도 문제가 생긴다. 따라서, 실제 운영환경은 다른 클라우드의 클라우드 자원으로의 이전을 고려하고 빠르게 이전할 수 있는 아키텍처를 설계했다.
 <img src="../../assets/images/2024-11-29-caringnote-architecture/caringnote-architecture.png" width="100%" height="50%">
1. 가장 큰 VM 사용
2. Kubeadm으로 kube cluster 형성
3. Github에서는 Action을 통해 build 후 docker hub에 push
4. Kubernetes cluster에서는 해당 image pull 후 rolling update

이를 통해 코드, 이미지, cluster 배포 간에 독립성을 유지하면서도 지속적으로 배포가 가능한 구조를 만들었다.

## 왜 kubernetes 배포를 선택했는가?
Kubernetes는 초기 환경 구성이 굉장히 복잡하고, contianer와 networking등 다양한 인프라 지식을 가지고 있어야 시도가 가능한 플랫폼이다. 특히 바로바로 띄워 상태를 확인해볼 수 있는 docker와 다르게, kubernetes cluster 구성부터 꽤 많은 시간을 소모하게 됩니다. 그러나 다음과 같은 이점을 위해서 Kubernetes를 사용했다.
1. Portability
    * Kubernetes에서 사용한 deploy는 환경에 상관 없이 구축이 가능하다. AWS나 Azure를 사용할 수 있고, Onpremise 기반 서버에도 동작하도록 만들 수 있다. 이 프로젝트가 개발이 끝난 뒤에 어디서 운영하게 될지 모르는 불확실성이 있기 때문에, 새롭게 구축을 만드는 것보다 kubernetes cluster로 하는 것이 낫다고 판단했다.
2. Helm Chart
    * Helm Chart에는 Kubernetes 애플리케이션을 배포하는 데 필요한 모든 리소스를 하나의 번들로 묶어 제공한다. 저희 아키텍처에서는 PosrtgreSql과 Keycloak이 필요했는데, 이를 위한 환경구성을 따로 하지 않고 Helm Chart로 바로 설치하고 다른 애플리케이션들과 연동할 수 있다.
3. Automaion
    * 각 애플리케이션이나 deployment과정에서의 오류를 자동화하고, 이 처리를 도와줌으로써 구축 후에 사람의 개입을 최소화할 수 있다.

## Kubernetes 아키텍처
케어링노트는 내담자, 상담자, 보조자, 관리자 등의 4계층 유저 구조를 가지고 있다. 유저 별로 볼 수 있는 인터페이스가 다르고, 관리되는 방식이 다르기 때문에 유저 등록과 로그인, 개인정보 관리 등의 작업들이 필요하다. 이러한 유저 관리와 로그인을 위해서는 Keycloak을 사용하기로 했다. Keycloak을 사용할 경우, SSO 지원도 가능하고, MFA나 이메일 인증 등 다양한 로그인 관련 기능들을 직접 개발하지 않아도 된다는 장점이 있어 채택했다. DB는 PostgreSql을 pod으로 띄워 사용하기로 결정했다. 
보안적으로 TLS 통신도 필요하기 때문에, nginx-ingress reverse proxy와 letsencrypt-cluster-issuer로 네트워크 트래픽 처리와 인증서 처리를 사용하였다.
Oauth2-proxy로 인증된 사용자만 내부 트래픽이 가능하도록 할 수도 있으나, 현재는 서비스가 API 서버 하나이기 때문에 사용하지 않았다.

결과적으로 사용한 서비스들은 다음과 같다.
* bitnami/postrgesql
* bitnami/keycloak
* ingress-nginx
* letsencrypt-cluster-issuer
* api-pod
* web-pod

현재 만든 pod 외에 가져온 프로그램들은 전부 helm chart기반으로 배포하였고, values 파일과 커맨드를 repo에 관리하고 있다.
api-pod과 web-pod은 단순 deployment로 저장한 뒤에, 후에 다시 고가용성 등을 고려하여 chart로 만들 예정이다. 자세한 세팅은 [caring-note-deployment](https://github.com/MediBird/caring-note-deployment) repo에서 확인할 수 있다.

## CI/CD
환경 구성에서 가장 고민이 되는 것은 CI/CD를 만드는 일이다. 환경이 더 복잡해지는 것을 막으면서, migration이 쉬운 CI/CD 시스템을 만들어야 했다. 이에 더해서, 코드가 변경 될 시에 바로 서버의 pod이 재배포되도록 해야 했다. argoCD와 git-action의 장단점을 비교 후에 이 프로젝트에서는 git-action을 사용했다.
관리 포인트를 최대한 줄이고 poc 수준의 배포 환경이기 때문에, secret+git-action으로 배포를 처리했다.

1. argoCD
   * argoCD는 가장 쉽게 시도해볼 수 있는 CI/CD 툴이다. 새롭게 배포가 필요하면 deployment 파일을 바꿔 푸쉬되면 이에 sync를 맞추어 배포를 새롭게 진행하도록 도와준다. 그러나, 현재 프로젝트에서는 kubernetes 환경을 다루거나 변수를 다뤄보지 않은 개발자가 있기 때문에 러닝커브가 존재하는 상황이었다. 또한, argoCD 역시 kubernetes에 배포가 되어있어야 해서, 추가적인 프로그램을 아키텍처에 추가하는 것도 부담이 있었다.
2. git-action
   * git-action기반 빌드는 널리 알려져 있는 방식이고, 쉽게 가능해 큰 문제가 아니다. 진짜 문제는 배포인데, git-action으로 배포하려면 ssh로 해당 인스턴스에 접속 후에 커맨드를 날리는 방식이다. 고전적이고 단순한 방식이지만, 자동 배포가 가능하고 빌드부터 배포까지 로그를 깃헙에서 볼 수 있다는 장점이 있다.


앞으로 변경점들이 있겠지만, 현재까지의 여정을 1차로 정리해보았다. 중요한 것은, 현재 팀원들이 이해할 수 있고, 협업과정에서 장점을 느낄 수 있도록 시스템을 구축하고 그들의 동의를 구하는 것이라고 생각한다. 이는 좋은 시스템 구축뿐만 아니라 팀원들이 이해할 수 있도록 노력하는 것들도 포함된다. 그런 점에서는 이 글 또한 caringnote-architecture 구현의 일부라고 생각한다.
