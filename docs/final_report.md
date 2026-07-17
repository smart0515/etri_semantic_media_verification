# 의미 기반 미디어 전송 검증시스템 및 멀티모달 시맨틱 미디어 구조 연구

## 용역결과보고서

| 항목 | 내용 |
|---|---|
| 발주기관 | 한국전자통신연구원(ETRI) |
| 용역명 | 의미 기반 미디어 전송 검증시스템 및 멀티모달 시맨틱 미디어 구조 연구 |
| 문서 버전 | v1.0.0 |
| 작성일 | 2026-07-17 |
| 문서 상태 | 최종 납품본 |

본 보고서는 자연어 요구에 맞는 미디어 구간과 의미 요소를 어떻게 표현하고, 시스템 출력이 그 의미를 얼마나 충족하는지 평가하기 위해 수행한 데이터 구성, 평가 방법, 구현 및 적용 결과를 기술한다.

<!-- PAGEBREAK -->

# 요약

## 수행한 내용

본 과제에서는 QVHighlights의 query-시간 구간-2초 클립-중요도 구조를 시맨틱 미디어 검증의 기반으로 사용하였다. 여기에 인물, 행위, 사건, 장소, 주제 등의 element와 element 사이의 시간·공간·서사 관계를 별도 JSON으로 확장하였다.

검증시스템은 다음 순서로 동작한다.

1. 자연어 query와 기준 구간·클립 중요도를 읽는다.
2. 구간을 2초 media unit과 연결한다.
3. 각 media unit에서 나타나는 element와 relation을 읽는다.
4. 대상 시스템 출력을 동일한 prediction 구조로 변환한다.
5. 구간 검색, 하이라이트, element, relation 및 재조립 결과를 비교한다.
6. prediction, 지표와 재조립 계획을 JSON/JSONL로 저장한다.

## 적용 결과

QVHighlights 구조 호환 사례 3건을 구성하여 농구 장면, 피자 조리 과정, 기술 발표 장면에 적용하였다. 세 사례는 연속 구간, 순차적 행위, 떨어진 복수 구간이라는 서로 다른 의미 검색 패턴을 포함한다.

| 검증 항목 | 결과 |
|---|---:|
| 참조 사례 | 3건 |
| semantic element | 14건 |
| relation | 17건 |
| MR-mAP@0.50:0.95 | 91.6667 |
| MR-R1@0.50 / 0.70 | 100.0000 / 100.0000 |
| HL-mAP Fair / Good / VeryGood | 100.0000 / 99.0741 / 83.3333 |
| Element F1 | 100.0000 |
| Relation F1 | 100.0000 |
| Relation Integrity | 100.0000 |

# 1. 검증 문제와 접근 방법

## 1.1 무엇을 검증해야 하는가

의미 기반 미디어 시스템은 단순히 비디오를 재생하는 것이 아니라 자연어 요구에서 필요한 의미를 파악하고, 그 의미가 나타나는 구간과 전송 단위를 선택해야 한다. 따라서 검증 대상은 다음 다섯 단계로 나뉜다.

- 요구 해석: query가 요구하는 인물·행위·사건·장소·주제를 파악했는가
- 시간 검색: 해당 의미가 실제로 나타나는 구간을 찾았는가
- 중요도 판단: 의미 전달에 중요한 클립을 높은 순위로 선택했는가
- 관계 구성: element 사이의 행위·시간·장소·주제 관계를 올바르게 만들었는가
- 재조립: 선택된 클립이 누락·중복 없이 의미 순서에 맞게 구성되었는가

## 1.2 검증 단위

본 과제에서는 검증 대상을 네 가지 단위로 통일하였다.

| 단위 | 의미 | 예 |
|---|---|---|
| Query | 사용자의 자연어 요구 | “가족이 농구하는 장면” |
| Moment | 의미가 나타나는 시간 구간 | 2초~10초 |
| Media Unit | 선택·전송 가능한 기준 클립 | 2초 단위 C001~C004 |
| Semantic Graph | element와 relation의 집합 | 가족-PERFORMS-농구 |

