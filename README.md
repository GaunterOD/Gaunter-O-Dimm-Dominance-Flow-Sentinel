# GOD_Spec_v7.3 (Stability & UI)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg)
![License](https://img.shields.io/badge/License-MIT-grey.svg)

**비트코인 추세 지속성 및 평균 회귀 분석 도구**
실시간 데이터 기반의 이격도(Mean Reversion) 분석과 터미널 환경에 최적화된 직관적인 컬러 UI를 제공합니다.

---

## 🚀 버전별 업데이트 내역 (Changelog)

### [v7.3] Stability & Color UI (현재 버전)
- **글로벌 마켓 뷰 확장:** BTC뿐만 아니라 ETH, SOL의 도미넌스 실시간 변화량(Delta) 모니터링 추가.
- **가독성(Color UI) 향상:** 터미널 환경에서 방향성(상승/하락), 수급, 매물대에 ANSI 컬러를 적용하여 직관성 극대화.
- **API 상태 표시기(신호등):** 코인게코 API 60초 쿨타임을 🟢/🟡/🔴 신호등 및 남은 시간으로 화면 상단에 표시.
- **시스템 안정성 확보:** 코인베이스 API 응답 지연 시 봇이 멈추는 프리징 현상 방지(타임아웃 적용).

### [v7.2] Mean Reversion & Regime
- 가격-이평선 간의 간격을 측정하는 평균 회귀(Mean Reversion) 분석 도입.
- RSI 50선 기준 추세 안착(Sustain) 카운팅 로직 추가.
- 최근 1,000개 캔들 기반 주요 지지/저항(S/R) 매물대 3곳 추출.

---

## 📊 주요 분석 항목

### 1. 글로벌 데이터 (Global Market)
- BTC.D / ETH.D / SOL.D / USDT.D 실시간 변동량 추적.
- USDT Pegging: 코인베이스 기준 테더 실시간 가격 감시 ($1.0000).

### 2. 기술적 지표 (Technical)
- 추세 지도: EMA 55/200 골든·데드크로스 판독.
- 체력 및 수급: RSI 지속성 카운팅 및 거래량 델타(Volume Delta) 분석.
- 이격도 정밀 분석: 현재가 vs 55선 / 55선 vs 200선 간의 거리 측정.

---

## 🛠️ 실행 방법

### 바이너리 실행 (.exe)
1. [Releases] 탭에서 `GAUNTER-O-DIMM_v7.3.exe` 다운로드.
2. 거래소(1: 바이낸스, 2: 코인베이스) 및 시간봉(1m ~ 1M) 입력.
3. 실행 중 `Ctrl + C` 입력 시 메인 메뉴로 안전하게 복귀.

### 소스 코드 실행
```bash
$ pip install ccxt pandas requests numpy
$ python GOD_Spec_v7.3.py
```

---

## ⚠️ 주의 및 참고 사항 (Notice)
- **투자 책임:** 본 프로그램의 데이터는 보조 참고용 지표입니다. 모든 투자 판단과 책임은 사용자 본인에게 있습니다.
- **거래소 차이:** 바이낸스는 거의 모든 정밀 시간봉(2h, 4h, 6h 등)을 지원하나, 코인베이스는 API 특성상 특정 시간봉에서 로딩 에러가 발생할 수 있습니다. (에러 지속 시 `Ctrl + C`로 초기화)
- **백신 오진:** 파이썬 실행 파일 특성상 백신에서 삭제할 수 있습니다. Windows 보안 설정의 '제외' 항목에 등록해 주세요.

---

## 📡 Support
- 공식 채널: 비트맥스(BitMEX) 트롤박스 (ID: GAUNTER-O-DIMM)
- 개발자: Gaunter-O-Dimm

### 📸 스크린샷
<img width="798" height="987" alt="스크린샷 2026-02-19 201209" src="https://github.com/user-attachments/assets/63b6e1bf-d8e3-4d42-8124-c87b8204f465" />


*(해당 시점의 트레이딩뷰 차트 캡처본)*
<img width="1698" height="1038" alt="스크린샷 2026-02-19 201133" src="https://github.com/user-attachments/assets/62ab8448-e998-4c6c-b0b3-0245fc00fd61" />


Designed by GAUNTER-O-DIMM
