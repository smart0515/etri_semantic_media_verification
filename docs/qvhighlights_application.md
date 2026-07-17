# QVHighlights 적용 방안

## 1. 적용 목적

QVHighlights의 query-moment-clip-saliency 구조를 시맨틱 미디어 전송 검증의 공통 입력 모델로 사용한다. query 기반 구간 검색과 하이라이트 평가를 동일 annotation에서 수행할 수 있어 검증시스템의 구간·중요도 계층을 구성하기 적합하다.

## 2. 원본 필드 매핑

| QVHighlights 필드 | 검증 의미 | 확장 대상 |
|---|---|---|
| `qid` | 요구 식별자 | SemanticRequest ID |
| `query` | 선택 조건 | 자연어 의미 조건 |
| `duration` | 시간 경계 | MediaAsset duration |
| `vid` | 미디어 참조 | asset·stream ID |
| `relevant_windows` | 정답 구간 | element 활성 구간 |
| `relevant_clip_ids` | 2초 단위 | MediaUnit |
| `saliency_scores` | 중요도 정답 | 전송 우선순위 |

## 3. 시맨틱 확장

원본 annotation과 별도의 extension JSONL을 `qid`로 연결한다. 확장 파일은 인물, 객체, 행위, 사건, 장소, 주제, 텍스트와 음향 element, media unit 및 시간·공간·서사·인과 relation을 표현한다.

이 분리 구조는 원본 데이터의 출처와 권리를 유지하면서 ETRI 과업의 시맨틱 구조를 독립적으로 관리할 수 있게 한다.

## 4. Prediction 계약

```json
{
  "qid": "QVH-REF-001",
  "query": "family playing basketball",
  "vid": "reference_video_001",
  "pred_relevant_windows": [[2.25, 9.75, 0.95]],
  "pred_saliency_scores": [0.0, 3.3, 3.67, 3.0],
  "result_status": "VERIFIED_REFERENCE"
}
```

## 5. 데이터 관리

- 외부 데이터셋 원본은 검증 코드와 분리한다.
- 원본 데이터와 신규 작성 extension의 출처를 provenance로 구분한다.
- 영상은 URL 대신 내부 asset ID, timestamp와 hash로 참조한다.
- 이용 조건에 맞는 데이터만 실행 프로파일에 등록한다.
- `samples/`에는 외부 원본을 복사하지 않고 구조 호환 참조 데이터만 포함한다.
