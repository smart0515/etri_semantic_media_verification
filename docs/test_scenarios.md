# 시험 시나리오

## 1. 현 단계 사전검증

| ID | 시나리오 | 입력 | 기대 결과 | 상태 |
|---|---|---|---|---|
| TC-001 | QVHighlights 호환 JSONL 로드 | 합성 3건 | qid·window·clip·saliency 변환 | 구현 |
| TC-002 | 잘못된 window 범위 탐지 | duration 초과 window | 입력 거부·오류 기록 | 구현 |
| TC-003 | Mock 예측 생성 | 정답 annotation | 예측 JSONL 생성, PRELIMINARY_MOCK 표시 | 구현 |
| TC-004 | Moment metric 흐름 | GT/Mock windows | MR-mAP·R@1 산출 | 구현 |
| TC-005 | Highlight metric 흐름 | clip score/Mock score | threshold별 mAP·Hit@1 | 구현 |
| TC-006 | Relation integrity | element·unit·relation | 미선언 node·predicate 탐지 | 구현 |
| TC-007 | Reassembly plan | 예측 windows | 시간순 클립 목록 | 구현 |
| TC-008 | 결과 면책 표시 | 데모 전체 | 실제 성능이 아님을 JSON에 표시 | 구현 |

## 2. 연말 실제 검증

| ID | 시나리오 | 주요 관찰값 | 증빙 |
|---|---|---|---|
| TC-101 | 비디오+자연어 질의 분석 | element, relation, window | 요청·응답 JSON, 로그 |
| TC-102 | 음성·텍스트·영상 element 통합 | modality별 element | 중간 출력, 모델 버전 |
| TC-103 | element-전송 단위 연결 | media unit reference | 페이로드, trace |
| TC-104 | 사용자 요구 기반 재조립 | selected unit order | manifest, 출력 파일 |
| TC-105 | 재생 가능성 | timestamp/codec continuity | 재생 로그, 화면 증빙 |
| TC-106 | 구간 검색 정확도 | MR-mAP, R@1 | metric JSON |
| TC-107 | 하이라이트 정확도 | HL-mAP, Hit@1 | metric JSON |
| TC-108 | element·relation 정확도 | Precision/Recall/F1 | matching 상세 내역 |
| TC-109 | 반복 일관성 | 5회 출력 일치율 | run별 hash·출력 |
| TC-110 | 환경 재현성 | 환경 간 편차 | 환경 명세, 결과 비교 |
| TC-111 | 단계별 처리 성능 | latency, throughput | timestamp, resource log |
| TC-112 | 비정상 입력 | error code, recovery | 오류·복구 로그 |

## 3. 입회 확인 항목

- 시험 일시·장소·참석자
- 대상 시스템·모델·검증시스템 버전
- 테스트 데이터 split·qid·hash
- 장비·OS·GPU·driver·codec 환경
- 시나리오별 입력·기대결과·실제결과·판정
- 이슈 및 조치 내역
- ETRI 담당자 확인·회의록

