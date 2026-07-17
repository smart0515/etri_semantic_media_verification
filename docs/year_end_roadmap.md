# 연말 동작 시스템 구현 로드맵

## 단계 1. 입출력 계약 확정

- ETRI 대상 시스템 API·파일·전송 프로토콜 확정
- 미디어 코덱, clip 단위, timestamp 정규화
- 오류코드·timeout·retry 정책

## 단계 2. 데이터셋 및 정답 구축

- QVHighlights 사용 승인 또는 대체 데이터셋 선정
- 대표 영상·query subset 확정
- element·relation 수작 annotation guideline 작성
- 복수 annotation 및 합의 절차 수행

## 단계 3. 멀티모달 분석 구현

- 비주얼 encoder, ASR, OCR, 음향 인식 adapter
- element 추출·표준화·중복 병합
- 시간·공간·서사·인과 relation 생성
- model card·버전·입력 hash 기록

## 단계 4. 재조립·재생 구현

- 요구 element 기반 전송 단위 선택
- 중요도·시간·코덱 제약을 반영한 assembly manifest
- FFmpeg 등을 이용한 재조립 adapter(사전 라이선스 협의)
- 재생 연속성·A/V sync 검증

## 단계 5. ETRI 연동 및 실제 검증

- EtriSystemAdapter 구현
- 동일 입력에 대한 참조 시스템·대상 시스템 출력 수집
- 구간·하이라이트·element·relation·재조립·성능 지표 산출
- 상호 입회 시험·이슈 조치·최종 확인

## 완료 기준

- 승인된 데이터셋으로 end-to-end 1개 이상 시나리오가 실행된다.
- 입력, 중간 출력, 예측, 재조립, 지표, 로그가 동일 실행 ID로 연결된다.
- 실제 결과와 Mock 결과가 파일·보고서에서 명확히 구분된다.
- 사용된 모든 오픈소스·모델·데이터셋의 사전 협의 및 고지가 완료된다.

