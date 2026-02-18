import ccxt
import pandas as pd
import numpy as np
import time
import os
import sys
import requests
from datetime import datetime

# ==========================================
# 1. 화면 설정 & 로고
# ==========================================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner_simple():
    clear_screen()
    print("  ____                    _             ")
    print(" / ___| __ _ _   _ _ __ | |_ ___ _ __ ")
    print("| |  _ / _` | | | | '_ \| __/ _ \ '__|")
    print("| |_| | (_| | |_| | | | | ||  __/ |   ")
    print(" \____|\__,_|\__,_|_| |_|\__\___|_|   ")
    print("                                      ")
    print(" ======================================================")
    print("    GAUNTER-O-DIMM Trend Follower Spec v7.1 (Final)")
    print("            Designed by [ GAUNTER-O-DIMM ]             ")   
    print(" ======================================================\n")

# ==========================================
# 1.5. 글로벌 마켓 감시 (도미넌스 & 페깅 & 추세)
# ==========================================
def get_global_market_status():
    try:
        # 1. 가격 (Coinbase)
        usdt_price = float(requests.get("https://api.coinbase.com/v2/prices/USDT-USD/spot").json()['data']['amount'])
        
        # 2. 글로벌 데이터 & 개별 코인 데이터 (CoinGecko)
        # 도미넌스 변화량을 계산하기 위해 24h 변동률 데이터가 필요함
        global_resp = requests.get("https://api.coingecko.com/api/v3/global", timeout=5).json()['data']
        
        # 비트코인과 테더의 24시간 변동률 가져오기 (도미넌스 역산용)
        coins_resp = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,tether&price_change_percentage=24h", 
            timeout=5
        ).json()
        
        btc_data = next(item for item in coins_resp if item['id'] == 'bitcoin')
        usdt_data = next(item for item in coins_resp if item['id'] == 'tether')

        # 현재 도미넌스
        cur_btc_dom = global_resp['market_cap_percentage']['btc']
        cur_usdt_dom = global_resp['market_cap_percentage'].get('usdt', 0)

        # [도미넌스 변화량 역산 로직]
        # 공식: 어제_도미 = 현재_도미 * ((1 + 전체시총변동률) / (1 + 코인시총변동률))
        total_chg = global_resp['market_cap_change_percentage_24h_usd'] / 100
        btc_chg_rate = btc_data['market_cap_change_percentage_24h'] / 100
        usdt_chg_rate = usdt_data['market_cap_change_percentage_24h'] / 100

        prev_btc_dom = cur_btc_dom * ((1 + total_chg) / (1 + btc_chg_rate))
        prev_usdt_dom = cur_usdt_dom * ((1 + total_chg) / (1 + usdt_chg_rate))

        btc_dom_delta = cur_btc_dom - prev_btc_dom
        usdt_dom_delta = cur_usdt_dom - prev_usdt_dom

        # [3] 테더 페깅 상태 메시지 결정
        # 가격은 무조건 보여주고, 상태 메시지만 여기서 정함
        if usdt_price >= 1.0005: 
            peg_msg = "🔴프리미엄 (주의)" 
        elif usdt_price <= 0.9995: 
            peg_msg = "🔵이탈우려 (주의)"
        else:
            peg_msg = "🟢안정"

        return {
            "btc_dom": cur_btc_dom,
            "btc_delta": btc_dom_delta,
            "usdt_dom": cur_usdt_dom,
            "usdt_delta": usdt_dom_delta,
            "usdt_price": usdt_price,
            "peg_msg": peg_msg
        }

    except Exception as e:
        # 에러 발생 시 None 리턴 (메인 루프에서 무시)
        return None

# ==========================================
# 2. 사용자 메뉴
# ==========================================
def main_menu():
    print_banner_simple()
    print(" [ 메인 컨트롤 센터 ]\n")
    print(" 1. Binance (바이낸스) - BTC/USDT")
    print(" 2. Coinbase (코인베이스) - BTC/USD")
    print(" Q. 시스템 종료")
    
    choice = input("\n >> 거래소를 선택해 (1/2/Q): ").strip().upper()
    
    if choice == 'Q':
        sys.exit()
    
    options = {'enableRateLimit': True, 'timeout': 15000}

    if choice == '1':
        exchange = ccxt.binance(options)
        symbol = 'BTC/USDT'
        ex_name = 'Binance'
        try:
            exchange.hosts = ['api.binance.com', 'api1.binance.com', 'api2.binance.com', 'api3.binance.com']
        except:
            pass
    elif choice == '2':
        exchange = ccxt.coinbase(options)
        symbol = 'BTC/USD'
        ex_name = 'Coinbase'
    else:
        return None, None, None, None

    print(f"\n >> {ex_name} 선택됨.")
    raw_input = input(" >> 시간봉 입력 (예: 15m, 1h, 4h): ")
    timeframe = raw_input.strip().lower()
    if not timeframe: timeframe = '15m'
        
    return exchange, ex_name, symbol, timeframe


