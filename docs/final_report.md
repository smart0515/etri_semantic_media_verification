# 의미 기반 미디어 전송 검증시스템 및 멀티모달 시맨틱 미디어 구조 연구

## 용역결과보고서 - 보고 단계 설계 및 사전검증 결과

| 항목 | 내용 |
|---|---|
| 발주기관 | 한국전자통신연구원(ETRI) |
| 용역명 | 의미 기반 미디어 전송 검증시스템 및 멀티모달 시맨틱 미디어 구조 연구 |
| 문서 버전 | v0.1.0-report |
| 작성일 | 2026-07-17 |
| 문서 상태 | 보고용 납품본 |
| 시스템 상태 | 설계 참조 구현 및 PRELIMINARY_MOCK 사전검증 |

### 문서 사용 주의

본 보고서의 사전검증 수치는 자체 작성한 QVHighlights 호환 합성 데이터와 정답에서 파생한 Mock 예측을 이용하여 데이터 흐름, 스키마, 평가 산식의 연결 가능성을 확인한 결과이다. 이 수치는 멀티모달 모델, 운영 시스템 또는 ETRI 대상 시스템의 실제 성능을 의미하지 않는다.

<!-- PAGEBREAK -->

# 문서 관리

## 개정 이력

| 버전 | 일자 | 구분 | 주요 내용 |
|---|---|---|---|
| 0.1.0-report | 2026-07-17 | 초안·납품본 | 설계, 코드 골격, 평가지표, 시험절차, QVHighlights 적용, 오픈소스 관리 |

## 산출물 상태 구분

| 상태 | 정의 | 본 납품 적용 |
|---|---|---|
| DESIGN_DEFINED | 구조·입출력·산식·절차를 정의 | 적용 |
| CONCEPT_SAMPLE | 개념 설명을 위해 새로 작성한 샘플 | 적용 |
| PRELIMINARY_MOCK | 정답 파생 Mock 출력으로 흐름을 검증 | 적용 |
| MODEL_PREDICTION | 실제 모델 추론 결과 | 미적용 |
| ETRI_SYSTEM_OUTPUT | ETRI 대상 시스템 출력 | 미적용 |
| JOINT_VERIFIED | ETRI-용역기관 상호 입회 확인 | 미적용 |

## 검토 및 승인

본 보고서는 보고 단계 설계 결과를 제시한다. 실제 데이터셋 사용, 멀티모달 모델 선정, 합격 기준값, ETRI 연동 방식은 후속 협의에서 확정해야 한다.

# 요약

## 과업 목적

본 용역은 시맨틱 미디어 스트리밍 시스템의 동작 및 성능을 비교검증할 검증시스템과 평가지표 체계를 정의하고, 멀티모달 미디어에서 추출된 시맨틱 element 간 관계를 표현할 데이터 모델을 연구하는 것을 목적으로 한다.

## 보고 단계 수행 결과

본 납품본에서는 다음을 완료했다.

- QVHighlights 형식을 참조한 dataset adapter와 공통 annotation 모델 정의
- query, 시간 구간, 2초 클립, 중요도를 ETRI 과업에 매핑
- 인물·객체·행위·사건·장소·주제·상황 element 확장 모델 정의
- 시간·공간·서사·행위·인과·미디어·출처 relation 사전 정의
- Moment Retrieval, Highlight Detection, Relation Integrity 사전검증 코드 작성
- 자체 작성한 QVHighlights 호환 합성 데이터 3건 및 시맨틱 확장 샘플 작성
- 평가지표 체계, 시험 시나리오, 검증 절차 및 증빙 방안 수립
- QVHighlights·Moment-DETR 및 연말 도입 후보에 대한 오픈소스·데이터 라이선스 관리 방안 작성

## 주요 결론

자연어 요구, 관련 시간 구간, 2초 클립, 클립 중요도로 구성된 QVHighlights 구조는 시맨틱 미디어 재조립 검증을 설명하기 위한 유용한 참조점을 제공한다. 다만 원본에는 element 유형, relation, 전송 페이로드, 음성·텍스트 중간 결과가 없으므로 별도 확장 annotation이 필요하다. 본 연구는 원본 annotation과 확장 annotation을 분리하는 방식을 채택했다.

# 1. 과업 개요

## 1.1 배경

시맨틱 미디어 스트리밍은 원본 미디어를 그대로 전송하는 데 그치지 않고, 미디어 내 인물, 사건, 주제, 상황과 같은 의미 단위를 파악하여 사용자 요구에 맞는 파생 콘텐츠를 재조립·제공하는 것을 지향한다. 이러한 시스템은 분석, element 추출, 전송 단위 연결, 재조립, 재생의 여러 단계로 구성되며, 각 단계의 정합성이 종단 경험을 결정한다.

기존 미디어 시스템의 bitrate, packet loss, startup delay와 같은 지표만으로는 이러한 의미 기반 처리의 정확도와 적절성을 충분히 평가하기 어렵다. 따라서 참조 데이터, 공통 출력 계약, 정량 지표, 시험 절차, 증빙 구조를 갖춘 별도 검증시스템이 필요하다.

## 1.2 목표

1. 시맨틱 미디어 검증시스템의 참조 설계를 제시한다.
2. 시간 구간, 중요도, element, relation, 재조립, 성능을 포함한 평가지표 체계를 제시한다.
3. QVHighlights 호환 데이터를 통해 연말 실제 구현으로 확장 가능한 코드 골격을 제공한다.
4. 시험 시나리오, 절차, 판정, 증빙 방법을 수립한다.
5. 시맨틱 element 사이의 시간·공간·서사·인과·미디어 관계를 구조화한다.
6. 오픈소스, 데이터셋, 모델, 미디어의 라이선스 위험을 관리한다.

