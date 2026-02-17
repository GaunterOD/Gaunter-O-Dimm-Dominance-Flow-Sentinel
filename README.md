# 🛡️ Dominance-Flow-Sentinel v7.0 (Final)

![Version](https://img.shields.io/badge/version-7.0.0-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

---

## ✨ 핵심 기능 (Key Features)

### 🌍 글로벌 마켓 매크로 분석
* **BTC & USDT 도미넌스:** 전체 시장의 자금 흐름을 실시간으로 추적합니다.
* **전일 대비 등락(Delta):** 수학적 역산 로직을 통해 24시간 전 대비 변화량을 즉시 계산하여 표시합니다.
* **테더 페깅 감시:** 코인베이스 데이터를 기반으로 USDT의 $1 유지 여부(프리미엄/디스카운트)를 정밀 감시합니다.

### 📈 기술적 지표 분석
* **이동평균선(EMA):** 55일선과 200일선의 정배열/역배열을 통해 장기 추세를 판단합니다.
* **이격도(Disparity):** 가격과 이평선의 괴리율을 분석하여 과열 및 침체 구간을 포착합니다.
* **시장 강도(RSI):** 50 기준선을 중심으로 현재 시장의 체력을 진단합니다.
* **수급(Volume Delta):** 실시간 거래량 추이를 분석하여 매수/매도 우위를 판단합니다.

---

## 🖥️ 실행 화면 (Preview)

```text
 [ 🌍 GLOBAL MARKET VIEW ]
  ■ BTC.D : 54.20% (▲ 0.12%)  |  USDT.D : 5.10% (▼ 0.05%)
  ■ USDT  : 🟢정상 ($1.0001)
 ======================================================

 💵 현재가      : 96,500.00
 🌊 추세 지도   : 📈 정배열(상승추세)
 📏 이격도 체크 : P-55[✅안정] / 55-200[📈확산]
 💪 체력(RSI)   : 62.50 -> 🔥강세 (Bull)

