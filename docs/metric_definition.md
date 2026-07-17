# 평가지표 정의서

## 1. 지표 체계

| ID | 범주 | 지표 | 단계 |
|---|---|---|---|
| M-01 | 구간 검색 | temporal IoU | 참조 구현 |
| M-02 | 구간 검색 | MR-mAP@0.5:0.95 | 참조 구현 |
| M-03 | 구간 검색 | R@1@IoU 0.5/0.7 | 참조 구현 |
| H-01 | 하이라이트 | HL-mAP | 참조 구현 |
| H-02 | 하이라이트 | HL-Hit@1 | 참조 구현 |
| E-01 | element | Element Precision/Recall/F1 | 산식 정의 |
| R-01 | 관계 | Relation Precision/Recall/F1 | 산식 정의 |
| R-02 | 관계 | Relation Integrity | 참조 구현 |
| A-01 | 재조립 | Requested Element Coverage | 산식 정의 |
| A-02 | 재조립 | Chronology Violation Rate | 산식 정의 |
| C-01 | 일관성 | Repeated Output Agreement | 연말 측정 |
| C-02 | 재현성 | Cross-environment Deviation | 연말 측정 |
| P-01 | 성능 | Stage Latency | 연말 측정 |
| P-02 | 성능 | Throughput | 연말 측정 |
| I-01 | 연동 | Interface Conformance | 연말 측정 |

## 2. 핵심 산식

### 2.1 temporal IoU

```text
tIoU = length(Predicted ∩ Reference) / length(Predicted ∪ Reference)
```

### 2.2 MR-mAP

각 query의 예측 구간을 신뢰도 순으로 정렬하고 tIoU 임계값별 Average Precision을 계산한다. tIoU 0.50~0.95, 0.05 간격의 결과를 평균한다.

### 2.3 R@1

가장 높은 점수의 예측 구간이 하나 이상의 정답 구간과 지정 tIoU 이상으로 겹치면 적중으로 본다.

### 2.4 HL-mAP / Hit@1

각 2초 클립의 중요도 예측을 정답 점수와 비교한다. 정답 2, 3, 4 이상을 각각 Fair, Good, VeryGood positive로 정의한다. Hit@1은 가장 높은 예측 점수의 클립이 positive인 질의의 비율이다.

### 2.5 Element F1

```text
Precision = 정답 element와 일치한 예측 element / 전체 예측 element
Recall    = 정답 element와 일치한 예측 element / 전체 정답 element
F1        = 2 * Precision * Recall / (Precision + Recall)
```

element 일치는 `type`, 표준화된 `label`, 미디어 시간 구간의 tIoU를 조합하여 판정한다. 표준화 규칙은 연말 annotation guideline에서 확정한다.

### 2.6 Relation F1

subject·predicate·object 삼중항이 정답과 동일할 때 true positive로 계산한다. subject와 object의 element 동일성 판정은 Element matching 규칙을 따른다.

### 2.7 Relation Integrity

```text
Relation Integrity = 유효 node와 허용 predicate를 모두 사용한 relation / 전체 relation
```

## 3. 측정 조건

- 동일 dataset split, query, video, clip length를 사용한다.
- 검증시스템과 ETRI 대상 시스템에 동일한 정규화 규칙을 적용한다.
- 실행 전 시스템, 모델, 코드, 설정 버전을 고정한다.
- 성능 측정 시 warm-up 횟수, 반복 횟수, 하드웨어를 기록한다.
- 정량 판정 기준값은 ETRI와 합의 전에 임의로 확정하지 않는다.

## 4. 결과 표시 규칙

| 상태 | 의미 |
|---|---|
| DESIGN_DEFINED | 산식·입력·출력 정의 |
| PRELIMINARY_MOCK | 합성 데이터·Mock 출력 결과 |
| MODEL_PREDICTION | 실제 모델 추론 결과 |
| ETRI_SYSTEM_OUTPUT | ETRI 대상 시스템 실제 출력 |
| JOINT_VERIFIED | 상호 입회 확인된 결과 |

