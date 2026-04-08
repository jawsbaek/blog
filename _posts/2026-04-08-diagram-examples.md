---
title: "블로그 다이어그램 사용 가이드"
categories: [Blog]
tags: [diagram, mermaid, excalidraw]
mermaid: true
mermaid_look: handDrawn
description: "Mermaid.js와 Excalidraw를 활용한 다이어그램 작성 가이드"
---

이 포스트에서는 블로그에서 사용할 수 있는 다이어그램 작성 방법을 소개합니다.

## Mermaid.js 다이어그램

포스트 front matter에 `mermaid: true`를 추가하면 Mermaid 다이어그램을 사용할 수 있습니다.

### Flowchart

```mermaid
flowchart TD
    A[사용자 요청] --> B{인증 확인}
    B -->|성공| C[API 서버]
    B -->|실패| D[로그인 페이지]
    C --> E[데이터베이스]
    C --> F[캐시]
    E --> G[응답 반환]
    F --> G
```

### Sequence Diagram

```mermaid
sequenceDiagram
    participant U as 사용자
    participant F as Frontend
    participant A as API Server
    participant D as Database

    U->>F: 페이지 요청
    F->>A: API 호출
    A->>D: 쿼리 실행
    D-->>A: 결과 반환
    A-->>F: JSON 응답
    F-->>U: 화면 렌더링
```

### Hand-drawn 스타일

이 포스트는 front matter에 `mermaid_look: handDrawn`을 설정했기 때문에 모든 다이어그램이 손으로 그린 듯한 스타일로 렌더링됩니다.

클래식 스타일을 원하면 `mermaid_look: classic`으로 변경하거나 해당 설정을 제거하면 됩니다.

### 사용 가능한 테마

| front matter | 설명 |
|---|---|
| `mermaid_theme: default` | 기본 테마 |
| `mermaid_theme: dark` | 다크 테마 |
| `mermaid_theme: forest` | 녹색 계열 테마 |
| `mermaid_theme: neutral` | 흑백 중심 테마 |
| `mermaid_look: handDrawn` | Excalidraw 스타일 hand-drawn |

## Excalidraw SVG 임베딩

[Excalidraw](https://excalidraw.com/)에서 다이어그램을 그린 뒤 SVG로 내보내기 하고, `assets/diagrams/` 폴더에 저장합니다.

포스트에서 include로 삽입합니다:

```liquid
{% raw %}{% include diagram.html file="my-diagram.svg" caption="아키텍처 다이어그램" alt="시스템 아키텍처" %}{% endraw %}
```

### Excalidraw 사용 팁

1. [excalidraw.com](https://excalidraw.com/)에서 다이어그램을 그립니다
2. 메뉴 → Export → SVG 형식으로 내보냅니다
3. "Background" 체크를 해제하면 투명 배경으로 내보낼 수 있습니다
4. 파일을 `assets/diagrams/` 폴더에 저장합니다
5. 포스트에서 `{% raw %}{% include diagram.html %}{% endraw %}`로 삽입합니다