# [추가] S/R Flip 감지 로직
def detect_sr_flip(df, window=5, tolerance=0.01):
    """
    df: 차트 데이터 (timestamp 컬럼 필수)
    window: 좌우 비교 범위
    tolerance: 오차 범위 비율
    """
    current_price = df['close'].iloc[-1]
    
    # 최근 500개 데이터만 사용 (속도 및 최신성 고려)
    subset = df.iloc[-500:-1].copy() 
    
    potential_pivots = [] # (가격, 타입, 날짜)를 저장할 리스트

    # 피벗 포인트 찾기
    for i in range(window, len(subset) - window):
        price = subset['close'].iloc[i]
        date_time = subset['timestamp'].iloc[i] # 타임스탬프 가져오기
        
        # 고점 판별
        is_high = all(subset['high'].iloc[i] >= subset['high'].iloc[i-k] for k in range(1, window+1)) and \
                  all(subset['high'].iloc[i] >= subset['high'].iloc[i+k] for k in range(1, window+1))
        
        # 저점 판별
        is_low = all(subset['low'].iloc[i] <= subset['low'].iloc[i-k] for k in range(1, window+1)) and \
                 all(subset['low'].iloc[i] <= subset['low'].iloc[i+k] for k in range(1, window+1))

        if is_high:
            potential_pivots.append((subset['high'].iloc[i], "RES", date_time))
        if is_low:
            potential_pivots.append((subset['low'].iloc[i], "SUP", date_time))

    # 현재 가격과 비교 (최신 피벗부터 역순으로 탐색)
    msg = "None"
    
    # 리스트를 뒤집어서 '가장 최근에 만들어진' 지지/저항부터 체크
    for pivot_price, p_type, p_time in reversed(potential_pivots):
        upper = pivot_price * (1 + tolerance)
        lower = pivot_price * (1 - tolerance)
        
        if lower <= current_price <= upper:
            # 타임스탬프를 읽기 좋은 날짜 문자열로 변환 (밀리초 제거)
            date_str = datetime.fromtimestamp(p_time / 1000).strftime('%Y-%m-%d %H:%M')
            
            # 메시지 구성
            if current_price >= pivot_price:
                # 가격이 위에 있으면 -> 지지(Support) 역할 기대
                role = "🟢 지지(Support)"
                origin = "고점" if p_type == "RES" else "저점"
                msg = f"{role} 테스트 중\n      └ 기준: {date_str}의 {origin} (${pivot_price:,.0f})"
            else:
                # 가격이 아래에 있으면 -> 저항(Resistance) 역할 기대
                role = "🔴 저항(Resistance)"
                origin = "저점" if p_type == "SUP" else "고점"
                msg = f"{role} 테스트 중\n      └ 기준: {date_str}의 {origin} (${pivot_price:,.0f})"
            
            return msg # 하나 찾으면 즉시 리턴

    return None

# ==========================================
# 3. 데이터 처리
# ==========================================
def fetch_and_process(exchange, symbol, timeframe):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=1000)
        # [수정] 리턴 값을 3개로 통일해야 해 (None, None, 메시지)
        if not ohlcv or len(ohlcv) < 200:
            return None, None, "데이터 부족" 
            
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # (1) 이평선
        df['EMA_55'] = df['close'].ewm(span=55, adjust=False).mean()
        df['EMA_200'] = df['close'].ewm(span=200, adjust=False).mean()
        
        # (2) 이격도
        df['Disp_Price_55'] = (df['close'] / df['EMA_55']) * 100
        df['Disp_55_200'] = (df['EMA_55'] / df['EMA_200']) * 100
        
        # (3) RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # (4) Volume Delta & Slope
        df['Vol_Delta'] = np.where(df['close'] > df['open'], df['volume'], -df['volume'])
        df['EMA_55_Slope'] = df['EMA_55'].diff()

        # [NEW] 타임프레임별 동적 설정 (Dynamic Settings)
        if timeframe in ['1m', '3m', '5m', '15m']:
            set_window = 5
            set_tol = 0.005  # 0.5%
        elif timeframe in ['30m', '1h', '4h']:
            set_window = 7
            set_tol = 0.01   # 1.0%
        else: 
            set_window = 9   # 굵직한 봉우리만
            set_tol = 0.02   # 2.0%

        # 함수 호출 시 설정값 전달
        sr_status = detect_sr_flip(df, window=set_window, tolerance=set_tol)
        
        return df, sr_status, None 

    except Exception as e:
        return None, None, str(e)

# ==========================================
# 4. 모니터링 & 판정
# ==========================================
def format_delta(val):
    """변화량에 따라 화살표와 색상(텍스트) 리턴"""
    if val > 0: return f"▲ {abs(val):.2f}%"
    elif val < 0: return f"▼ {abs(val):.2f}%"
    else: return "- 0.00%"

