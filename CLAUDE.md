# CLAUDE.md

이 파일은 이 저장소에서 작업할 때 Claude Code(claude.ai/code)에게 제공되는 안내 문서입니다.

## 프로젝트 개요

`llm-wiki`는 AI 및 LLM 학습을 위한 개인 위키/지식 베이스입니다.

- `raw/` — 위키 작성을 위해 수집한 원본 자료(노트, 아티클, 참고 자료 등)
- `wiki/` — `raw/`의 내용을 바탕으로 정리/작성한 위키 콘텐츠

## 작업 방식

Claude는 `raw/`에 있는 자료를 읽고, 그 내용을 정리하여 `wiki/`에 작성합니다.

`teach` 스킬을 통해 학습한 내용이 있다면 `learning-records/`에 기록이 남습니다. wiki를 작성하거나 갱신할 때 `learning-records/`를 함께 참고하여, 사용자가 이미 이해한 내용과 어려워했던 부분을 반영합니다.

## 규칙

- `raw/`는 원본 자료 보관용이므로 수정, 삭제, 이동 등 어떠한 변경도 하지 않습니다. 읽기만 합니다.

## wiki 작성 포맷

`wiki/` 아래의 파일은 다음 규칙을 따릅니다.

- 파일명: `wiki/학습일-학습내용.md` (예: `wiki/2026-06-15-micrograd-engine.md`)
- 파일 상단에 frontmatter로 메타데이터를 기록합니다:

```yaml
---
date: YYYY-MM-DD
tags: [관련 태그들]
source: raw/ 안의 원본 자료 경로
---
```