## 1.3 보고 단계 범위

현 단계의 최종 목표는 실제 ETRI 시스템 성능 측정이 아니라, 연말 구현을 위한 설계·데이터·코드·시험 계약의 정합성을 확보하는 것이다. 이에 따라 다음을 범위에서 제외했다.

- 실제 비디오 프레임 특징 추출
- ASR, OCR, 음향 인식 모델 실행
- 실제 멀티모달 element 자동 추출
- ETRI 대상 시스템 API·전송 프로토콜 연동
- FFmpeg 등을 이용한 미디어 파일 실제 재조립
- 실제 시스템 지연시간·처리량 측정
- ETRI 담당자 입회 합격·불합격 판정

# 2. 요구사항 분석 및 산출물 매핑

## 2.1 과업-산출물 추적성

| 과업 항목 | 본 납품 산출물 | 상태 |
|---|---|---|
| 검증용 시스템 설계안 | 시스템 설계서, 모듈 구조, adapter 경계 | DESIGN_DEFINED |
| 평가지표 체계 설계안 | 평가지표 정의서, metrics config | DESIGN_DEFINED |
| 검증시스템 구현 | Python 참조 구현, JSON Schema, CLI, test | REFERENCE_IMPLEMENTATION |
| 시험 시나리오·절차 | 사전 8건, 연말 12건, 검증 절차서 | DESIGN_DEFINED |
| ETRI 대상 실제 검증 | EtriSystemAdapter 경계, 입회 템플릿, 연말 로드맵 | NOT_TESTED |
| 검증 결과 보고서 | 본 PDF·Markdown, 사전검증 JSON | PRELIMINARY_MOCK |
| element 관계 데이터 모델 | element·media unit·relation extension | DESIGN_DEFINED |
| 오픈소스·라이선스 | 사용내역 CSV, Third-Party Notices | DOCUMENTED |

## 2.2 현 시점 검수 포인트

현 납품본은 다음 질문에 대한 답을 제공한다.

- 어떤 데이터를 입력하고 어떤 결과를 비교할 것인가?
- 자연어 요구와 비디오 전송 단위를 어떻게 연결할 것인가?
- element와 relation을 어떤 JSON으로 표현할 것인가?
- 구간, 중요도, element, relation을 어떤 지표로 평가할 것인가?
- Mock 결과와 실제 ETRI 결과를 어떻게 구분할 것인가?
- 연말 연동에서 어느 모듈을 구현·교체할 것인가?
- 외부 dataset·code·model을 어떻게 관리할 것인가?

<!-- PAGEBREAK -->

# 3. QVHighlights 참조 데이터 분석

## 3.1 데이터셋 개요

QVHighlights는 자연어 query에 대해 비디오의 관련 moment를 찾고, query와 관련된 하이라이트의 중요도를 탐지하는 문제를 다룬다. 공식 annotation은 JSON Lines 형식이며, 각 레코드는 질의 ID, 자연어 query, 영상 길이, 영상 ID, 관련 시간 구간, 관련 2초 클립 ID, 세 명의 평가자가 부여한 클립 중요도 점수를 갖는다.

QVHighlights의 핵심 장점은 query 기반 moment retrieval과 highlight detection을 하나의 annotation에서 동시에 다룰 수 있다는 점이다. 이는 사용자 요구에 맞는 시맨틱 미디어 구간을 선택하고 중요도에 따라 재조립하는 과업을 설명하는 데 적합하다.

## 3.2 JSON 구조

```json
{
  "qid": 8737,
  "query": "A family is playing basketball together on a green court outside.",
  "duration": 126,
  "vid": "bP5KfdFJzC4_660.0_810.0",
  "relevant_windows": [[0, 16]],
  "relevant_clip_ids": [0, 1, 2, 3, 4, 5, 6, 7],
  "saliency_scores": [[4, 1, 1], [4, 1, 1], [4, 2, 1]]
}
```

| 필드 | 검증 해석 | ETRI 확장 |
|---|---|---|
| qid | 사용자 요구 단위 | 시험·요청 추적 ID |
| query | 선택할 의미 조건 | SemanticRequest |
| duration | 시간 정규화 기준 | MediaAsset metadata |
| vid | 원본 미디어 참조 | asset·stream ID |
| relevant_windows | 정답 moment | 예상 재조립 구간 |
| relevant_clip_ids | 2초 전송 후보 단위 | MediaUnit |
| saliency_scores | 클립 중요도 정답 | 전송·재조립 우선순위 |

## 3.3 예측 구조

시스템 출력은 `pred_relevant_windows`에 `[start, end, score]` 형식의 구간을 저장하고, `pred_saliency_scores`에 모든 2초 클립의 예측 중요도를 저장한다. 본 구현은 이 구조에 `result_status`와 `metadata`를 추가하여 Mock·모델·ETRI 출력을 구분한다.

```json
{
  "qid": "SYN-001",
  "query": "A family plays basketball together on an outdoor court.",
  "vid": "synthetic_family_basketball_001",
  "pred_relevant_windows": [[2.25, 9.75, 0.95]],
  "pred_saliency_scores": [0.0, 3.33, 3.67, 3.67, 2.67],
  "result_status": "PRELIMINARY_MOCK"
}
```

## 3.4 제약

