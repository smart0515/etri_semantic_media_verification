# 시맨틱 element 관계 구조 데이터 모델

## 1. 모델 구성

본 모델은 네 가지 핵심 엔티티를 갖는다.

| 엔티티 | 설명 | 주요 속성 |
|---|---|---|
| SemanticRequest | 사용자의 자연어 요구 | qid, text, request_type |
| SemanticElement | 인물·객체·행위·사건·주제·상황 | element_id, type, label, confidence |
| MediaUnit | 전송·재조립이 가능한 미디어 단위 | unit_id, media_id, start_ms, end_ms |
| Relation | element와 media unit 사이의 관계 | subject, predicate, object, confidence |

## 2. element 유형

- `PERSON`, `PERSON_GROUP`: 인물 또는 인물 그룹
- `OBJECT`: 구체적 사물
- `ACTION`: 시간 구간을 갖는 행위
- `EVENT`: 여러 element를 포함하는 사건
- `PLACE`: 장소·공간
- `TOPIC`: 주제·개념
- `SITUATION`: 상황·분위기·맥락
- `TEXT`: 자막·화면 문자열
- `AUDIO_EVENT`: 발화·음향·환경음

## 3. 관계 분류

| 분류 | predicate 예시 | 활용 |
|---|---|---|
| 시간 | TEMPORALLY_BEFORE, AFTER, OVERLAPS | 재조립 순서, 이벤트 연결 |
| 공간 | OCCURS_AT, SPATIALLY_NEAR | 장소 기반 선택 |
| 서사 | HAS_TOPIC, HAS_PARTICIPANT | 사건·주제 재구성 |
| 행위 | PERFORMS, PARTICIPATES_IN | 주체-행위 연결 |
| 인과 | CAUSES | 원인-결과 맥락 |
| 미디어 | EVIDENCE_OF, DESCRIBED_BY | element-실제 데이터 연결 |
| 출처 | DERIVED_FROM | 추적성·재현성 |

## 4. QVHighlights 매핑

| QVHighlights | 공통 모델 |
|---|---|
| `qid`, `query` | SemanticRequest |
| `vid`, `duration` | MediaAsset |
| `relevant_windows` | Reference Moment |
| `relevant_clip_ids` | MediaUnit |
| `saliency_scores` | MediaUnit.reference_saliency |

QVHighlights에 없는 SemanticElement과 Relation은 별도 extension JSONL에 저장한다. 원본 annotation을 변경하지 않으므로 출처·라이선스·변환 이력을 명확히 분리할 수 있다.

## 5. ID 규칙

```text
qid                 SYN-001
element_id          SYN-001:E001
media unit ID       SYN-001:C001
relation ID         SYN-001:R001
test execution ID   TC-001:RUN-20261201-001
```

## 6. 확장 원칙

- 스키마는 `schema_version`으로 버전 관리한다.
- 알 수 없는 실제 추론값은 `null`로 표현하며 임의 신뢰도를 기재하지 않는다.
- 모델 출력에는 `model_version`, `confidence`, `generated_at`을 추가한다.
- 수작 annotation에는 `annotator_id`, `guideline_version`, `review_status`를 추가한다.
- 연말 전송 프로토콜 확정 시 `transport_unit_id`, `payload_offset`, `codec`, `stream_id`를 MediaUnit에 추가한다.
