---
date: 2026-06-16
tags: [pytorch, rnn, nlp, classification, one-hot-encoding]
source: raw/torch-basic-nlp/chapter1.ipynb
---

# PyTorch로 구현하는 CharRNN: 이름으로 국적 분류

## 문제 정의

이름(문자열) → 국적(18개 클래스) 분류 문제
- 데이터: 20,074개 이름, 18개 언어 (Czech, Arabic, Chinese, ...)
- 입력: 문자 시퀀스 / 출력: 국적 레이블

## 데이터 전처리

### 문자 인코딩

유니코드 이름을 ASCII로 정규화한 뒤 one-hot 벡터로 변환

```python
allowed_chars = string.ascii_letters + " .,;'" + "_"  # 58개 문자
n_letters = len(allowed_chars)  # 58

def lineToTensor(line):
    tensor = torch.zeros(len(line), 1, n_letters)  # (seq_len, 1, 58)
    for li, letter in enumerate(line):
        tensor[li][0][letterToIndex(letter)] = 1
    return tensor
```

`lineToTensor('Jones')` → shape `[5, 1, 58]`: 5글자 × 1배치 × 58차원 one-hot

### Dataset 클래스

```python
class NamesDataset(Dataset):
    # txt 파일명이 레이블 (e.g. Czech.txt → label='Czech')
    # 각 이름을 one-hot 텐서로 변환해 저장
    def __getitem__(self, idx):
        return label_tensor, data_tensor, data_label, data_item
```

Train/Test 분할: 85% / 15% (random_split, seed=2026)
- train: 17,063개 / test: 3,011개

## 모델 구조: CharRNN

```python
class CharRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        self.rnn = nn.RNN(input_size, hidden_size)   # 시퀀스 처리
        self.h2o = nn.Linear(hidden_size, output_size) # 최종 분류
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, line_tensor):
        rnn_out, hidden = self.rnn(line_tensor)
        output = self.h2o(hidden[0])  # 마지막 hidden state만 사용
        return self.softmax(output)
```

하이퍼파라미터: `input_size=58`, `hidden_size=128`, `output_size=18`

## 핵심 포인트

- RNN은 시퀀스를 순서대로 처리하고, **마지막 hidden state**가 전체 시퀀스의 요약
- one-hot 인코딩은 단순하지만 어휘 크기가 작은 문자 수준 모델에서 효과적
- `nn.RNN`은 `(seq_len, batch, input_size)` 형태의 입력을 받음

## RNN의 구조적 한계 (이론과 연결)

이 모델은 하나의 hidden state에 전체 이름의 맥락을 압축한다. 이름처럼 짧은 시퀀스에서는 잘 동작하지만, 긴 텍스트에서는 앞부분 정보가 희석되는 문제가 생긴다 → Transformer가 이 한계를 해결