QVHighlights의 구간·중요도 annotation만으로는 인물, 객체, 사건, 주제, 상황, 음성, 텍스트, 공간, 인과 관계를 직접 평가할 수 없다. 따라서 QVHighlights를 완전한 정답으로 간주하지 않고, moment·highlight 정답을 제공하는 기반 계층으로 사용한다. element·relation 정답은 ETRI extension으로 분리하여 구축한다.

## 3.5 라이선스 판단

공식 Moment-DETR 저장소의 안내에 따르면 코드는 MIT, QVHighlights annotation은 CC BY-NC-SA 4.0이다. CC BY-NC-SA 4.0은 출처 표시, 비영리 사용, 변경물의 동일조건 배포 조건을 포함한다. 유상 용역에서 원본 annotation을 이용·납품하는 행위의 허용 여부는 사전 검토가 필요하다.

본 납품본에는 QVHighlights 원본 annotation, YouTube 영상, Moment-DETR 코드를 포함하지 않았다. 스키마 및 절차 확인에 사용된 3건의 레코드는 본 용역을 위해 새로 작성한 합성 샘플이다.

# 4. 검증시스템 설계안

## 4.1 전체 아키텍처

```text
External Dataset / ETRI Annotation / Synthetic Fixture
                         |
                         v
                  Dataset Adapters
                         |
                         v
       Common Annotation + Semantic Extension
                         |
           +-------------+--------------+
           |             |              |
           v             v              v
    Mock/Model Adapter  ETRI Adapter  Relation Model
           |             |              |
           +-------------+--------------+
                         |
                         v
         Moment / Highlight / Element / Relation Evaluators
                         |
                         v
             Reassembly Plan + Evidence Package
```

## 4.2 계층 별 책임

### Dataset Layer

dataset 특유 JSON, 파일 경로, ID, 시간 단위를 공통 모델로 변환한다. QVHighlights adapter와 후속 ETRI annotation adapter를 교체 가능하게 분리한다.

### Semantic Layer

query를 SemanticRequest로, 인물·행위·사건·주제를 SemanticElement로, 2초 클립·전송 페이로드를 MediaUnit으로 정규화한다. Relation을 통해 element-element 및 element-media unit 연결을 표현한다.

### Target Integration Layer

검증시스템 참조 모델과 ETRI 대상 시스템의 출력을 동일 Prediction 계약으로 변환한다. 현 버전의 `EtriSystemAdapter`는 인터페이스만 제공하며, 프로토콜 확정 후 HTTP, JSONL 파일 교환, 전송 추적 방식 중 하나로 구현한다.

### Evaluation Layer

정답과 예측의 qid·vid 범위를 검사한 후 moment, highlight, element, relation, reassembly, consistency, performance 지표를 산출한다. 평가 결과에는 항상 result status와 면책 문구를 포함한다.

### Evidence Layer

원시 입력, 원시 출력, 정규화 출력, 지표 JSON, 로그, 환경 명세, 파일 hash, 입회 회의록을 실행 ID로 연결한다.

## 4.3 구현 구조

| 경로 | 기능 |
|---|---|
| `src/semantic_validator/models.py` | 공통 annotation·예측·extension 모델 |
| `datasets/qvhighlights.py` | QVHighlights 호환 JSONL 검사·로드 |
| `adapters/mock_reference.py` | 흐름 확인용 정답 파생 Mock 예측 |
| `adapters/etri_system.py` | 연말 ETRI 연동 interface |
| `evaluation/moment.py` | tIoU, MR-mAP, R@1 |
| `evaluation/highlight.py` | HL-mAP, HL-Hit@1 |
| `evaluation/relations.py` | relation node·predicate 정합성 |
| `assembly/planner.py` | moment에서 시간순 media unit manifest 생성 |
| `cli.py` | 전체 사전검증 오케스트레이션 |

## 4.4 설계 특성

- 외부 dataset의 정보구조가 바뀌어도 adapter만 수정한다.
- 평가 코드는 멀티모달 모델·ETRI 시스템에서 독립한다.
- 출력의 상태를 필수 필드로 관리하여 Mock 결과의 오인을 방지한다.
- 원본 미디어 바이트 대신 ID·timestamp·hash를 사용하여 보안·저작권 위험을 줄인다.
- 설정·스키마·코드·샘플·시험을 하나의 Git 버전으로 관리한다.

<!-- PAGEBREAK -->

# 5. 시맨틱 element 관계 구조 데이터 모델

## 5.1 개념 모델

| 엔티티 | 목적 | 핵심 필드 |
|---|---|---|
| SemanticRequest | 사용자가 원하는 의미 조건 | qid, text, request_type |
| MediaAsset | 원본 영상·음성·텍스트 자산 | media_id, duration, modality |
| SemanticElement | 인물·객체·행위·사건·주제 | element_id, type, label, confidence |
| MediaUnit | 전송·재조립 가능 단위 | unit_id, start_ms, end_ms, stream_id |
| Relation | node 사이의 관계 | subject, predicate, object, confidence |
| AssemblyPlan | 재조립 순서·정책 | selected_units, policy, constraint |
| Provenance | 출처·모델·변환 이력 | source, generator, version, timestamp |

## 5.2 element 유형

`PERSON`, `PERSON_GROUP`, `OBJECT`, `ACTION`, `EVENT`, `PLACE`, `TOPIC`, `SITUATION`, `TEXT`, `AUDIO_EVENT`를 1차 유형으로 정의했다. 이 분류는 query 기반 구간 검색에서 추출할 대상을 표현하며, 연말에는 다음 속성을 확장한다.