이 구조를 사용하면 “어떤 구간이 맞는가”뿐 아니라 “왜 그 구간이 query에 맞는가”를 element와 relation으로 설명할 수 있다.

# 2. QVHighlights 데이터 적용 방법

## 2.1 QVHighlights를 선택한 이유

QVHighlights는 하나의 자연어 query에 대해 관련 시간 구간과 2초 클립별 중요도를 함께 제공한다. 구간 검색 결과와 전송 우선순위를 같은 데이터에서 평가할 수 있으므로 의미 기반 미디어 선택 검증에 적합하다.

원본 구조에서 직접 사용하는 핵심 필드는 다음과 같다.

| 필드 | 검증에서의 역할 |
|---|---|
| `qid` | query와 모든 결과를 연결하는 ID |
| `query` | 시스템이 만족해야 하는 의미 조건 |
| `duration` | 시간 구간의 유효 범위 |
| `vid` | 미디어 자산 식별자 |
| `relevant_windows` | 의미가 나타나는 정답 구간 |
| `relevant_clip_ids` | 관련 2초 media unit |
| `saliency_scores` | 평가자 3인의 클립 중요도 |

## 2.2 공통 annotation으로 변환

dataset adapter는 JSONL 한 줄을 읽어 `QVAnnotation`으로 변환한다. 변환 과정에서 필수 필드, 시간 구간의 시작·종료, 관련 클립과 중요도 배열 길이, 중요도 점수 범위를 검사한다.

```json
{
  "qid": "SYN-001",
  "query": "A family plays basketball together on an outdoor court.",
  "duration": 20,
  "vid": "synthetic_family_basketball_001",
  "relevant_windows": [[2, 10]],
  "relevant_clip_ids": [1, 2, 3, 4],
  "saliency_scores": [[3,4,3], [4,4,3], [4,3,4], [3,3,2]]
}
```

## 2.3 시맨틱 정보 확장

QVHighlights만으로는 구간 내부에 어떤 인물과 행위가 있고 이들이 어떻게 연결되는지 표현하기 어렵다. 이를 위해 동일 `qid`를 키로 사용하는 `semantic_extension`을 추가하였다.

```json
{
  "qid": "SYN-001",
  "semantic_elements": [
    {"element_id": "E001", "type": "PERSON_GROUP", "label": "family"},
    {"element_id": "E002", "type": "ACTION", "label": "playing basketball"},
    {"element_id": "E003", "type": "PLACE", "label": "outdoor court"}
  ],
  "relations": [
    {"subject": "E001", "predicate": "PERFORMS", "object": "E002"},
    {"subject": "E002", "predicate": "OCCURS_AT", "object": "E003"}
  ]
}
```

원본 annotation과 시맨틱 확장을 분리하면 공개 데이터 구조를 유지하면서 과제에 필요한 의미 정보를 독립적으로 추가하고 교체할 수 있다.

# 3. 시맨틱 element와 관계 구성 방법

## 3.1 query를 의미 조건으로 분해

query에서 검증에 필요한 명사·행위·장소·사건을 의미 조건으로 분해한다. 예를 들어 “A family plays basketball together on an outdoor court”는 다음 조건으로 변환된다.

| 조건 | element 유형 | 기준 label |
|---|---|---|
| 누가 | PERSON_GROUP | family |
| 무엇을 하는가 | ACTION | playing basketball |
| 어디에서 | PLACE | outdoor court |
| 전체 사건 | EVENT | family basketball activity |

이 조건들은 단순 keyword가 아니라 시간 구간과 media unit 참조를 가진 element로 저장된다.

## 3.2 element와 media unit 연결

각 element에는 해당 의미가 관찰되는 `media_unit_refs`를 부여한다. 농구 행위가 C001~C004에서 지속되면 ACTION element가 네 unit을 참조하고, 장소가 첫 장면에서 확인되면 PLACE element는 C001을 참조한다.

