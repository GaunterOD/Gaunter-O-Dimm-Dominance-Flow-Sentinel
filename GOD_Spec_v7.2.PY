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
    print("    GAUNTER-O-DIMM Trend Follower Spec v7.2 (Final)")
    print("             Designed by [ GAUNTER-O-DIMM ]              ")
    print(" ------------------------------------------------------")
    print("  Supported: 1m, 3m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M  ")
    print("  Control  : Press [ Ctrl + C ] to Stop / Back         ")
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

    
    print(" [지원 시간봉: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M]")
    
    raw_input = input(" >> 시간봉 입력 (기본값 15m): ")
    timeframe = raw_input.strip().lower()
    if not timeframe: timeframe = '15m'
        
    return exchange, ex_name, symbol, timeframe



def detect_sr_flip(df, window=5, tolerance=0.01):
    """
    df: 차트 데이터 (timestamp 컬럼 필수)
    window: 좌우 비교 범위
    tolerance: 오차 범위 비율
    """
    current_price = df['close'].iloc[-1]
    
    # 최근 1000개 데이터만 사용 (속도 및 최신성 고려)
    subset = df.iloc[:-1].copy() 
    
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

    # [3] 클러스터링 (비슷한 가격대 뭉치기) & 필터링
    zones = []
    
    for p_price, p_type, p_time in reversed(potential_pivots):
        # 기존 존들과 비교
        is_grouped = False
        for i, (z_price, z_count, z_type, z_time) in enumerate(zones):
            # 기존 존 가격의 오차범위 내에 있다면 같은 존으로 취급 (횟수 증가)
            if z_price * (1 - tolerance) <= p_price <= z_price * (1 + tolerance):
                # 가격을 평균내서 업데이트 (더 정확해짐)
                new_avg = (z_price * z_count + p_price) / (z_count + 1)
                zones[i] = (new_avg, z_count + 1, z_type, p_time) # 시간은 최신걸로
                is_grouped = True
                break
        
        if not is_grouped:
            zones.append((p_price, 1, p_type, p_time)) # (가격, 터치횟수, 타입, 시간)

    # [4] 현재가 기준 가까운 순서로 정렬 및 선별
    valid_zones = []
    
    for z_price, z_count, z_type, z_time in zones:
        # 조건: 2번 이상 지지/저항 받았거나, 최근에 생긴 외바닥/외봉일 경우
        if z_count >= 2: 
            valid_zones.append({'price': z_price, 'count': z_count, 'type': z_type})

    # 현재가와 거리 계산해서 정렬
    valid_zones.sort(key=lambda x: abs(x['price'] - current_price))

    # 가장 가까운 3개만 리턴
    return valid_zones[:3] if valid_zones else None