def run_monitor(exchange, ex_name, symbol, timeframe):
    print(f"\n >>> {ex_name} 데이터 로딩 중... (최대 1000봉)")
    
    # 글로벌 데이터 캐싱용 변수
    g_data = None

    while True:
        try:
            print(".", end="", flush=True)

            # [1] 글로벌 데이터 가져오기
            try:
                temp_g_data = get_global_market_status()
                if temp_g_data:
                    g_data = temp_g_data
            except Exception:
                pass 

            # [2] 차트 데이터 가져오기 (여기가 문제였어!)
            df, sr_msg, error_msg = fetch_and_process(exchange, symbol, timeframe)
            
            if df is not None:
                print_banner_simple()

                # [3] 글로벌 정보 출력 (전일 대비 등락 포함)
                if g_data:
                    print(f" [ 🌍 GLOBAL MARKET VIEW ]")
                    print(f"  ■ BTC.D : {g_data['btc_dom']:.2f}% ({format_delta(g_data['btc_delta'])})")
                    print(f"  ■ USDT.D: {g_data['usdt_dom']:.2f}% ({format_delta(g_data['usdt_delta'])})")
                    print(f"  ■ USDT  : ${g_data['usdt_price']:.4f}  {g_data['peg_msg']}")
                    print(" =" * 55 + "\n")

                curr = df.iloc[-1]
                
                # --- [판단 로직] ---
                is_golden_cross = curr['EMA_55'] > curr['EMA_200']
                trend_up = (curr['close'] > curr['EMA_55']) and (curr['EMA_55_Slope'] > 0)
                
                # 이격도 메시지
                p_val = curr['Disp_Price_55']
                if p_val >= 103: p_msg = "🔥과열(상승)"
                elif p_val <= 97: p_msg = "❄️과열(하락)"
                else: p_msg = "✅안정"
                
                t_val = curr['Disp_55_200']
                if t_val >= 104: t_msg = "📈확산(정배열)"
                elif t_val <= 96: t_msg = "📉확산(역배열)"
                else: t_msg = "✅수렴(초기)"

                # RSI 상태
                rsi_val = curr['RSI']
                if rsi_val >= 50: rsi_status = "🔥강세 (Bull)"
                else: rsi_status = "💧약세 (Bear)"
                
                # --- [화면 출력] ---
                print(f" [타겟] {ex_name} | {symbol} | {timeframe}")
                print(f" [시간] {datetime.now().strftime('%H:%M:%S')} (종료: Ctrl+C)\n")
                
                print(f" 💵 현재가      : {curr['close']:,.2f}")
                
                trend_icon = "📈 정배열(상승추세)" if is_golden_cross else "📉 역배열(하락추세)"
                print(f" 🌊 추세 지도   : {trend_icon}")
                print(f"    └ 55선: {curr['EMA_55']:,.2f} | 200선: {curr['EMA_200']:,.2f}")
                
                print(f" 📏 이격도 체크 : P-55[{p_msg}] / 55-200[{t_msg}]")
                
                vol_icon = "매수세 우위" if curr['Vol_Delta'] > 0 else "매도세 우위"
                print(f" 💪 체력(RSI)   : {rsi_val:.2f} -> {rsi_status}")
                print(f" 📊 수급(Vol)   : {vol_icon}")
                # [NEW] 지지/저항 구간 정보 출력
                if sr_msg: # 메시지가 있을 때만 출력
                    print(f" 🛡️ S/R 구간    : {sr_msg}")
                else:
                    print(f" 🛡️ S/R 구간    : ⚪ 특이사항 없음 (허공에 있음)")
                
                print("-" * 55)
                
                # --- [최종 코멘트] ---
                if is_golden_cross and rsi_val >= 50 and trend_up:
                    print("\n >>> [군터의 조언] 완벽한 '상승 추세'야. 파도에 올라타기 좋은 날.")
                elif not is_golden_cross and rsi_val < 50:
                    print("\n >>> [군터의 조언] 완전한 '하락 추세'야. 숏을 보거나 얌전히 있어.")
                elif is_golden_cross and rsi_val < 50:
                    print("\n >>> [군터의 조언] 상승장 중 '눌림목(조정)' 구간일 수 있어.")
                else:
                    print("\n >>> [군터의 조언] 추세가 혼조세야. 방향이 정해질 때까지 관망해.")

            else:
                print(f"\n [!!!] 오류: {error_msg}")
                time.sleep(3)
                
            time.sleep(2)

        except KeyboardInterrupt:
            return
        except Exception as e:
            # 치명적인 에러가 나도 루프가 안 꺼지게 방어
            print(f"\n[Error] {e}")
            time.sleep(5)

if __name__ == "__main__":
    try:
        while True:
            exchange, ex_name, symbol, timeframe = main_menu()
            if exchange:
                run_monitor(exchange, ex_name, symbol, timeframe)
    except Exception as e:
        print(f"\n\n[프로그램 종료] 오류 발생: {e}")
        input("엔터 키를 누르면 종료합니다...")