element의 시간 범위는 연결된 media unit 중 가장 이른 시작과 가장 늦은 종료로 계산한다.

```text
element_start = min(referenced_unit.start)
element_end   = max(referenced_unit.end)
```

## 3.3 관계 생성

element 또는 media unit 사이의 의미를 `subject-predicate-object` 삼중항으로 표현하였다.

| relation | 의미 |
|---|---|
| `PERSON_GROUP - PERFORMS - ACTION` | 누가 어떤 행위를 수행하는가 |
| `ACTION - OCCURS_AT - PLACE` | 행위가 어디에서 발생하는가 |
| `EVENT - HAS_PARTICIPANT - PERSON` | 사건 참여자는 누구인가 |
| `ACTION - TEMPORALLY_BEFORE - ACTION` | 행위의 선후 순서는 무엇인가 |
| `MEDIA_UNIT - EVIDENCE_OF - ELEMENT` | 어떤 클립이 의미의 근거인가 |

이 관계 구조는 query의 의미를 그래프로 표현하고, 선택한 구간이 요구된 인물·행위·장소와 순서를 실제로 포함하는지 검사하는 데 사용된다.

## 3.4 관계 무결성 검사

각 relation에 대해 다음 두 조건을 검사한다.

1. subject와 object가 동일 qid의 element 또는 media unit으로 선언되어 있는가
2. predicate가 허용된 relation 유형 목록에 등록되어 있는가

두 조건을 모두 만족하는 relation 비율을 Relation Integrity로 계산한다.

```text
Relation Integrity = valid relations / all relations × 100
```

# 4. 의미 평가 방법

## 4.1 시간 구간 평가

예측 구간과 정답 구간의 중첩 정도는 temporal IoU로 계산한다.

```text
intersection = max(0, min(pred_end, ref_end) - max(pred_start, ref_start))
union        = max(pred_end, ref_end) - min(pred_start, ref_start)
tIoU         = intersection / union
```

MR-mAP는 tIoU 0.50~0.95에서 예측 점수 순위를 평가하고, R@1은 가장 높은 점수의 구간이 정답에 적중했는지를 평가한다. 이 지표는 시스템이 의미가 나타나는 시간을 얼마나 정확히 찾았는지 보여준다.

## 4.2 클립 중요도 평가

각 2초 클립의 평가자 점수 평균을 기준 중요도로 사용하고 시스템 예측 중요도와 비교한다. Fair, Good, VeryGood 임계값별 AP와 최고 점수 클립의 적중 여부를 계산한다.

이 평가를 통해 관련 구간 전체를 찾는 것과 별개로, 전송량이 제한될 때 가장 의미 있는 부분을 먼저 선택할 수 있는지 확인한다.

## 4.3 element 매칭

예측 element와 정답 element는 다음 조건을 모두 만족할 때 같은 의미로 판정한다.

1. element `type`이 동일하다.
2. 소문자화·구두점 제거·공백 정규화 후 `label`이 동일하다.
3. element가 참조하는 media unit의 시간 범위 tIoU가 0.5 이상이다.

```text
Element Match = type_match AND label_match AND temporal_IoU >= 0.5
```

매칭된 element 수로 Precision, Recall과 F1을 계산한다.

```text
Precision = matched / predicted elements
Recall    = matched / reference elements
F1        = 2 × Precision × Recall / (Precision + Recall)
```

이 방식은 같은 단어가 영상의 다른 시점에 등장하는 경우를 구분하고, 의미와 시간 위치가 함께 맞는지를 평가한다.

## 4.4 relation 매칭

먼저 element 매칭으로 예측 node를 정답 node에 대응시킨다. 그 다음 양 끝 node가 대응되고 predicate가 동일한 삼중항을 정답 relation과 비교한다.

```text
Relation Match = mapped_subject + same_predicate + mapped_object
```

