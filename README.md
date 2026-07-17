# ETRI 시맨틱 미디어 검증시스템

본 저장소는 **"의미 기반 미디어 전송 검증시스템 및 멀티모달 시맨틱 미디어 구조 연구"** 용역의 보고용 납품 패키지이다.

현 버전(`v0.1.0-report`) 범위는 다음과 같다.

- QVHighlights 호환 annotation을 활용한 검증 데이터 구조
- 시맨틱 element·관계·미디어 전송 단위 확장 모델
- 대상 시스템 연동을 위한 adapter 인터페이스
- 구간 검색, 하이라이트, 관계 정합성 평가 구조
- QVHighlights 호환 **자체 작성 합성 샘플**을 이용한 사전검증 데모
- 연말 실제 동작 시스템으로 확장하기 위한 로드맵

> **중요:** 현 버전의 출력은 설계·데이터 흐름·평가 산식을 확인하기 위한 `PRELIMINARY_MOCK` 결과이다. ETRI 대상 시스템의 실제 성능 측정값이 아니다.

## 납품물

| 구분 | 경로 | 내용 |
|---|---|---|
| 용역결과보고서 | `deliverables/ETRI_시맨틱_미디어_용역결과보고서.pdf` | 과업 결과, 설계, 평가체계, 시험절차, 로드맵 |
| 보고서 원문 | `docs/final_report.md` | PDF의 편집 가능한 Markdown 원문 |
| 검증시스템 1식 | `src/`, `schemas/`, `config/`, `samples/`, `tests/` | 코드, 스키마, 설정, 샘플, 시험 |
| 설계·시험 문서 | `docs/` | 시스템 설계, 지표 정의, 시나리오, 검증 절차 |
| 오픈소스 관리 | `licenses/` | 사용·참조·도입예정 항목 및 고지 |

## 시스템 구조

```text
QVHighlights-compatible annotation
            |
            v
      Dataset Adapter
            |
            v
 Common Verification Model <--- Semantic Element Extension
            |
            +-- Moment/Highlight Evaluator
            +-- Relation Integrity Evaluator
            +-- Reassembly Planner
            |
            v
  Preliminary Result JSON

ETRI System Adapter (interface only in v0.1.0-report)
            |
            +------> 연말 실제 연동
```

## 사전검증 데모

현 데모는 Python 표준 라이브러리만 사용한다. QVHighlights 원본이 아닌 자체 작성 합성 샘플을 읽고 Mock 예측과 평가 결과를 생성한다.

```powershell
./run_demo.ps1
```

또는:

```powershell
$env:PYTHONPATH = "src"
python -m semantic_validator.cli demo --output-dir artifacts/demo
```

생성 파일:

```text
artifacts/demo/
├─ mock_predictions.jsonl
├─ reassembly_plans.jsonl
└─ preliminary_evaluation.json
```

## 시험

```powershell
./run_tests.ps1
```

## QVHighlights 적용 방식

- 외부 데이터셋 원본은 본 저장소에 포함하지 않는다.
- `samples/qvhighlights_compatible_sample.jsonl`은 스키마 검증을 위한 자체 작성 합성 데이터이다.
- 실제 데이터 사용 시 `qid`, `query`, `duration`, `vid`, `relevant_windows`, `relevant_clip_ids`, `saliency_scores`를 공통 모델로 변환한다.
- QVHighlights annotation은 CC BY-NC-SA 4.0이므로 유상 용역 내 원본 사용·재배포 여부를 ETRI와 사전 협의해야 한다.

상세 내용은 [`docs/qvhighlights_application.md`](docs/qvhighlights_application.md)를 참조한다.

## 현 버전과 연말 버전 구분

| 항목 | 현 보고용 버전 | 연말 동작 버전 |
|---|---|---|
| 데이터 | 합성 샘플 | 승인된 QVHighlights 또는 ETRI 데이터 |
| element 추출 | Seed 정의 로드 | 멀티모달 모델 추론 |
| 관계 생성 | annotation 로드 | 규칙+모델 기반 생성 |
| 대상 시스템 | interface만 제공 | API/파일 연동 |
| 평가 | Mock 출력 사전검증 | 실제 출력 비교검증 |
| 성능 | 미측정 | 지연시간·처리량 측정 |

## 권리 및 이용

본 저장소의 신규 작성 코드와 문서는 해당 용역 계약의 권리 귀속 조건을 따른다. 제3자 데이터·소프트웨어의 권리는 각 출처와 라이선스에 따른다. 자세한 사항은 `PROPRIETARY_NOTICE.md`와 `licenses/` 폴더를 참조한다.

