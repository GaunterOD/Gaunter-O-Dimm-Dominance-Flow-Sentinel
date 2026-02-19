# GOD_Spec_v7.2 (Trend & Mean Reversion)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg)
![License](https://img.shields.io/badge/License-MIT-grey.svg)

**비트코인 추세 지속성 및 평균 회귀 분석 도구**
실시간 데이터 기반의 이격도(Mean Reversion) 분석과 RSI 50선 안착(Sustain) 카운팅을 지원합니다.

---

## 🚀 v7.2 업데이트 (New Features)

### 🧲 평균 회귀(Mean Reversion) 정밀 분석
- 가격-이평선 이격 감지: 현재가와 EMA 55선 사이의 간격을 계산하여 과열/침체 여부를 판독합니다.
- 상황별 경고 시스템: 상승 이격 과다(+7%)와 하락 이격 과다(-7%)를 구분하여 실시간 리스크 코멘트를 제공합니다.

### 💪 RSI 50선 안착(Sustain) 카운팅
- RSI가 50선 위/아래에서 연속으로 유지된 봉(Candle)의 개수를 실시간 추적합니다.
- 추세 전환(1봉): 방금 돌파 시점 포착
- 안착 시도(3~6봉): 지지 및 저항 확인 구간
- 추세 장악(7봉 이상): 강력한 방향성 지속 구간 판단

### 🛡️ S/R Flip & 클러스터링 확장
- 분석 범위를 최근 1,000개 캔들로 확대하여 신뢰도를 높였습니다.
- 주요 지지/저항 매물대 3곳을 엄선하여 현재가와의 거리(%)를 표시합니다.

---

## 📊 주요 분석 항목

### 1. 글로벌 데이터 (Global Market)
- BTC.D / USDT.D: 비트코인 및 테더 도미넌스 실시간 변동량
- USDT Pegging: 코인베이스 기준 테더 실시간 가격 감시 ($1.0000)

### 2. 기술적 지표 (Technical)
- 추세 지도: EMA 55/200 골든·데드크로스 판독
- RSI/Vol: 상대강도지수 및 거래량 델타(Volume Delta) 분석
- 이격도 분석: 현재가 vs 55선 / 55선 vs 200선 간의 거리 분석

---

## 🛠️ 실행 방법

### 바이너리 실행 (.exe)
1. [Releases] 탭에서 GAUNTER-O-DIMM_v7.2.exe 다운로드
2. 거래소 및 시간봉(1m ~ 1M) 입력 후 실행
3. Ctrl + C 입력 시 메인 메뉴로 복귀

### 소스 코드 실행
$ pip install ccxt pandas requests numpy
$ python GOD_Spec_v7.2.py

---

## ⚠️ 참고 사항 (FAQ)
- 백신 오진: 실행 파일이 삭제될 경우 Windows 보안 설정의 '제외' 항목에 등록하십시오.
- 데이터 부족: 신규 상장 코인의 경우 과거 데이터 부족으로 분석이 제한될 수 있습니다.

---

## 📡 Support
- 공식 채널: 비트맥스(BitMEX) 트롤박스 (ID: GAUNTER-O-DIMM)
- 개발자: Gaunter-O-Dimm

- 스크린샷
<img width="763" height="855" alt="image" src="https://github.com/user-attachments/assets/c871f287-655a-47a3-b603-fdef0bdee108" />

- 위와 같은 상황일 당시 트레이딩뷰 차트 
<img width="2413" height="1274" alt="image" src="https://github.com/user-attachments/assets/ab5751d6-a248-45aa-96a9-0731460b36e5" />

Designed by GAUNTER-O-DIMM



