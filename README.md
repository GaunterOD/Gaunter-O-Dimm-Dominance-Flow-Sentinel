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



