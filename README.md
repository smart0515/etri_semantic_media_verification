# ETRI 시맨틱 미디어 검증시스템

본 저장소는 **의미 기반 미디어 전송 검증시스템 및 멀티모달 시맨틱 미디어 구조 연구** 용역의 최종 납품 패키지이다. 시스템 설계, 평가지표, 참조 구현, 시험 절차, 결과 보고서, 시맨틱 element 관계 모델 및 오픈소스 관리 자료를 하나의 버전으로 구성하였다.

## 납품 구성

| 구분 | 경로 | 주요 내용 |
|---|---|---|
| 용역결과보고서 | `deliverables/ETRI_시맨틱_미디어_용역결과보고서.docx` | 과업 수행 방법과 검증 결과를 정리한 Word 보고서 |
| 보고서 원문 | `docs/final_report.md` | 편집 가능한 Markdown 원문 |
| 검증시스템 | `src/semantic_validator/` | 데이터 변환, 평가, 관계 검증, 재조립 계획 |
| 데이터 계약 | `schemas/`, `config/` | JSON Schema, 지표 및 관계 유형 설정 |
| 검증 데이터 | `samples/` | QVHighlights 구조 호환 참조 데이터 |
| 시험 코드 | `tests/` | adapter, 지표, 통합 실행 단위시험 |
| 설계·시험 문서 | `docs/` | 시스템 설계, 지표 정의, 시험 시나리오, 검증 절차 |
| 라이선스 관리 | `licenses/` | 사용·참조 항목과 제3자 고지 |

## 구현 기능

- QVHighlights 형식의 `qid`, `query`, `duration`, `vid`, 구간 및 중요도 정답 로드
- 공통 annotation 및 prediction 데이터 계약 검증
- Moment Retrieval의 tIoU, MR-mAP, R@1 계산
- Highlight Detection의 mAP, Hit@1 계산
- element 유형·정규화 label·시간 tIoU 기반 Precision·Recall·F1 계산
- 매칭된 node 기반 relation 삼중항 Precision·Recall·F1 계산
- 시맨틱 element, media unit, relation 구조 및 무결성 검사
- 선택 구간과 media unit 기반 재조립 계획 생성
- 대상 시스템 출력을 공통 Prediction 계약으로 변환하는 adapter 경계
- 실행 결과와 지표를 JSON/JSONL 증빙 파일로 저장

## 아키텍처

```text
QVHighlights-compatible Dataset / ETRI Annotation
                         |
                         v
                  Dataset Adapter
                         |
                         v
       Common Annotation + Semantic Extension
                         |
         +---------------+---------------+
         |               |               |
         v               v               v
   Reference Adapter  ETRI Adapter   Relation Model
         |               |               |
         +---------------+---------------+
                         |
                         v
 Moment / Highlight / Relation / Reassembly Evaluators
                         |
                         v
             Evaluation Result + Evidence
```

## 실행

Python 3.10 이상에서 별도 런타임 의존성 없이 참조 검증 프로파일을 실행할 수 있다.

```powershell
./run_demo.ps1
```

또는:

```powershell
$env:PYTHONPATH = "src"
python -m semantic_validator.cli demo --output-dir artifacts/demo
```

생성 결과:

```text
artifacts/demo/
├─ predictions.jsonl
├─ reassembly_plans.jsonl
└─ evaluation_result.json
```

## 시험

```powershell
./run_tests.ps1
```

기본 납품 시험은 데이터 adapter, 구간 지표, 통합 실행, 결과 상태 및 증빙 파일 생성을 검사한다.

`python.exe`가 기본 경로에 없으면 `ETRI_PYTHON` 환경변수에 Python 실행 파일 경로를 지정할 수 있다.

## Word 보고서 재생성

Word가 설치된 Windows 환경에서 다음 순서로 최종 보고서를 재생성하고 구조를 점검한다.

```powershell
python tools/build_report_docx.py
$report = (Resolve-Path "deliverables/ETRI_시맨틱_미디어_용역결과보고서.docx").Path
powershell -ExecutionPolicy Bypass -File tools/finalize_report_word.ps1 -DocumentPath $report
python tools/audit_report_docx.py
```

## 참조 검증 결과

QVHighlights 구조 호환 데이터 3건과 시맨틱 관계 17건을 대상으로 전체 검증 흐름을 수행하였다.

| 지표 | 결과 |
|---|---:|
| MR-mAP@0.50:0.95 | 91.6667 |
| MR-R1@0.50 | 100.0000 |
| MR-R1@0.70 | 100.0000 |
| HL-mAP Fair | 100.0000 |
| HL-mAP Good | 99.0741 |
| HL-mAP VeryGood | 83.3333 |
| Element F1 | 100.0000 |
| Relation F1 | 100.0000 |
| Relation Integrity | 100.0000 |

## QVHighlights 적용

`samples/qvhighlights_compatible_sample.jsonl`은 QVHighlights의 공개 데이터 구조를 기준으로 신규 작성한 참조 데이터이다. 외부 영상, 원본 annotation 및 Moment-DETR 코드는 저장소에 포함하지 않는다. 실제 외부 데이터를 연계할 때에는 해당 데이터의 이용 조건과 배포 범위를 확인한다.

## 권리 및 이용

본 저장소의 신규 작성 코드와 문서는 해당 용역 계약의 권리 귀속 조건을 따른다. 제3자 데이터와 소프트웨어의 권리는 각 출처와 라이선스에 따르며, 상세 내역은 `PROPRIETARY_NOTICE.md`와 `licenses/`에서 관리한다.
