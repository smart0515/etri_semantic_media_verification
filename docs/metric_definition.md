# 평가지표 정의서

## 1. 지표 체계

| ID | 범주 | 지표 | 평가 대상 |
|---|---|---|---|
| MR-01 | 구간 검색 | temporal IoU | 예측·정답 구간 중첩 |
| MR-02 | 구간 검색 | MR-mAP@0.50:0.95 | query별 ranked windows |
| MR-03 | 구간 검색 | R@1@0.50, R@1@0.70 | 최상위 구간 적중 |
| HL-01 | 하이라이트 | HL-mAP | 2초 clip 중요도 순위 |
| HL-02 | 하이라이트 | HL-Hit@1 | 최상위 clip 적중 |
| EL-01 | element | Precision, Recall, F1 | type·label·구간 일치 |
| RL-01 | relation | Triple F1 | subject·predicate·object |
| RL-02 | relation | Relation Integrity | node·predicate 참조 무결성 |
| RA-01 | 재조립 | Coverage | 요구 단위 포함률 |
| RA-02 | 재조립 | Chronology Violation | 시간 순서 위반률 |
| CS-01 | 일관성 | Repeated Output Agreement | 동일 입력 반복 결과 |
| PF-01 | 성능 | Stage Latency | 단계별 처리시간 |
| PF-02 | 성능 | Throughput | 단위 시간 처리량 |
| IF-01 | 연동 | Interface Conformance | 입출력 계약 준수율 |

## 2. 구간 지표

두 구간 `A=[a1,a2]`, `B=[b1,b2]`의 temporal IoU는 다음과 같다.

```text
intersection = max(0, min(a2,b2) - max(a1,b1))
union        = max(a2,b2) - min(a1,b1)
tIoU         = intersection / union
```

MR-mAP는 tIoU 0.50부터 0.95까지 0.05 간격 임계값에서 Average Precision을 계산한 뒤 평균한다. R@1은 query별 최고 점수 구간이 대표 임계값을 만족한 비율이다.

## 3. 하이라이트 지표

각 클립에 대해 평가자 점수와 예측 중요도를 비교한다. Fair, Good, VeryGood 등급별 positive clip을 구성하고 AP와 Hit@1을 산출한다.

## 4. element·relation 지표

element는 유형, 정규화 label과 시간 구간을 조합해 일치 여부를 판정한다. relation은 `subject-predicate-object` 삼중항을 비교하며, Relation Integrity는 relation 양 끝점과 predicate 선언 여부를 검사한다.

## 5. 재조립·운영 지표

- Coverage: 요구 element와 media unit 중 선택 결과에 포함된 비율
- Chronology Violation: 시간순 정책을 위반한 인접 단위의 비율
- Repeated Output Agreement: 동일 입력 반복 결과의 일치도
- Stage Latency: 수집, 변환, 평가, 계획 생성 단계별 소요시간
- Interface Conformance: Prediction Schema와 오류 계약 준수 비율

## 6. 결과 판정

| 상태 | 정의 |
|---|---|
| PASS | 입력·출력·지표·증빙 요건 충족 |
| CONDITIONAL_PASS | 경미한 이슈와 조치 조건을 포함해 충족 |
| FAIL | 핵심 계약 또는 합의 기준 미충족 |
| EXCLUDED | 시험 범위에서 사전 제외된 항목 |

기준값, 표본 수와 예외 규칙은 대상 시스템 시험계획서에서 실행 프로파일별로 고정한다.
