# QVHighlights 적용 방안

## 1. 선정 이유

QVHighlights는 자연어 질의에 대한 관련 비디오 구간과 클립 중요도를 함께 제공한다. 따라서 다음 과업을 설명하기 위한 참조 데이터로 적합하다.

- 사용자 요구에 부합하는 시맨틱 구간 선택
- 시간 구간을 미디어 전송 단위로 변환
- 중요도에 따른 우선순위 또는 재조립 정책 적용
- 정답과 시스템 예측 구간의 정량 비교

## 2. 원본 필드

| 필드 | 형식 | 설명 |
|---|---|---|
| `qid` | int | query 고유 ID |
| `query` | string | 자연어 요구 |
| `duration` | integer | 비디오 길이(초) |
| `vid` | string | 영상 ID |
| `relevant_windows` | list([start,end]) | 정답 시간 구간 |
| `relevant_clip_ids` | list(int) | 관련 2초 클립 ID |
| `saliency_scores` | list([s1,s2,s3]) | 3명 평가자의 0~4점 점수 |

## 3. 출력 필드

- `pred_relevant_windows`: `[start, end, confidence]` 목록
- `pred_saliency_scores`: 모든 2초 클립의 예측 중요도

## 4. 적용 단계

1. 발주기관과 annotation·영상 사용 범위를 협의한다.
2. 승인된 환경에서 데이터를 다운로드하고 출처·해시를 기록한다.
3. QVHighlights adapter로 필드·범위·길이를 검사한다.
4. 원본 annotation과 ETRI extension을 qid로 조인한다.
5. 검증시스템과 ETRI 대상 시스템에 동일 입력을 제공한다.
6. 예측 구간·중요도·element·relation을 수집한다.
7. 공통 평가기로 정량 지표를 산출한다.

## 5. 제약과 보완

QVHighlights 원본은 시각-언어 기반 구간 검색에 중점을 둔다. ETRI 과업에서 요구하는 음성, 텍스트, 인물, 사건, 인과·서사 관계 정답은 별도로 확장해야 한다. 보고 단계에서는 3건의 합성 샘플에 확장 스키마를 적용했으며, 연말에는 대표 샘플에 대한 수작 정답 구축이 필요하다.

## 6. 라이선스

- 공식 Moment-DETR 저장소의 코드: MIT
- QVHighlights annotation: CC BY-NC-SA 4.0
- YouTube 영상: annotation 라이선스와 별도의 권리·서비스 조건 검토 필요

본 납품본은 원본 annotation·영상·Moment-DETR 코드를 복사하지 않고 스키마와 공식 출처만 참조한다.

## 7. 공식 참고자료

- Dataset structure: https://github.com/jayleicn/moment_detr/blob/main/data/README.md
- Evaluation format: https://github.com/jayleicn/moment_detr/blob/main/standalone_eval/README.md
- Reference evaluation code: https://github.com/jayleicn/moment_detr/blob/main/standalone_eval/eval.py
- Paper: https://arxiv.org/abs/2107.09609
- CC BY-NC-SA 4.0: https://creativecommons.org/licenses/by-nc-sa/4.0/