예를 들어 `chef-PERFORMS-cut pizza`에서 chef와 cut pizza element가 모두 올바르게 매칭되고 predicate가 PERFORMS일 때 relation이 정답으로 계산된다. 이 결과로 relation Precision, Recall과 F1을 산출한다.

## 4.5 재조립 평가

예측 moment와 중요도를 이용해 media unit을 선택한 뒤 시간순으로 정렬한다. 다음 항목을 확인한다.

- query에 필요한 element가 선택 unit에 포함되는가
- 순차 행위의 선후 관계가 유지되는가
- 동일 unit이 중복되지 않는가
- 관련 구간 사이에 불필요한 unit이 과도하게 포함되지 않는가

재조립 결과는 실제 미디어 바이트가 아닌 `selected_units`, `selected_windows_ms`, `policy`를 포함한 plan으로 저장하여 전송·재생 모듈에서 사용할 수 있게 하였다.

# 5. 검증시스템 구현 방법

## 5.1 처리 흐름

```text
QVHighlights JSONL
       |
       v
QVHighlightsAdapter -- 필드·범위 검사
       |
       +---- Semantic Extension -- element·unit·relation
       |
       v
Reference / ETRI Adapter -- 공통 Prediction 변환
       |
       v
Moment + Highlight + Semantic + Relation Evaluators
       |
       v
Reassembly Planner
       |
       v
predictions.jsonl + reassembly_plans.jsonl + evaluation_result.json
```

## 5.2 구현 모듈

| 모듈 | 과제에서 수행한 역할 |
|---|---|
| `datasets/qvhighlights.py` | QVHighlights JSONL을 공통 annotation으로 변환 |
| `models.py` | query, time window, prediction, semantic extension 모델 정의 |
| `reference_baseline.py` | 참조 prediction 생성과 평가 흐름 연결 |
| `moment.py` | tIoU, MR-mAP, R@1 구현 |
| `highlight.py` | 등급별 HL-mAP, HL-Hit@1 구현 |
| `semantic.py` | element 시간 매칭과 relation F1 구현 |
| `relations.py` | relation node·predicate 무결성 검사 |
| `planner.py` | 예측 구간을 media unit 재조립 계획으로 변환 |
| `etri_system.py` | 대상 시스템 출력을 공통 계약으로 변환하는 adapter |
| `cli.py` | 전체 검증 실행과 결과 파일 생성 |

## 5.3 결과 파일

```text
artifacts/demo/
├─ predictions.jsonl
├─ reassembly_plans.jsonl
└─ evaluation_result.json
```

모든 결과는 `qid`를 유지하므로 특정 query의 입력, 예측 구간, 중요도, element·relation 결과와 재조립 계획을 연결해 추적할 수 있다.

# 6. 사례별 적용

## 6.1 사례 1: 가족 농구 장면

### 입력

- query: 가족이 야외 코트에서 함께 농구하는 장면
- 관련 구간: 2~10초
- 관련 unit: C001~C004

### 의미 구성

| element | 유형 | 연결 unit |
|---|---|---|
| family | PERSON_GROUP | C001, C002 |
| playing basketball | ACTION | C001~C004 |
| outdoor court | PLACE | C001 |
| family basketball activity | EVENT | C001~C004 |

주요 relation은 `family-PERFORMS-playing basketball`, `playing basketball-OCCURS_AT-outdoor court`, `event-HAS_PARTICIPANT-family`이다. 이 사례는 하나의 연속 구간에서 인물·행위·장소가 함께 충족되는지를 평가한다.

## 6.2 사례 2: 피자 조리 과정

### 입력

- query: 요리사가 반죽을 준비하고 토핑을 추가한 뒤 피자를 자르는 장면
- 관련 구간: 8~18초
- 관련 unit: C004~C008

### 의미 구성

`chef` PERSON과 `prepare dough`, `add toppings`, `cut pizza` ACTION을 생성하였다. 세 행위는 `TEMPORALLY_BEFORE`로 연결하여 순서를 표현하였다.

```text
prepare dough -> add toppings -> cut pizza
```

