# CLAUDE.md

이 파일은 이 저장소에서 작업할 때 Claude Code(claude.ai/code)에게 제공되는 안내 문서입니다.

## 프로젝트 개요

`llm-wiki`는 AI 및 LLM 학습을 위한 개인 위키/지식 베이스입니다.

- `raw/` — 위키 작성을 위해 수집한 원본 자료(노트, 아티클, 참고 자료 등)
- `wiki/` — `raw/`의 내용을 바탕으로 정리/작성한 위키 콘텐츠

## 작업 방식

Claude는 `raw/`에 있는 자료를 읽고, 그 내용을 정리하여 `wiki/`에 작성합니다.

## 규칙

- `raw/`는 원본 자료 보관용이므로 수정, 삭제, 이동 등 어떠한 변경도 하지 않습니다. 읽기만 합니다.

## wiki 작성 포맷

`wiki/` 아래의 파일은 markdown(`.md`)이 아닌 HTML(`.html`)로 작성합니다. 보기 좋게 렌더링되는 것이 목적이므로, 가독성 있는 스타일이 적용된 상태로 작성합니다. 다음 규칙을 따릅니다.

- `wiki/style.css`(공유 스타일시트)를 모든 페이지의 `<head>`에 `<link rel="stylesheet" href="style.css">`로 연결합니다. 디자인을 바꿀 때는 `style.css` 한 곳만 수정하면 모든 페이지에 반영됩니다.
- markdown으로는 표현할 수 없는 인터랙션/시각화 요소를 적극적으로 활용합니다. HTML로 바꾼 핵심 이유이므로, "글로만 설명하면 markdown과 다를 게 없다"는 기준으로 판단합니다.
  - 파일 상단(메타데이터 블록 아래)에 각 `<h2>`(필요하면 주요 `<h3>`까지) 섹션으로 이동하는 목차(`<nav class="toc">`)를 둡니다. 각 헤딩에는 `id`를 붙이고 목차에서 앵커 링크로 연결합니다.
  - 보충 설명, 참고 자료 목록, 긴 코드/로그처럼 본문 흐름을 방해하는 내용은 `<details><summary>...</summary>...</details>`로 접어둡니다.
  - 계산 그래프, 아키텍처, 파이프라인, 워크플로, 시퀀스(턴 단위 상호작용) 등 구조를 설명하는 내용은 텍스트나 ASCII 다이어그램 대신 [Mermaid](https://mermaid.js.org/)로 실제 렌더링되는 도식을 그립니다. `<head>`에 `<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>`를 추가하고, `</body>` 직전에 `<script>mermaid.initialize({ startOnLoad: true });</script>`를 둔 뒤 `<div class="mermaid">...</div>` 블록 안에 다이어그램 코드를 작성합니다.

- 같은 날짜에 작성하는 모든 학습 내용은 하나의 파일로 묶습니다. 파일명: `wiki/YYYY-MM-DD.html` (예: `wiki/2026-06-15.html`)
- 같은 날짜에 여러 주제를 다룰 경우, 각 주제는 파일 안에서 `<h2>` 레벨 섹션으로 구분합니다(하위 제목은 그에 맞춰 한 단계씩 내려서 작성: `<h3>`, `<h4>` ...).
- `<body>` 최상단에 메타데이터 정보 블록을 둡니다. `tags`는 그날 다룬 모든 주제의 태그를 합쳐 중복 없이 기록하고, `source`는 그날 참고한 모든 원본 자료 경로를 리스트로 기록합니다:

```html
<div class="meta">
  <p>date: YYYY-MM-DD</p>
  <p>tags: 태그1, 태그2</p>
  <ul class="source">
    <li>raw/ 안의 원본 자료 경로1</li>
    <li>raw/ 안의 원본 자료 경로2</li>
  </ul>
</div>
```

## GitHub Pages 배포

이 저장소는 GitHub Pages로 배포됩니다(소스: `main` 브랜치 `/`(root)). 새 날짜 파일을 `wiki/`에 추가하면, 저장소 루트의 `index.html`(전체 항목을 모아 보는 랜딩 페이지)에도 그 날짜와 다룬 주제 목록을 최신순(맨 위)으로 추가합니다.
