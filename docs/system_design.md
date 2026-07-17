# 검증시스템 설계서

## 1. 문서 목적

본 문서는 시맨틱 미디어 스트리밍 검증시스템의 보고 단계 참조 아키텍처를 정의한다. 현 단계에서는 데이터 계약, 모듈 경계, 평가 흐름과 연말 연동 포인트를 확정한다.

## 2. 설계 원칙

- 외부 데이터셋은 adapter로 분리하여 교체 가능하게 한다.
- 시맨틱 element와 미디어 단위는 독립 ID를 부여한다.
- 시스템 출력과 정답 annotation을 분리한다.
- 설계 검증·Mock 검증·실제 검증 결과를 상태값으로 구분한다.
- 원본 미디어를 복제하지 않고 ID와 시간 참조로 처리한다.
- 시험의 재현을 위해 설정, 스키마, 입출력, 버전을 기록한다.

## 3. 논리 구조

```text
[Dataset Layer]
  QVHighlights / ETRI annotation / synthetic fixture
                  |
                  v
[Normalization Layer]
  DatasetAdapter -> QVAnnotation -> SemanticExtension
                  |
                  v
[Verification Layer]
  Moment Retrieval / Highlight / Element / Relation / Reassembly
                  |
                  v
[Target Integration Layer]
  EtriSystemAdapter -> Prediction / Logs / Timing
                  |
                  v
[Evidence Layer]
  JSONL / Metrics JSON / Screenshots / Meeting Record / Final Report
```

## 4. 모듈 책임

| 모듈 | 책임 | 현 버전 |
|---|---|---|
| `datasets.qvhighlights` | QVHighlights 호환 JSONL 변환 | 구현 |
| `models` | 공통 annotation·예측·관계 모델 | 구현 |
| `adapters.mock_reference` | Mock 출력 생성 | 구현 |
| `adapters.etri_system` | ETRI 대상 시스템 연동 경계 | interface |
| `evaluation.moment` | temporal IoU, MR-mAP, R@1 | 참조 구현 |
| `evaluation.highlight` | HL-mAP, Hit@1 | 참조 구현 |
| `evaluation.relations` | node·predicate 관계 정합성 | 구현 |
| `assembly.planner` | 예측 구간을 전송 단위로 변환 | 참조 구현 |
| `cli` | 사전검증 오케스트레이션 | 구현 |

## 5. 연말 연동 인터페이스

ETRI 대상 시스템의 프로토콜이 확정되면 `EtriSystemAdapter.request_analysis()`를 다음 중 하나로 구현한다.

1. HTTP/REST: video ID와 query를 전송하고 JSON 출력을 수신한다.
2. File exchange: 입력 JSONL 폴더와 출력 JSONL 폴더를 감시한다.
3. Transport trace: 전송 프로토콜 로그를 파싱하여 element-미디어 단위 매핑을 복원한다.

권장 출력은 `prediction.schema.json`을 따르며, 모든 실행에 `system_version`, `model_version`, `input_hash`, `started_at`, `completed_at`, `environment_id`를 기록한다.

## 6. 비기능 요구사항

- 재현성: 동일 입력·설정·버전으로 반복 실행한다.
- 추적성: 결과에 원본 ID, 예측 ID, 시험 ID를 포함한다.
- 확장성: dataset, model, target system adapter를 독립 교체한다.
- 보안성: 미디어 원본을 로그에 직접 포함하지 않는다.
- 라이선스: 외부 자원은 사전 승인 후 설정에 등록한다.