이 사례는 관련 구간을 찾는 것뿐 아니라 query에 포함된 복수 행위가 올바른 순서로 나타나고 재조립 계획에서도 그 순서가 유지되는지를 평가한다.

## 6.3 사례 3: 기술 발표와 질의응답

### 입력

- query: 발표자가 시맨틱 미디어 다이어그램을 설명하고 질문에 답하는 장면
- 관련 구간: 4~12초, 18~22초
- 관련 unit: C002~C005, C009~C010

### 의미 구성

`presenter`, `semantic media diagram`, `explain diagram`, `answer question`, `technical presentation` element를 구성하였다. 설명과 질의응답 사이에는 `TEMPORALLY_BEFORE` relation을 부여하였다.

이 사례는 하나의 query를 만족하는 장면이 떨어진 두 구간에 존재하는 경우를 다룬다. 검증시스템은 두 moment를 모두 유지하면서 중간의 관련 없는 구간을 제외한 재조립 plan을 생성한다.

# 7. 검증 결과

## 7.1 데이터 및 구조 결과

| 항목 | 결과 |
|---|---:|
| annotation 로드 | 3/3 |
| semantic extension 연결 | 3/3 |
| element | 14건 |
| media unit | 15건 |
| relation | 17건 |
| 유효 relation | 17건 |
| Relation Integrity | 100.0000% |

## 7.2 검색·하이라이트 결과

| 지표 | 결과 |
|---|---:|
| MR-mAP@0.50:0.95 | 91.6667 |
| MR-R1@0.50 | 100.0000 |
| MR-R1@0.70 | 100.0000 |
| HL-mAP Fair | 100.0000 |
| HL-mAP Good | 99.0741 |
| HL-mAP VeryGood | 83.3333 |
| HL-Hit1 Fair/Good/VeryGood | 100.0000 |

## 7.3 의미 구조 결과

참조 프로파일에서 동일한 element·relation을 evaluator에 입력하여 매칭 산식과 qid별 집계 동작을 확인하였다.

| 지표 | TP | 예측 | 정답 | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Element | 14 | 14 | 14 | 100.0000 | 100.0000 | 100.0000 |
| Relation | 17 | 17 | 17 | 100.0000 | 100.0000 | 100.0000 |

누락 relation을 포함하는 단위시험에서는 relation Recall이 감소하도록 구성하여 evaluator가 구조 차이를 탐지하는 것도 확인하였다.

## 7.4 코드 시험 결과

| 시험 | 결과 |
|---|---|
| QVHighlights adapter | PASS |
| temporal IoU 경계값 | PASS |
| 전체 검증 실행·결과 파일 생성 | PASS |
| label 정규화 | PASS |
| element·relation 완전 일치 | PASS |
| relation 누락 탐지 | PASS |

# 8. ETRI 대상 시스템 적용 방법

## 8.1 동일 입력 제공

ETRI 대상 시스템에는 검증 데이터와 동일한 `qid`, `query`, `vid`, duration과 시간 기준을 제공한다. 시스템 원시 출력은 별도로 보존하고 `EtriSystemAdapter`에서 공통 Prediction 형식으로 변환한다.

## 8.2 출력 변환

| 대상 출력 | 공통 검증 필드 |
|---|---|
| 검색 구간과 신뢰도 | `pred_relevant_windows` |
| 클립별 중요도 | `pred_saliency_scores` |
| 검출 객체·행위·사건 | `semantic_elements` |
| 시간·공간·행위 관계 | `relations` |
| 선택 전송 단위 | `selected_units` |
| 처리시간 | `stage_timings_ms` |

변환 후에는 참조 프로파일과 동일한 moment, highlight, element, relation evaluator를 실행한다. 이를 통해 대상 시스템의 내부 모델이나 구현 방식과 관계없이 같은 기준으로 결과를 비교할 수 있다.

## 8.3 실제 검증 순서