- 모델 신뢰도·추출 모달리티
- 원본 frame·clip·ASR segment·OCR span 참조
- 유의어·표준명·지식 그래프 ID
- 수작 annotation·모델 annotation 구분
- 검수 상태·합의 이력

## 5.3 relation 분류

| 분류 | 예시 | 검증 사용 |
|---|---|---|
| 시간 | TEMPORALLY_BEFORE, AFTER, OVERLAPS | 순서·겹침·재조립 |
| 공간 | OCCURS_AT, SPATIALLY_NEAR | 장소·공간 조건 |
| 서사 | HAS_TOPIC, HAS_PARTICIPANT | 주제·사건 흐름 |
| 행위 | PERFORMS, PARTICIPATES_IN | 인물-행위 연결 |
| 인과 | CAUSES | 원인-결과 맥락 |
| 미디어 | EVIDENCE_OF, DESCRIBED_BY | element-미디어 근거 |
| 출처 | DERIVED_FROM | 추적성·재현성 |

## 5.4 extension JSON

```json
{
  "schema_version": "0.1.0",
  "qid": "SYN-001",
  "annotation_status": "CONCEPT_SAMPLE",
  "semantic_elements": [
    {"element_id": "SYN-001:E001", "type": "PERSON_GROUP", "label": "family"},
    {"element_id": "SYN-001:E002", "type": "ACTION", "label": "playing basketball"}
  ],
  "media_units": [
    {"unit_id": "SYN-001:C001", "source_clip_id": 1, "start_ms": 2000, "end_ms": 4000}
  ],
  "relations": [
    {
      "relation_id": "SYN-001:R001",
      "subject": "SYN-001:E001",
      "predicate": "PERFORMS",
      "object": "SYN-001:E002"
    }
  ]
}
```

## 5.5 원본과 확장의 분리

QVHighlights 원본 annotation에 임의 필드를 추가하지 않고, qid를 키로 사용하는 `etri_semantic_extension.jsonl`을 별도 관리한다. 이 방식은 다음 장점을 갖는다.

- 외부 annotation의 출처와 변환 여부를 명확히 구분한다.
- QVHighlights와 ETRI 자체 정답의 라이선스 범위를 분리한다.
- element·relation schema를 독립적으로 버전 관리한다.
- 외부 데이터셋을 교체해도 확장 구조를 유지한다.

# 6. 평가지표 체계

## 6.1 지표 구성

| 범주 | 대표 지표 | 평가 대상 |
|---|---|---|
| Moment Retrieval | tIoU, MR-mAP, R@1 | query 대비 관련 시간 구간 |
| Highlight | HL-mAP, HL-Hit@1 | 2초 클립 중요도 |
| Element | Precision, Recall, F1 | 인물·행위·사건 등 |
| Relation | Triple F1, Integrity | subject-predicate-object |
| Reassembly | Coverage, Chronology Violation | 선택 단위·순서 |
| Consistency | Repeated Output Agreement | 동일 환경 반복 출력 |
| Reproducibility | Cross-environment Deviation | 환경·버전 간 편차 |
| Performance | Stage Latency, Throughput | 분석·전송·재조립·재생 |
| Interface | Conformance, Error Recovery | ETRI 연동 계약 |

## 6.2 구간 지표

temporal IoU는 예측 구간과 정답 구간의 교집합 길이를 합집합 길이로 나눈 값이다. MR-mAP은 예측 구간을 신뢰도 순으로 정렬하고 tIoU 임계값별 Average Precision을 계산한 후 query 전체를 평균한다. QVHighlights 참조 평가와 일관되게 tIoU 0.50~0.95 구간을 0.05 간격으로 사용한다.

R@1은 가장 높은 점수의 예측 구간이 정답 구간에 적중한 질의의 비율이다. 본 지표 체계는 tIoU 0.5와 0.7을 대표값으로 보고한다.

## 6.3 하이라이트 지표

각 2초 클립에 대한 예측 중요도를 세 명의 평가자 점수와 비교한다. 점수 2, 3, 4 이상을 각각 Fair, Good, VeryGood positive로 변환하여 AP를 산출한다. Hit@1은 시스템이 가장 중요하다고 예측한 클립이 어느 한 평가자에게라도 positive인 query의 비율을 의미한다.

## 6.4 element·relation 지표

Element F1은 type, 표준화된 label, 시간 구간 일치를 조합한 matching 규칙을 사용한다. Relation F1은 subject·predicate·object 삼중항을 비교한다. 연말 단계에서는 유의어, 동일 인물·객체, 복수 표현, 부분 구간 일치를 처리하는 annotation guideline을 합의해야 한다.

Relation Integrity는 정확도가 아니라 구조 타당성 검사이다. relation의 subject와 object가 선언된 element 또는 media unit이고 predicate가 허용 사전에 있는지를 검사한다.

## 6.5 판정 기준

보고 단계에서는 지표의 의미, 입력, 산식, 출력 형식까지 정의하고 합격 기준값은 확정하지 않았다. 기준값은 ETRI 대상 시스템의 개발 단계, baseline, 표본 수, 용도를 고려하여 사전 합의해야 한다.

<!-- PAGEBREAK -->

# 7. 검증시스템 참조 구현

## 7.1 구현 범위

현 참조 구현은 Python 3.10 이상의 표준 라이브러리만 사용한다. 멀티모달 모델, 미디어 codec, GPU dependency를 제외하여 데이터·평가 구조를 독립적으로 검증할 수 있게 했다.

구현된 기능은 다음과 같다.

