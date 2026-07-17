# 검증시스템 설계서

## 1. 목적

시맨틱 미디어 전송 과정에서 query, 시간 구간, 중요도, element, relation 및 재조립 계획의 정합성을 동일한 데이터 계약과 평가지표로 검증한다.

## 2. 설계 원칙

- 외부 데이터 형식은 dataset adapter에서 공통 모델로 정규화한다.
- 참조 출력과 대상 시스템 출력은 동일한 Prediction 계약을 사용한다.
- 지표 계산과 대상 시스템 연동을 분리하여 평가 산식의 독립성을 유지한다.
- 입력, 설정, 출력, 지표와 실행 정보를 증빙 파일로 연결한다.
- element와 media unit은 안정적인 ID로 relation의 양 끝점을 구성한다.

## 3. 계층 구조

| 계층 | 책임 |
|---|---|
| Dataset Layer | JSONL 로드, 필수 필드·범위·시간 단위 검증 |
| Semantic Layer | query, element, media unit, relation 공통 모델 |
| Integration Layer | 참조 및 ETRI 출력의 Prediction 변환 |
| Evaluation Layer | moment, highlight, relation, reassembly 평가 |
| Evidence Layer | 입력·출력·지표·실행정보 저장 |

## 4. 모듈

| 모듈 | 기능 |
|---|---|
| `datasets/qvhighlights.py` | QVHighlights 호환 annotation 로드 |
| `adapters/reference_baseline.py` | 결정적 참조 prediction 생성 |
| `adapters/etri_system.py` | 대상 시스템 연동 계약 |
| `evaluation/moment.py` | tIoU, MR-mAP, R@1 |
| `evaluation/highlight.py` | HL-mAP, HL-Hit@1 |
| `evaluation/relations.py` | relation node·predicate 무결성 |
| `assembly/planner.py` | 선택 구간 기반 재조립 계획 |
| `cli.py` | 검증 실행 및 결과 패키지 생성 |

## 5. 입출력 계약

입력 annotation은 `qid`, `query`, `duration`, `vid`, `relevant_windows`, `relevant_clip_ids`, `saliency_scores`를 사용한다. 출력 prediction은 `pred_relevant_windows`, `pred_saliency_scores`, `result_status`, `metadata`를 사용한다.

시맨틱 확장 데이터는 `semantic_elements`, `media_units`, `relations`, `expected_assembly`를 포함한다. JSON Schema가 자료형과 필수 필드를 검증하고 relation evaluator가 참조 무결성을 검사한다.

## 6. 대상 시스템 연동

`EtriSystemAdapter`는 대상 시스템의 API, 파일 또는 전송 추적 출력을 공통 Prediction 객체로 변환하는 경계를 제공한다. 연동 구현은 다음 계약을 따른다.

1. 동일 `qid`, `vid`, query 및 시간 기준을 사용한다.
2. 구간은 초 단위 `[start, end, score]`로 정규화한다.
3. 클립 중요도는 기준 클립 간격에 맞춰 배열로 변환한다.
4. 오류·부분 응답·timeout은 실행 로그와 결과 상태에 기록한다.
5. 변환 후 공통 evaluator를 호출하여 결과 비교 가능성을 보장한다.

## 7. 증빙 구조

```text
evidence/<execution_id>/
├─ environment.json
├─ input_manifest.json
├─ source_output/
├─ normalized_predictions.jsonl
├─ metrics.json
├─ reassembly_plans.jsonl
├─ logs/
└─ issues.csv
```
