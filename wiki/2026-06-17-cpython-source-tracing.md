---
date: 2026-06-17
tags: [python, cpython, internals, type-checking]
source: raw/python/2026-06-17-cpython-source-tracing.md
---

# Python 구현체와 CPython 소스 추적

## Python과 구현체의 관계

- Python은 언어 명세이고, CPython은 그 명세를 C로 구현한 기본 구현체다.
- 다른 구현체: PyPy(JIT, Python으로 구현), Jython(JVM), IronPython(.NET), MicroPython(임베디드)
- GIL은 언어 규칙이 아니라 CPython의 구현 디테일(레퍼런스 카운팅 때문에 생긴 제약)이다. CPython 3.13부터 실험적으로 GIL을 끌 수 있는 free-threading 빌드를 지원한다.
- 현재 쓰는 구현체 확인: `python3 -c "import platform; print(platform.python_implementation())"`

## 타입 체커와 스텁 (Pyright / Pylance / typeshed)

- **Pyright**: Microsoft가 만든 정적 타입 검사기(TypeScript로 작성). 코드를 실행하지 않고 타입 힌트만 분석한다.
- **Pylance**: VS Code용 Python 확장. 내부적으로 Pyright를 엔진으로 쓰고, 자동완성/네비게이션/리팩토링 등 IDE 기능을 더한다.
- **`.pyi`(타입 스텁)**: 실제 구현 없이 함수/클래스의 타입 시그니처만 담은 파일
- **typeshed**: 표준 라이브러리 및 유명 서드파티 패키지의 `.pyi` 스텁을 모아둔 공식 저장소(`python/typeshed`). 표준 라이브러리 중 C로 구현된 부분(빌트인 타입 등)은 파이썬 코드가 없어 타입 체커가 분석할 수 없는데, typeshed가 그 자리를 채워준다.
- 에디터에서 빌트인(`len`, `str.split` 등)에 "정의로 이동"을 누르면 실제 C 구현이 아니라 typeshed의 `.pyi` 스텁으로 이동한다 — "타입 체커가 참고하는 선언"으로 가는 것일 뿐, 진짜 로직이 있는 곳은 아니다.

## CPython 소스에서 빌트인 메서드의 진짜 구현 찾기

`str`, `list`, `dict` 등은 파이썬 코드가 아니라 CPython 인터프리터(C)에 들어있어, 에디터가 보여주는 typeshed 스텁만으로는 실제 구현을 볼 수 없다. CPython 저장소(`python/cpython`)로 직접 가야 한다.

### 추적 절차
1. CPython 저장소에서 메서드 이름으로 검색 (GitHub Code Search `repo:python/cpython unicode_split`, 안 되면 grep.app, 또는 경로 직접 탐색)
2. `Objects/clinic/unicodeobject.c.h`에서 **Argument Clinic**이 생성한 파싱 래퍼를 찾는다 — 이건 빌드 도구가 생성한 코드로, 인자를 파싱한 뒤 `*_impl(...)`을 호출하는 역할만 한다
3. `Objects/unicodeobject.c`에서 `*_impl` 함수 본문을 읽는다 — 여기서부터가 사람이 직접 쓴 진짜 로직
4. `_impl` 함수가 공통 헬퍼를 호출하는지 확인한다. 예: `str.split`은 `Objects/stringlib/split.h`의 `STRINGLIB(split)` 템플릿(매크로로 str/bytes/bytearray가 코드를 공유)을 호출

### Argument Clinic이란
CPython의 코드 생성기. 빌트인 함수의 인자 파싱(`PyObject*` → C 타입 변환) 보일러플레이트를 손으로 쓰지 않도록, `/*[clinic input]*/` 주석 블록에 시그니처를 선언하면 빌드 시 `*.c.h` 파일에 파싱 코드를 자동 생성한다. 생성된 코드는 끝에 `*_impl`을 호출한다.

### 실습 비교: `str.split` vs `str.replace`
- `str.split` → `unicode_split`(Clinic 래퍼) → `unicode_split_impl` → `Objects/stringlib/split.h`의 `STRINGLIB(split)` 템플릿
- `str.replace` → `unicode_replace`(Clinic 래퍼) → `unicode_replace_impl`(`unicodeobject.c:12582`) → `replace()`(`unicodeobject.c:10516`, **stringlib 미사용**, 직접 C로 구현)

**핵심 발견**: "공통 헬퍼(stringlib)로 이어진다"는 일반 규칙이 아니다. 알고리즘이 str/bytes/bytearray 간 그대로 공유 가능할 때만 stringlib 템플릿을 쓰고, `replace`처럼 더 복잡한 경우는 직접 구현한다. 추적할 때마다 실제 호출부를 따라가서 확인해야 한다.

### 검색 도구의 한계
- GitHub Code Search(웹 UI, `gh search code` CLI 모두)는 큰 파일(`unicodeobject.c`, 약 444KB)에서 결과를 놓칠 수 있다 — 로그인 여부와 무관하게 실제로 존재하는 `unicode_replace_impl`을 검색 결과에서 빠뜨리고 `.c.h`만 보여준 사례가 있었다
- 브라우저에서 큰 파일을 볼 때 Ctrl+F는 아직 렌더링되지 않은 부분을 놓칠 수 있다(GitHub가 큰 파일을 점진적으로 로드하기 때문) → "Raw" 보기로 전환하면 전체가 한 번에 로드되어 Ctrl+F가 제대로 동작한다
- 검색이 안 통할 때의 안정적인 백업 전략: 파일 경로를 직접 추측해서 들어가기 (`str` 관련 C 구현은 거의 다 `Objects/unicodeobject.c`에 있음)

## 참고 자료
- [CPython Devguide — Argument Clinic](https://devguide.python.org/development-tools/clinic/)
- [Argument Clinic How-To](https://docs.python.org/3/howto/clinic.html)
- [CPython Internals 샘플 챕터](https://static.realpython.com/cpython-internals-sample-chapters.pdf)