- JSONL 입력·출력
- QVHighlights 호환 필수 필드·값 범위 검사
- qid 중복·window duration 초과·saliency 길이 불일치 검사
- 정답 파생 Mock moment·saliency prediction 생성
- temporal IoU, MR-mAP, R@1 계산
- 임계값별 HL-mAP, HL-Hit@1 계산
- relation node·predicate integrity 검사
- 예측 moment를 2초 media unit으로 변환한 reassembly plan 생성
- PRELIMINARY_MOCK 면책 문구가 포함된 결과 JSON 생성

## 7.2 Mock 예측의 목적

Mock predictor는 정답 구간의 시작·종료를 소폭 변경하고 정답 saliency의 평균을 예측 점수로 변환한다. 따라서 높은 수치가 생성되는 것은 예상된 동작이며, 실제 모델 성능을 대표하지 않는다. Mock의 목적은 다음에 한정된다.

1. annotation에서 prediction으로의 필드 변환 확인
2. evaluator가 예측 구조를 읽고 지표를 생성하는지 확인
3. 예측 구간이 reassembly plan으로 변환되는지 확인
4. Mock 상태와 면책 문구가 결과물에 남는지 확인

## 7.3 실행 방법

```powershell
./run_demo.ps1
./run_tests.ps1
```

데모 실행 결과로 `mock_predictions.jsonl`, `reassembly_plans.jsonl`, `preliminary_evaluation.json`이 생성된다. 생성 폴더는 Git 납품 소스에서 제외했으며, 재실행하여 재생성할 수 있다.

## 7.4 시험 결과

Python 문법 검사, JSON 파싱, 단위시험, 데모 실행을 수행했다.

| 검사 | 결과 |
|---|---|
| Python compileall | PASS |
| JSON configuration/schema parse | 7 files PASS |
| Dataset adapter test | PASS |
| temporal IoU tests | PASS |
| Preliminary demo end-to-end test | PASS |
| Relation integrity fixture | 17/17 valid |

단위시험 4건이 통과했다. 이 통과는 코드·스키마 흐름의 기술적 정상 여부만 의미하며 ETRI 시스템 합격 판정이 아니다.

# 8. 시험 시나리오 및 검증 절차

## 8.1 현 단계 사전검증

| ID | 내용 | 판정 근거 |
|---|---|---|
| TC-001 | QVHighlights 호환 JSONL 로드 | 3건 변환, qid 유일 |
| TC-002 | 입력 window·score 범위 검사 | 잘못된 입력 거부 |
| TC-003 | Mock prediction 생성 | result_status·metadata 포함 |
| TC-004 | Moment metrics | threshold별 MR-mAP·R@1 생성 |
| TC-005 | Highlight metrics | Fair·Good·VeryGood 결과 생성 |
| TC-006 | Relation integrity | 17 relation node·predicate 검사 |
| TC-007 | Reassembly plan | 시간순·중복 제거 clip 생성 |
| TC-008 | Mock 면책 | 결과 JSON에 실제 성능이 아님을 명시 |

## 8.2 연말 실제 시나리오

연말에는 다음 범주의 시험을 추가한다.

- 비디오·음성·텍스트 중간 출력 수집
- element 추출 정확도·시간 정렬
- relation 정확도·구조 정합성
- element-전송 단위 연결·페이로드 정합성
- 요구 기반 재조립·시간 순서·중복 제거
- 재생 연속성·A/V sync·codec 호환성
- 일관성·재현성·단계별 latency·throughput
- 비정상 입력·timeout·일부 단계 실패 복구

## 8.3 검증 절차

1. **범위 동결:** 대상 시스템, 모델, 데이터, 설정 버전을 확정한다.
2. **권리 확인:** dataset, 영상, 모델, 코드의 사용·복제·납품 범위를 확인한다.
3. **환경 기록:** OS, CPU, GPU, driver, codec, library, container version을 기록한다.
4. **입력 고정:** qid·vid·query·annotation hash를 기록한다.
5. **동일 입력 실행:** 참조 검증시스템과 ETRI 대상 시스템에 동일 입력을 제공한다.
6. **단계별 수집:** 분석, 전송, 재조립, 재생 출력·로그·시각을 수집한다.
7. **정규화·평가:** 공통 Prediction으로 변환하고 지표를 산출한다.
8. **판정:** 합의된 기준으로 PASS, FAIL, CONDITIONAL_PASS, NOT_TESTED, EXCLUDED를 부여한다.
9. **이슈 관리:** 재현 절차, 원인, 조치, 재시험 결과를 연결한다.
10. **입회 확인:** ETRI 담당자와 시나리오·결과·제외·잔여 이슈를 확인한다.

## 8.4 증빙 패키지

```text
evidence/{execution_id}/
├─ environment.json
├─ input_manifest.json
├─ source_output/
├─ normalized_predictions.jsonl
├─ metrics.json
├─ logs/
├─ screenshots/
├─ issues.csv
└─ attendance_record.pdf
```

# 9. 사전검증 결과

## 9.1 실행 조건

| 항목 | 값 |
|---|---|
| 데이터 | 자체 작성 QVHighlights 호환 합성 3건 |
| 미디어 원본 | 포함하지 않음 |
| element extension | 수작 CONCEPT_SAMPLE 3건 |
| relation | 17건 |
| predictor | ReferenceMockPredictor |
| predictor 특성 | 정답 moment·saliency 파생 |
| 결과 상태 | PRELIMINARY_MOCK |

## 9.2 지표 출력