# [수정됨] 데이터 처리
def fetch_and_process(exchange, symbol, timeframe):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=1000)
        
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
            set_window = 10       
            set_tol = 0.003       
        elif timeframe in ['30m', '1h', '4h']:
            set_window = 15
            set_tol = 0.005       
        elif timeframe in ['1d', '3d']:
            set_window = 20
            set_tol = 0.01        
        else: # 1w, 1M 등
            set_window = 30       
            set_tol = 0.02        

        # 함수 호출 시 설정값 전달 (결과값 변수명도 리스트임을 명시하기 위해 변경)
        sr_lines = detect_sr_flip(df, window=set_window, tolerance=set_tol)
        
        return df, sr_lines, None

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
    
    g_data = None

    while True:
        try:
            print(".", end="", flush=True)

            # [1] 글로벌 데이터
            try:
                temp_g_data = get_global_market_status()
                if temp_g_data:
                    g_data = temp_g_data
            except Exception:
                pass 

            # [2] 차트 데이터
            df, sr_msg, error_msg = fetch_and_process(exchange, symbol, timeframe)
            
            if df is not None:
                print_banner_simple()

                # [3] 글로벌 정보
                if g_data:
                    print(f" [ 🌍 GLOBAL MARKET VIEW ]")
                    print(f"  ■ BTC.D : {g_data['btc_dom']:.2f}% ({format_delta(g_data['btc_delta'])})")
                    print(f"  ■ USDT.D: {g_data['usdt_dom']:.2f}% ({format_delta(g_data['usdt_delta'])})")
                    print(f"  ■ USDT  : ${g_data['usdt_price']:.4f}  {g_data['peg_msg']}")
                    print(" =" * 60 + "\n")

                curr = df.iloc[-1]
                
                # --- [판단 로직] ---
                is_golden_cross = curr['EMA_55'] > curr['EMA_200']
                trend_up = (curr['close'] > curr['EMA_55']) and (curr['EMA_55_Slope'] > 0)
                
                # (1) 이격도 정밀 분석
                gap_p_55 = curr['Disp_Price_55'] - 100
                if gap_p_55 >= 5.0: 
                    p_status, p_comment = "🔴과매수", "이격 과다! 되돌림 주의"
                elif gap_p_55 <= -5.0:
                    p_status, p_comment = "🔵과매도", "이격 과다! 기술적 반등 가능성"
                elif gap_p_55 > 0:
                    p_status, p_comment = "📈상승 유지", "55선 위 지지 중"
                else:
                    p_status, p_comment = "📉하락 유지", "55선 아래 저항 중"

                # (2) 55-200 이격도
                gap_55_200 = curr['Disp_55_200'] - 100
                if gap_55_200 >= 10.0:
                    t_status, t_comment = "🚀단기 과열", "간격 너무 넓음 (조정 주의)"
                elif gap_55_200 <= -10.0:
                    t_status, t_comment = "💀단기 침체", "간격 너무 넓음 (반등 주의)"
                elif gap_55_200 > 0:
                    t_status, t_comment = "✨정배열", "이상적인 확산 중"
                else:
                    t_status, t_comment = "🌧️역배열", "하락 힘이 강함"

                # (3) RSI 정밀 분석 (지속성 카운팅) [NEW]
                rsi_val = curr['RSI']
                if rsi_val >= 70: rsi_status = "🔥과매수 구간 (70↑)"
                elif rsi_val <= 30: rsi_status = "💧과매도 구간 (30↓)"
                elif rsi_val >= 50: rsi_status = "✨강세 구간 (Bull)"
                else: rsi_status = "🌑약세 구간 (Bear)"

                # [NEW] RSI 50선 기준 지속성 카운팅 로직
                rsi_series = df['RSI'].values
                current_is_bull = rsi_val >= 50
                rsi_duration = 0
                
                # 역순으로 추적하여 몇 봉 연속인지 계산
                for i in range(len(rsi_series) - 1, -1, -1):
                    val = rsi_series[i]
                    if current_is_bull and val >= 50:
                        rsi_duration += 1
                    elif not current_is_bull and val < 50:
                        rsi_duration += 1
                    else:
                        break # 추세가 끊긴 지점
                
                # 상황별 메시지 생성
                if rsi_duration == 1:
                    # 방금 막 돌파함
                    action_msg = "🚀 [알림] 방금 50선 돌파! (추세 전환 시도)"
                elif 3 <= rsi_duration <= 6:
                    # 3~6봉 지속 (안착 시도 중)
                    action_msg = f"👀 [주시] 추세 굳히기 중 ({rsi_duration}봉 연속 유지)"
                elif rsi_duration > 6:
                    # 장기 지속
                    tag = "🔥상승" if current_is_bull else "❄️하락"
                    action_msg = f"{tag}세 완전 장악 ({rsi_duration}봉 째 지속 중)"
                else:
                    # 2봉 등 애매한 구간
                    action_msg = f"🔍 방향 탐색 중 ({rsi_duration}봉 째)"

                
                # --- [화면 출력] ---
                print(f" [타겟] {ex_name} | {symbol} | {timeframe}")
                print(f" [시간] {datetime.now().strftime('%H:%M:%S')} (종료: Ctrl+C)\n")
                
                print(f" 💵 현재가        : {curr['close']:,.2f}")
                
                trend_icon = "📈 정배열(상승장)" if is_golden_cross else "📉 역배열(하락장)"
                print(f" 🌊 추세 지도    : {trend_icon}")
                print(f"    └ 55선: {curr['EMA_55']:,.2f} | 200선: {curr['EMA_200']:,.2f}")
                
                print("-" * 60) # 섹션 구분선
                
                print(f" 🧲 이격도 분석 (평균 회귀 관점)")
                print(f"    ① [현재가 vs 55선] : {gap_p_55:+.2f}% ({p_status})")
                print(f"       └ 해석: {p_comment}")
                print()
                print(f"    ② [55선 vs 200선]  : {gap_55_200:+.2f}% ({t_status})")
                print(f"       └ 해석: {t_comment}")
                
                print("-" * 60) # 섹션 구분선
                
                vol_icon = "매수세 우위" if curr['Vol_Delta'] > 0 else "매도세 우위"
                print(f" 💪 체력(RSI)    : {rsi_val:.2f} -> {rsi_status}")
                print(f"    └ 지속성 : {action_msg}") 
                print(f" 📊 수급(Vol)    : {vol_icon}")
                
                print("-" * 60) # 섹션 구분선
                
                print(f" 🛡️ S/R 주요구간 (가까운 순)")
                if sr_msg and isinstance(sr_msg, list): 
                    for item in sr_msg:
                        p = item['price']
                        cnt = item['count']
                        diff = ((curr['close'] - p) / p) * 100
                        
                        if curr['close'] >= p:
                            pos_str = f"🟢 지지 (하방 {abs(diff):.2f}%)"
                        else:
                            pos_str = f"🔴 저항 (상방 {abs(diff):.2f}%)"
                            
                        print(f"    └ {pos_str} : ${p:,.0f} (터치 {cnt}회)")
                else:
                    print(f"    └ ⚪ 현재가 근처에 뚜렷한 매물대 없음")
                
                print("=" * 60) # 최종 구분선
                

                # --- [최종 코멘트: 상황별 정밀 조언] ---
                print(" >>> [군터의 조언]", end=" ")
                
                # 1. 이격도 과다 (위험 경고)
                if gap_p_55 >= 7.0:
                    print("🔥상승폭이 너무 커! 지금 사면 '고점 판독기' 된다. 조정 올 때까지 참아.")
                elif gap_p_55 <= -7.0:
                    print("💧너무 많이 빠졌어. '기술적 반등'이 나올 자리야. 추격 숏은 위험해.")
                
                # 2. 추세 확정 (건강한 흐름)
                elif is_golden_cross and rsi_val >= 50 and trend_up:
                    print("🚀상승 추세가 아주 건강해! 쫄지 말고 흐름에 올라타. (Long 유리)")
                elif not is_golden_cross and rsi_val < 50:
                    print("📉하락 추세가 명확해. 반등 시 숏을 보거나 현금 쥐고 있어. (Short 유리)")
                
                # 3. 비추세/횡보
                else:
                    print("💤방향이 애매해. 고래들이 싸우는 중이니 이평선 정리될 때까지 구경해.")

            else:
                print(f"\n [!!!] 오류: {error_msg}")
                time.sleep(3)
                
            time.sleep(2)

        except KeyboardInterrupt:
            return
        except Exception as e:
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
