# 시험 시나리오

## 1. 납품 검증 시나리오

| ID | 시험 항목 | 입력 | 기대 결과 |
|---|---|---|---|
| TC-001 | QVHighlights 호환 JSONL 로드 | 참조 annotation 3건 | 전 건 로드, qid 고유성 확인 |
| TC-002 | 입력 범위 검사 | 구간·clip·duration | 범위 및 배열 길이 정합 |
| TC-003 | 참조 prediction 생성 | annotation | Prediction Schema 준수 |
| TC-004 | Moment Retrieval 평가 | 정답·예측 구간 | MR-mAP·R@1 생성 |
| TC-005 | Highlight Detection 평가 | 정답·예측 중요도 | 등급별 mAP·Hit@1 생성 |
| TC-006 | relation 무결성 | element·media unit·relation | node·predicate 전 건 유효 |
| TC-007 | 재조립 계획 | 예측 구간 | 시간순 media unit 계획 생성 |
| TC-008 | 결과 패키지 | 전체 실행 | prediction·plan·evaluation 파일 생성 |

## 2. 대상 시스템 연동 시나리오

| ID | 시험 항목 | 확인 내용 |
|---|---|---|
| IT-001 | 입력 계약 | query·vid·qid·시간 기준 전달 |
| IT-002 | 출력 계약 | Prediction Schema 변환 및 오류 처리 |
| IT-003 | element 추출 | 유형·label·시간 구간 정확성 |
| IT-004 | relation 생성 | 삼중항 정확성 및 참조 무결성 |
| IT-005 | 전송 단위 연결 | element-media unit 연결 정합성 |
| IT-006 | 재조립 | 선택 단위·순서·중복·누락 확인 |
| IT-007 | 반복 실행 | 동일 입력 결과의 일관성 |
| IT-008 | 성능 | 단계별 지연시간과 처리량 |
| IT-009 | 장애 복구 | timeout·부분 응답·재시도 |
| IT-010 | 증빙 추적 | 실행 ID 기반 입력·출력·지표 연결 |

## 3. 합격 조건

- 필수 JSON Schema 위반이 없다.
- 모든 relation이 선언된 node와 predicate를 참조한다.
- 지표 JSON과 보고서 표의 값이 일치한다.
- 실행 ID를 통해 입력, 출력, 설정과 결과를 추적할 수 있다.
- 대상 시스템 연동 시험은 합의된 프로파일의 기준값을 적용한다.
