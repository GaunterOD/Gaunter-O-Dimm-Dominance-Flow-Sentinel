# Dominance-Flow-Sentinel v7.0

![Version](https://img.shields.io/badge/version-7.0.0-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-lightgrey.svg)

비트코인 도미넌스와 주요 기술적 지표를 결합하여 실시간으로 시장 추세를 분석하는 **CLI 기반 트레이딩 보조 도구**입니다. 전체 시장의 자금 흐름과 개별 차트의 강세를 한눈에 파악할 수 있도록 설계되었습니다.

---

## 🛠️ 주요 기능 (Key Features)

### 1. 글로벌 마켓 분석 (Macro View)
* **도미넌스 추적:** 비트코인(BTC.D) 및 테더(USDT.D) 도미넌스의 실시간 수치와 전일 대비 등락(%)을 표시합니다.
* **테더 페깅 감시:** 코인베이스(Coinbase) USD 페어 데이터를 기반으로 USDT의 $1 페깅 상태를 정밀 모니터링합니다.

### 2. 기술적 지표 분석 (Technical Analysis)
* **추세 판단:** EMA 55일선과 200일선의 정배열/역배열 상태를 통해 시장의 방향성을 제시합니다.
* **이격도 분석:** 현재 가격과 이동평균선 사이의 이격도를 계산하여 과열 또는 침체 여부를 판별합니다.
* **강도 및 수급:** RSI 지표를 통한 시장 체력 진단과 거래량 델타를 활용한 수급 현황을 제공합니다.

---

## 🚀 사용 방법 (Usage)

### 실행 파일(EXE) 이용 시
1. [Releases](https://github.com/GaunterOD/Gaunter-O-Dimm-Dominance-Flow-Sentinel/releases) 탭에서 최신 버전의 실행 파일을 다운로드합니다.
2. 프로그램을 실행한 후 분석할 거래소(Binance / Coinbase)를 선택합니다.
3. 확인하고자 하는 시간봉(예: 15m, 1h, 4h, 1d)을 입력하면 실시간 모니터링이 시작됩니다.

### 소스 코드 실행 시
```bash
# 가상환경 설정 및 필수 라이브러리 설치
python -m venv venv
venv\Scripts\activate
pip install pandas ccxt requests

# 프로그램 실행
python "gaunter_v7.py"



📝 참고 사항 (Notes)
데이터 출처: Coinbase (Spot Price), CoinGecko (Global Dominance), Binance/Coinbase (OHLCV).

빌드 정보: Nuitka 컴파일러를 사용하여 C++ 기반으로 최적화된 단일 실행 파일을 제공합니다.

⚖️ 면책 조항 (Disclaimer)
본 프로그램은 투자 판단을 돕기 위한 정보 제공만을 목적으로 하며, 금융 상품의 매수·매도를 권유하지 않습니다. 모든 투자의 책임은 투자자 본인에게 있으며, 개발자는 프로그램 사용으로 인해 발생하는 어떠한 손실에 대해서도 책임을 지지 않습니다.

👤 Author
GAUNTER-O-DIMM

Bitcoin Trend Analysis & Open Source Development

[GitHub Profile](https://github.com/GaunterOD)



# 📈 GAUNTER-O-DIMM Trend Follower Spec v7.0 (Final)
> **실시간 가상화폐 시장 추세 및 자금 흐름 분석 도구**

바이낸스(Binance)와 코인베이스(Coinbase)의 데이터를 기반으로 시장의 거시적인 흐름과 기술적 지표를 실시간으로 분석합니다. 단순한 가격 등락을 넘어 시장의 '맥락'을 파악하세요.

---

## 1. 프로그램 개요
본 프로그램은 비트코인의 가격 추세뿐만 아니라, 전체 가상화폐 시장의 자금 흐름(Dominance)을 실시간으로 분석하여 투자 판단을 돕는 강력한 보조 도구입니다.

## 2. 주요 기능 및 화면 설명

### 🌍 글로벌 마켓 뷰 (Global Market View)
시장의 전체적인 '날씨'를 판단하는 거시 지표입니다.

| 지표 | 설명 | 비고 |
| :--- | :--- | :--- |
| **BTC.D** | 비트코인 도미넌스 | 상승 시 비트코인 독주 혹은 알트코인 하락 가능성 |
| **USDT.D** | 테더 도미넌스 | 상승 시 현금화 및 하락장 관망세 심화 |
| **USDT Pegging** | 테더 가격 안정성 | 🔴 $1.00 이상: 매수 대기 유입 / 🔵 $1.00 미만: 자금 이탈 우려 |

### 🌊 기술적 분석 지표
* **추세 지도 (Trend Map):** EMA 55일선과 200일선을 비교합니다.
    * 📈 **정배열:** 상승 추세 (매수 유리)
    * 📉 **역배열:** 하락 추세 (매도/관망 유리)
* **이격도 (Disparity):** 현재 가격과 이동평균선의 거리를 분석하여 **[과열 / 안정 / 침체]** 상태를 진단합니다.
* **시장 체력 & 수급:**
    * **RSI:** 50 기준 강세/약세 판별
    * **Volume:** 직전 캔들 대비 매수/매도 우위 분석

---

## 3. 사용 방법
1. `Gunther_v7.2_Final.exe` 파일을 실행합니다.
2. 분석할 **거래소**를 선택합니다. (1: Binance, 2: Coinbase)
3. 분석할 **시간봉(Timeframe)**을 입력합니다. (예: `15m`, `1h`, `4h`, `1d`)
4. 프로그램이 실행되면 실시간으로 데이터가 갱신됩니다.

---

## 🛡️ 실행 및 보안 설정 (중요)
파이썬 실행 파일(.exe) 특성상 윈도우 백신이 위협으로 오진할 수 있습니다. 파일이 강제로 삭제된다면 아래 절차를 따라주세요.

> **Windows 보안 예외 등록 방법:**
> 1. `Windows 보안` 앱 실행 -> `바이러스 및 위협 방지` 클릭
> 2. `설정 관리` -> 맨 아래 `제외 추가 또는 제거` 클릭
> 3. `+ 제외 사항 추가` 버튼 클릭 후 `파일` 선택
> 4. 실행 파일(`Gunther_v7.2_Final.exe`)을 선택하여 등록

---

## ❓ 자주 묻는 질문 (FAQ)

**Q. 화면이 주기적으로 깜빡거립니다.**
A. 정상입니다! 실시간 데이터를 최신으로 유지하기 위해 화면을 리프레시하는 과정입니다.

**Q. 도미넌스 옆의 화살표(▲/▼)는 무엇인가요?**
A. 전일(24시간 전) 대비 수치의 변동률을 나타냅니다.

**Q. "Windows의 PC 보호" 창이 뜹니다.**
A. [추가 정보]를 누른 뒤 [실행] 버튼을 클릭하면 정상 작동합니다.

---

## ⚠️ 면책 조항 (Disclaimer)
본 프로그램은 투자 판단을 돕기 위한 **보조 지표**일 뿐이며, 미래의 수익을 보장하지 않습니다. 모든 투자의 책임은 사용자 본인에게 있습니다. 지표를 맹신하기보다 본인의 통찰력과 함께 참고용으로 활용하시기 바랍니다.

## ✉️ Support & Contact
* **Channel:** BitMEX 트롤박스 International 2 채널
* **Manager:** `Gaunter-O-Dimm (군터)`

---
**Designed by GAUNTER-O-DIMM**
*"In codes we trust, in errors we learn."*