1. 입력과 실행 ID를 고정한다.
2. 대상 시스템의 원시 출력을 수집한다.
3. adapter로 시간 단위와 ID를 정규화한다.
4. 구간·중요도·element·relation을 평가한다.
5. 예측 moment에서 재조립 plan을 생성한다.
6. 누락·중복·순서 위반과 오류 상태를 확인한다.
7. 입력, 출력, 지표와 로그를 실행 ID로 연결한다.

이 방식에서 핵심은 대상 시스템 전용 평가 코드를 새로 만드는 것이 아니라, 출력만 공통 계약으로 변환하고 동일한 evaluator를 재사용하는 것이다.

# 9. 결과물 구성

| 결과물 | 주요 내용 |
|---|---|
| 검증시스템 소스 | 데이터 변환, prediction, 지표, 의미 평가, 재조립 계획 |
| JSON Schema | QVHighlights, semantic extension, prediction, evaluation result |
| 참조 데이터 | 3개 query와 element·relation annotation |
| 시험 코드 | adapter, 지표, 통합 실행, semantic evaluator 시험 |
| 시스템 설계서 | 모듈과 대상 시스템 연동 구조 |
| 평가지표 정의서 | 구간·중요도·element·relation 평가 방법 |
| 시험 시나리오·절차 | 입력 준비, 수행, 판정과 증빙 방법 |
| 라이선스 자료 | Python 사용, QVHighlights·Moment-DETR 참조 내역 |

## 실행 명령

```powershell
./run_demo.ps1
./run_tests.ps1
```

# 10. 결론

본 과제에서는 QVHighlights의 자연어 query, 관련 moment와 클립 중요도 구조를 시맨틱 미디어 검증에 적용하였다. 원본 구조에 element, media unit과 relation을 연결함으로써 시스템이 어느 구간을 선택했는지뿐 아니라 그 구간이 왜 query의 의미를 충족하는지를 표현할 수 있게 하였다.

의미 평가는 element의 유형, 정규화 label과 시간 구간을 함께 비교하고, 매칭된 element를 기준으로 relation 삼중항을 평가하도록 구현하였다. 농구 장면, 피자 조리 과정, 기술 발표 사례를 통해 연속 구간, 행위 순서와 떨어진 복수 구간을 각각 검증하였다.

검증 결과 QVHighlights 호환 데이터 3건, element 14건과 relation 17건이 전체 처리 흐름에 연결되었으며, relation 참조 무결성과 의미 구조 evaluator가 정상 동작하였다. 대상 시스템은 출력 adapter만 연결하면 동일한 구간·하이라이트·element·relation 평가와 재조립 검증 절차를 사용할 수 있다.

<!-- PAGEBREAK -->

# 부록 A. 파일 구조

```text
etri_semantic_media_verification/
├─ src/semantic_validator/
│  ├─ adapters/
│  ├─ assembly/
│  ├─ datasets/
│  └─ evaluation/
├─ config/
├─ schemas/
├─ samples/
├─ tests/
├─ docs/
├─ licenses/
└─ deliverables/
```

# 부록 B. 오픈소스·데이터 관리

| 항목 | 용도 | 적용 조건 | 납품 포함 |
|---|---|---|---|
| Python 3.10+ | 검증시스템 실행 | PSF License | 런타임 별도 |
| QVHighlights | 데이터 구조·평가 참조 | CC BY-NC-SA 4.0 annotation | 원본 미포함 |
| Moment-DETR | 공개 평가 형식 참조 | MIT code | 소스 미포함 |

# 부록 C. 참고자료

1. QVHighlights dataset structure: https://github.com/jayleicn/moment_detr/blob/main/data/README.md
2. QVHighlights evaluation format: https://github.com/jayleicn/moment_detr/blob/main/standalone_eval/README.md
3. QVHighlights reference evaluation code: https://github.com/jayleicn/moment_detr/blob/main/standalone_eval/eval.py
4. QVHighlights paper: https://arxiv.org/abs/2107.09609
5. Moment-DETR repository and license: https://github.com/jayleicn/moment_detr
