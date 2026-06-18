---
date: 2026-06-15
tags: [micrograd, autograd, backpropagation, derivative, chain-rule]
source: raw/micrograd/engine.ipynb
---

# Micrograd: 미분과 역전파의 기초

## 1. 미분(derivative)의 직관

함수 `f(x) = 3x^2 - 4x + 5`에 대해, 미분의 정의(극한)를 그대로 코드로 구현해보면:

```python
h = 0.000000000001
x = 3.0
(f(x + h) - f(x)) / h  # ≈ 14.0
```

`x`를 아주 조금(`h`) 늘렸을 때 `f(x)`가 얼마나 변하는지의 비율 = 그 지점에서의 기울기(미분값).
이게 신경망 학습에서 "이 변수를 살짝 바꾸면 결과(loss)가 얼마나 바뀌는가"를 구하는 핵심 아이디어다.

## 2. 계산 그래프를 만드는 `Value` 클래스

스칼라 값 하나하나를 감싸서, 연산을 할 때마다 "어떤 값들로부터 만들어졌는지(`_prev`)"와 "어떤 연산인지(`_op`)"를 기록한다.

```python
class Value:
    def __init__(self, data, _children=(), _op='', label=''):
        self.data = data
        self.grad = 0.0
        self._prev = set(_children)
        self._op = _op
        self.label = label

    def __add__(self, other):
        return Value(self.data + other.data, (self, other), '+')

    def __mul__(self, other):
        return Value(self.data * other.data, (self, other), '*')
```

- `data`: 실제 값
- `grad`: 이 값이 최종 출력(L)에 미치는 영향(기울기). 처음엔 0으로 초기화
- `_prev`: 이 값을 만들어낸 입력값들 (연산 그래프의 부모 노드들)
- `_op`: 어떤 연산으로 만들어졌는지 (`+`, `*` 등)

예시 그래프:

```
a = 2.0, b = -3.0, c = 10.0, f = -2.0
e = a * b      # -6.0
d = e + c      # 4.0
L = d * f      # -8.0
```

## 3. 그래프 시각화 (`graphviz`)

`trace()`로 그래프의 모든 노드/엣지를 모으고, `draw_dot()`으로 각 노드를 `{ label | data | grad }` 형태로 그려서 계산 흐름을 한눈에 볼 수 있다.

## 4. 수동 역전파 (manual backpropagation)

`L = d * f` 라는 최종 출력에서 시작해서, **체인룰(chain rule)** 을 이용해 각 변수가 `L`에 얼마나 영향을 주는지(`grad`)를 거꾸로 계산한다.

```python
L.grad = 1.0   # dL/dL = 1 (자기 자신에 대한 미분은 항상 1)
f.grad = 4.0   # L = d * f → dL/df = d = 4.0
d.grad = -2.0  # L = d * f → dL/dd = f = -2.0
c.grad = -2.0  # dL/dc = (dL/dd) * (dd/dc) = -2.0 * 1 = -2.0
e.grad = -2.0  # dL/de = (dL/dd) * (dd/de) = -2.0 * 1 = -2.0
```

핵심 규칙:
- **곱(`*`)**: `z = x * y` 이면 `dz/dx = y`, `dz/dy = x` → 즉, "내 grad = 상위 grad × 상대방의 data"
- **합(`+`)**: `z = x + y` 이면 `dz/dx = dz/dy = 1` → 합 연산은 grad를 그대로 흘려보낸다 (분배)

## 5. 수치 미분으로 검증

위에서 손으로 계산한 `dL/dc = -2.0`이 맞는지, `c`를 `h`만큼 늘려서 `L`이 얼마나 변하는지로 다시 확인:

```python
h = 0.0001
# c = 10.0 일 때 L = L1
# c = 10.0 + h 일 때 L = L2
(L2 - L1) / h  # ≈ -1.9999999999953388 ≈ -2.0
```

손으로 구한 체인룰 결과(`-2.0`)와 수치 미분 결과(`≈ -2.0`)가 거의 일치 → 역전파 계산이 맞다는 검증 방법.

## 요약

- 미분 = "입력을 살짝 바꿨을 때 출력이 얼마나 변하는가"의 비율
- `Value` 클래스는 연산 과정을 그래프로 기록해서 나중에 거꾸로(`grad`) 계산할 수 있게 해준다
- 역전파는 출력에서 입력 방향으로 체인룰을 반복 적용하는 것
- `+`는 grad를 그대로 분배, `*`는 grad에 상대방 값을 곱해서 전달
- 수치 미분(`(f(x+h)-f(x))/h`)으로 역전파 결과를 검증할 수 있다