| 지표 | 사전검증 값 | 해석 |
|---|---:|---|
| MR-mAP@0.50:0.95 | 91.6667 | 정답 파생 Mock의 흐름 확인값 |
| MR-R1@0.50 | 100.0000 | 정답 파생 Mock의 흐름 확인값 |
| MR-R1@0.70 | 100.0000 | 정답 파생 Mock의 흐름 확인값 |
| HL-mAP Fair | 100.0000 | 정답 평균 사용에 따른 Mock 값 |
| HL-mAP Good | 99.0741 | 정답 평균 사용에 따른 Mock 값 |
| HL-mAP VeryGood | 83.3333 | 정답 평균 사용에 따른 Mock 값 |
| Relation Integrity | 100.0000 | 작성된 17 relation의 node·predicate 유효 |

## 9.3 결과 해석

상기 수치는 정답으로부터 Mock 예측을 생성하였으므로 높게 나오도록 설계되었다. 따라서 값의 대소를 통해 시스템 품질을 판단하면 안 된다. 현 단계에서 확인된 것은 다음과 같다.

- annotation을 prediction 스키마로 변환할 수 있다.
- prediction에서 moment·highlight 지표를 생성할 수 있다.
- prediction moment를 순서화된 media unit 목록으로 변환할 수 있다.
- extension relation의 미선언 node·알 수 없는 predicate를 탐지할 수 있다.
- 모든 결과에 Mock 상태와 실제 성능이 아님을 나타낼 수 있다.

## 9.4 미수행 항목

| 항목 | 상태 | 선행 조건 |
|---|---|---|
| 실제 멀티모달 추론 | NOT_TESTED | 모델·가중치·입력 파이프라인 확정 |
| 실제 QVHighlights 평가 | NOT_TESTED | 사용 승인·데이터 취득 |
| Element/Relation F1 | NOT_TESTED | 수작 정답·matching guideline |
| 미디어 실제 재조립 | NOT_TESTED | codec·FFmpeg·출력 계약 |
| ETRI 시스템 연동 | NOT_TESTED | API·전송 규격·접근 환경 |
| 성능 측정 | NOT_TESTED | 실제 구현·하드웨어 고정 |
| 상호 입회 판정 | NOT_TESTED | ETRI 시험 일정·기준 합의 |

# 10. ETRI 대상 실제 검증 계획

## 10.1 연동 준비 항목

ETRI 대상 시스템 실제 검증을 위해 최소한 다음 정보가 필요하다.

- 입력 비디오·음성·텍스트 형식
- query 표현 방식·인코딩·언어
- element·relation 출력 스키마
- element-전송 단위 연결 표현
- 분석·전송·재조립·재생 단계별 상태·오류코드
- API, directory exchange, message queue, packet trace 중 연동 방식
- timeout, retry, 부분 응답, 순서 보장 규칙
- 접근 권한·보안·로그 반출 규칙

## 10.2 실제 검증 출력 계약

```json
{
  "execution_id": "RUN-20261201-001",
  "result_status": "ETRI_SYSTEM_OUTPUT",
  "system_version": "TBD",
  "model_version": "TBD",
  "qid": "TBD",
  "vid": "TBD",
  "pred_relevant_windows": [],
  "pred_saliency_scores": [],
  "semantic_elements": [],
  "relations": [],
  "stage_timings_ms": {},
  "errors": [],
  "provenance": {}
}
```

## 10.3 상호 입회

검증 당일에는 시험 일시, 장소, 참석자, 시스템·모델·데이터 버전, 환경, 시나리오별 입력·기대결과·실제결과·판정, 이슈, 후속 조치를 회의록으로 남긴다. 실제 결과는 ETRI 담당자 확인 전에 `JOINT_VERIFIED`로 변경하지 않는다.

<!-- PAGEBREAK -->

# 11. 오픈소스·데이터·라이선스 관리

## 11.1 현 납품 사용 현황

현 참조 구현은 Python 표준 라이브러리만 사용한다. QVHighlights, Moment-DETR, PyTorch, FFmpeg, 멀티모달 모델 코드·가중치는 현 납품본에 포함되지 않았다.

| 상태 | 항목 | 용도 | 조치 |
|---|---|---|---|
| USED | Python | 참조 구현 실행 | 표준 라이브러리만 사용 |
| REFERENCE | QVHighlights | 스키마·평가 구조 참조 | 원본 미포함, 사전 협의 필요 |
| REFERENCE | Moment-DETR | 공식 출력·평가 방식 참조 | 코드 미복사 |
| PLANNED | PyTorch | 연말 모델 추론 | 버전·라이선스 협의 |
| PLANNED | FFmpeg | 미디어 분할·재조립 | 빌드·코덱 조건 협의 |
| PLANNED | Multimodal Model | element 추출 | 코드·가중치·학습데이터 검토 |

## 11.2 관리 항목

외부 자원별로 명칭, 버전, 사용 목적, URL, 라이선스, 수정 여부, 소스 공개 의무, 고지 의무, 특허 조항, 배포 여부, 협의 상태를 기록한다. 정식 구현에서는 SBOM을 생성하고 실제 배포 파일과 사용내역을 대조한다.

## 11.3 관리 절차

1. 도입 후보의 라이선스·특허·재배포 조건을 검토한다.
2. ETRI와 사용 범위를 사전 협의한다.
3. 버전을 고정하고 취득 URL·hash·일자를 기록한다.
4. 소스·이진·모델·데이터 등 대상별 의무를 분리한다.
5. Third-Party Notices·license text·출처 표시를 납품본에 반영한다.
6. 발주기관이 요구하는 라이선스 검증 서비스를 납기 최소 7일 전에 신청한다.

