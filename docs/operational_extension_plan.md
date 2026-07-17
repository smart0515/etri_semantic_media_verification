# 운영 확장 계획

## 1. 대상 시스템 연동

- API, JSONL 파일 교환 또는 전송 추적 방식에 맞춘 `EtriSystemAdapter` 구현
- 입력·출력·오류·timeout·retry 계약 고정
- 공통 Prediction Schema 기반 contract test 자동화

## 2. 멀티모달 분석 확장

- 비주얼, ASR, OCR, 음향 인식 adapter 연결
- element 추출·표준화·중복 병합
- 시간·공간·서사·인과 relation 생성
- model card, 버전, 입력 hash 및 provenance 기록

## 3. 전송·재조립 확장

- 요구 element 기반 media unit 선택
- 중요도·시간·코덱 제약을 반영한 assembly manifest
- 승인된 미디어 도구를 통한 재조립 adapter 연결
- 재생 연속성, A/V sync 및 누락·중복 검사

## 4. 운영 품질

- 실행 ID 기반 입력·출력·지표·로그 추적
- 반복 실행 일관성과 환경 간 재현성 검사
- 단계별 latency와 throughput 수집
- 사용 소프트웨어·모델·데이터셋의 라이선스 및 버전 관리