## 11.4 QVHighlights 권장 사용 방식

유상 용역 결과물에 QVHighlights 원본 영상·annotation을 그대로 넣지 않는다. 납품 코드에는 다운로드 경로·adapter·스키마만 제공하고, ETRI가 승인한 환경에서 데이터를 취득하여 평가한다. 협의 결과 사용이 곤란한 경우 자체 영상·annotation 또는 사용 조건이 적합한 대체 dataset으로 교체한다.

# 12. 품질·보안·재현성 관리

## 12.1 품질 관리

- JSON Schema로 입출력 필수 필드·형식을 관리한다.
- 단위시험·통합시험·샘플 실행을 버전별로 수행한다.
- 평가 코드에 고정 예제를 유지하여 지표 산식 변경을 탐지한다.
- 결과 상태·면책 문구를 필수 필드로 검사한다.
- 보고서 표와 JSON 결과가 일치하는지 확인한다.

## 12.2 재현성

각 실행에 코드 commit, 설정 hash, 데이터 hash, 모델 ID, 환경 ID, 시작·종료 시각, random seed, 실행 ID를 기록한다. 외부 데이터를 납품본에 포함할 수 없는 경우 취득 절차와 예상 hash를 기록한다.

## 12.3 보안

- 원본 미디어를 로그·오류 메시지에 직접 저장하지 않는다.
- 파일 경로, 인증정보, 내부 URL, 개인정보를 결과 반출 전에 점검한다.
- 입력·출력 디렉터리 권한을 분리하고 반출 시 hash를 확인한다.
- 외부 모델·코드 다운로드는 승인된 URL·버전으로 제한한다.
- 시험 장비와 개인용 저장장치의 반입·반출 규칙을 준수한다.

## 12.4 주요 위험과 대응

| 위험 | 영향 | 대응 |
|---|---|---|
| QVHighlights 사용 조건 미합의 | 실제 평가 지연 | 사전 협의, 대체 dataset·자체 정답 준비 |
| ETRI 출력 계약 변경 | adapter 재작업 | 공통 Prediction 경계 유지, contract test |
| element matching 애매성 | F1 신뢰도 저하 | guideline·복수 annotation·합의 |
| Mock 결과의 오인 | 성능 과장 | result status·면책 필수, 보고서 분리 |
| 미디어 codec 불일치 | 재조립·재생 실패 | 코덱 매트릭스, 사전 transcode 정책 |
| 모델 라이선스 미확인 | 납품 제한 | 가중치·학습데이터까지 사전 검토 |

# 13. 유지보수 및 기술이전

## 13.1 유지보수 범위

코드, 설정, JSON Schema, 시험 자료, 보고서 원문을 동일 Git 저장소에서 관리한다. 하자보수 기간의 상세 범위와 응답 수준은 계약서를 따르되, 최소한 다음을 이스 단위로 관리한다.

- 납품 버전에서 재현되는 입출력·지표 오류
- 문서와 코드 계약의 불일치
- 승인된 환경에서의 설치·실행 오류
- ETRI adapter의 합의된 프로토콜 적합성
- 라이선스 고지 누락·사용내역 불일치

## 13.2 기술이전 자료

| 자료 | 목적 |
|---|---|
| README | 납품물 구조·실행·현 범위 안내 |
| 시스템 설계서 | 모듈 책임·연동 경계 |
| 데이터 모델 | element·relation·media unit schema |
| 평가지표 정의서 | 지표 입력·산식·해석 |
| 시험 시나리오·절차 | 재시험·입회 기준 |
| QVHighlights 적용서 | 데이터 매핑·제약·라이선스 |
| 오픈소스 사용내역 | 제3자 자원 현황·후속 검토 |
| 연말 로드맵 | 실제 동작 구현 단계 |

## 13.3 권장 기술이전 세션

1. 저장소·납품 구조 안내
2. QVHighlights annotation·prediction 구조 설명
3. ETRI semantic extension 스키마 설명
4. 사전검증 데모·단위시험 실행
5. 지표 JSON 해석·Mock 결과 구분
6. EtriSystemAdapter 구현 포인트 설명
7. 실제 검증 증빙·입회 절차 설명
8. 오픈소스·데이터셋 도입 승인 절차 설명

# 14. 연말 동작 시스템 구현 로드맵

## 14.1 1단계 - 연동·데이터 계약 확정

ETRI 대상 시스템의 입력, 중간 출력, 최종 출력, 오류, timestamp, 인증, 로그 반출 규칙을 확정한다. contract test를 작성하여 ETRI 버전 변경을 탐지한다.

## 14.2 2단계 - dataset·정답 확정

QVHighlights 사용 가능 여부를 확정하고 관련 query·video subset을 선정한다. 사용이 곤란한 경우 자체 영상·query·moment·saliency를 구축한다. 대표 표본에 element·relation 수작 정답을 부여한다.

## 14.3 3단계 - 멀티모달 분석

비주얼 encoder, ASR, OCR, 음향 인식을 adapter로 분리한다. 각 모달리티의 출력을 element 후보로 변환하고 중복·동일 객체를 병합한다. 규칙·모델 기반으로 relation을 생성하고 모든 출력에 provenance를 부여한다.

## 14.4 4단계 - 전송 단위·재조립

element의 media unit reference를 이용하여 query에 필요한 단위를 선정한다. 중요도, 시간 순서, 중복, codec, 가용 길이, 전송 제약을 반영하여 assembly manifest를 생성한다. 승인된 미디어 도구로 재조립하고 재생 연속성을 검사한다.

## 14.5 5단계 - ETRI 실제 검증

참조 검증시스템과 ETRI 대상 시스템에 동일 입력을 제공한다. 공통 Prediction 계약으로 출력을 수집하고 moment, highlight, element, relation, reassembly, consistency, performance를 평가한다. ETRI-용역기관 상호 입회 하에 시나리오별 판정·이슈·잔여 조치를 확정한다.

## 14.6 연말 완료 기준

- 승인된 데이터셋으로 최소 1개 end-to-end 시나리오가 실제 실행된다.
- 분석·전송·재조립·재생 단계의 출력과 시각이 하나의 execution ID로 연결된다.
- 실제 ETRI 출력과 Mock 출력이 저장 경로·상태·보고서에서 분리된다.
- 사용된 모든 dataset·model·code·tool의 사전 협의·고지·SBOM이 완료된다.
- 시험 결과, 로그, 증빙, 환경 명세, 회의록이 최종 보고서와 연결된다.

<!-- PAGEBREAK -->

# 15. 결론

본 연구는 QVHighlights의 query·moment·clip·saliency 구조를 시맨틱 미디어 전송 검증에 적용하고, 원본에 부족한 element·relation·media unit·assembly plan을 ETRI extension으로 분리하는 구조를 제시했다. 이를 바탕으로 dataset adapter, Prediction 계약, moment·highlight 평가, relation integrity, reassembly planner, ETRI adapter interface로 구성된 참조 코드를 작성했다.

보고 단계의 합성 샘플·Mock 결과를 이용하여 입력, 정규화, 예측, 평가, 재조립 계획, 결과 JSON의 연결 가능성을 확인했다. 사전검증 수치는 실제 성능으로 해석하지 않도록 코드·JSON·보고서에 PRELIMINARY_MOCK 상태와 면책을 부여했다.

연말 동작 시스템으로의 전환에서 가장 중요한 선행 과제는 다음 네 가지이다.

1. QVHighlights 또는 대체 dataset의 실제 사용 범위와 라이선스 협의
2. ETRI 대상 시스템의 입출력·전송·오류 계약 확정
3. element·relation 정답과 matching guideline 구축
4. 상호 입회 시험의 표본·합격 기준·증빙 항목 합의

이 사항을 확정한 후 현 저장소의 adapter·schema·metric·test 구조에 실제 모델과 ETRI 연동을 추가하면 보고 단계 결과물을 연말 운영 가능한 검증시스템으로 발전시킬 수 있다.

# 부록 A. 납품 파일 구조

```text
etri_semantic_media_verification/
├─ README.md
├─ PROPRIETARY_NOTICE.md
├─ pyproject.toml
├─ run_demo.ps1
├─ run_tests.ps1
├─ config/
│  ├─ datasets.json
│  ├─ metrics.json
│  └─ relation_types.json
├─ schemas/
│  ├─ qvhighlights.schema.json
│  ├─ semantic_extension.schema.json
│  ├─ prediction.schema.json
│  └─ evaluation_result.schema.json
├─ src/semantic_validator/
├─ samples/
├─ tests/
├─ docs/
├─ licenses/
└─ deliverables/
```

# 부록 B. 주요 상태·용어

| 용어 | 정의 |
|---|---|
| Semantic Element | 미디어에서 식별된 인물·객체·행위·사건·주제 등의 의미 단위 |
| Media Unit | 전송·선택·재조립이 가능한 시간·페이로드 단위 |
| Moment Retrieval | 자연어 query에 관련된 비디오 시간 구간을 찾는 작업 |
| Highlight Detection | query에 대한 클립별 중요도를 예측하는 작업 |
| Reassembly | 선택된 media unit을 정책·시간 순서에 따라 재구성하는 작업 |
| Reference Annotation | 평가의 정답으로 사용하는 검수된 annotation |
| Mock Prediction | 데이터·코드 흐름 확인을 위해 생성한 모의 출력 |
| Provenance | 데이터·모델·변환·실행의 출처와 이력 |

# 부록 C. 참고자료

1. QVHighlights dataset structure: https://github.com/jayleicn/moment_detr/blob/main/data/README.md
2. QVHighlights evaluation format: https://github.com/jayleicn/moment_detr/blob/main/standalone_eval/README.md
3. QVHighlights reference evaluation code: https://github.com/jayleicn/moment_detr/blob/main/standalone_eval/eval.py
4. QVHighlights paper: https://arxiv.org/abs/2107.09609
5. Moment-DETR repository and license notice: https://github.com/jayleicn/moment_detr
6. Creative Commons BY-NC-SA 4.0: https://creativecommons.org/licenses/by-nc-sa/4.0/

# 부록 D. 현 단계 최종 확인 체크리스트

- 완료: 과업 8개 항목을 보고서·코드·부속 문서에 매핑
- 완료: QVHighlights 호환 스키마·샘플·adapter 작성
- 완료: 시맨틱 element·relation·media unit 확장 모델 작성
- 완료: Moment·Highlight·Relation Integrity 참조 평가기 작성
- 완료: Mock 결과의 상태·면책 표시
- 완료: 단위시험·JSON 파싱·데모 실행 확인
- 완료: 시험 시나리오·검증 절차·증빙 구조 작성
- 완료: 오픈소스·데이터셋 사용내역·고지 작성
- 완료: 연말 실제 구현·ETRI 연동 로드맵 작성
- 미완료: QVHighlights 실제 사용 승인·데이터 취득
- 미완료: 멀티모달 모델·미디어 재조립 구현
- 미완료: ETRI 대상 시스템 실제 연동·입회 검증
