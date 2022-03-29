import time
import pyupbit
import datetime
import schedule
import numpy as np
import operator

def get_upper_down_rate(ticker, lastbuyprice):
    df = pyupbit.get_ohlcv(ticker, interval="minute30", count=1)
    start_price = df.iloc[0]['open']
    rate =  ((get_current_price(ticker)-lastbuyprice)/lastbuyprice)*100

    return rate

def get_ror(ticker,k):
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=7)
    time.sleep(0.1)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror
    
def find_bestk(ticker):
  for k in np.arange(0.1,1.0,0.1):
    ror = get_ror(ticker, k)
    
    if k == 0.1:
      bestk = k
      max = ror
    else:
      if ror> max:
        max = ror
        bestk = k
  return round(bestk,1)

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price



def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

def get_ma2(ticker):
    """2일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=2)
    ma2 = df['close'].rolling(2).mean().iloc[-1]
    return ma2

def get_ma3(ticker):
    """2일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=3)
    ma2 = df['close'].rolling(3).mean().iloc[-1]
    return ma2

#캔들 봉 체크 할때 datetime.timedelta hours 교체 필수
def get_delay_ma2(ticker):
    """하루 전 2일 이동 평균선 조회"""
    timegap5 = datetime.datetime.now() - datetime.timedelta(hours=4)
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=2, to = str(timegap5))
    d_ma2 = df['close'].rolling(2).mean().iloc[-1]
    return d_ma2

#캔들 봉 체크 할때 datetime.timedelta hours 교체 필수
def get_delay_delay_ma2(ticker):
    """이틀 전 2일 이동 평균선 조회"""
    timegap5 = datetime.datetime.now() - datetime.timedelta(hours=8)
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=2, to = str(timegap5))
    d_d_ma2 = df['close'].rolling(2).mean().iloc[-1]
    return d_d_ma2

#일봉의 5일 이동 평균선 조회
def get_ma5(ticker):
    """5일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=5)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5


#일봉의 20일 이동 평균선 조회
def get_ma20(ticker):
    """20일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20


def find_ma2_change_flow():
    for i in range(0,104,1):
        print(str(coinname[i]))
        #이틀 전의 2일 이동평균선을 찾음
        d_d_ma2 = get_delay_delay_ma2("KRW-"+str(coinname[i]))
        #하루 전의 2일 이동평균선을 찾음
        d_ma2 = get_delay_ma2("KRW-"+str(coinname[i]))
        #오늘의 3일 이동평균선을 찾음
        ma2 = get_ma2("KRW-"+str(coinname[i]))
        
        ma5 = get_ma5("KRW-"+str(coinname[i]))
        ma20= get_ma20("KRW-"+str(coinname[i]))

        time.sleep(0.3)
        if ma5 > ma20*1.02:
            if d_d_ma2 > d_ma2:
                if ma2>d_ma2:
                    print("금일 5이평선이 20이평선보다 위에 존재함")
                    attentioncoin.append(str(coinname[i]))

def buying_time():
    #하루의 기준인 오전 9시를 가져옴
    stand = get_start_time("KRW-BTC")
    #계산을 위한 시간 설정
    start_time = stand
    #익일 09시 10분 전 
    reset_start_time  = stand +datetime.timedelta(minutes=1430)
    #익일 09시
    reset_end_time = stand +datetime.timedelta(minutes=1440)
    now = datetime.datetime.now()
    #익일 08시 50분 ~ 08시 59분
    if reset_start_time < now < reset_end_time:
        return 1
    #초기화 이외의 시간
    else:
        return 2

def find_high_value_coin():
    #BTC 최근 200시간의 데이터 불러옴
    e=[]
    e={}
    e1={}
    for i in range(0,104,1):
        df = pyupbit.get_ohlcv("KRW-"+str(coinname[i]), interval="day", count = 1)
        e[str(coinname[i])]= df.iloc[-1]['value']
        time.sleep(0.3)
    
    e1= sorted(e.items(), key=operator.itemgetter(1), reverse=True)
    for k in range(0,15,1):
        high_value_coin.append(str(e1[k][0]))





access = ""
secret = ""


coinname =["DOGE","NEAR","WEMIX","JST","SAND","XRP","SBD","SNT","SXP","STRK",
      "POWR","MED","CBK","SOL","ETC","ADA","BORA","LINK","ATOM","XLM",
      "KAVA","STX","MANA","ALGO","DOT","PLA","VET","OMG","EOS","RFR",
      "1INCH","BTG","FLOW","NU","BAT","TRX","QTUM","LTC","LSK","IQ",
      "AQT","AXS","ORBS","HUM","SRM","ICX","STORJ","HUNT","XTZ","HIVE",
      "WAXP","HBAR","ANKR","ELF","NEO","AAVE","CHZ","SC","DAWN","ARDR",
      "ZIL","MOC","DKA","ENJ","TON","BCH","STPT","STEEM","TT","CVC",
      "XEM","META","CRO","MTL","KNC","SSX","MBL","POLY","WAVES","THETA",
      "IOTA","UPP","STMX","TFUEL","ZRX","BSV","STRAX","MVL","MFT","ONT",
      "AERGO","GRS","PUNDIX","CRE","REP","GLM","LOOM","ONG","FCT2","ARK",
      "IOST","AHT","GAS","QKC"]

attentioncoin=[]
bought_coin=[]
high_value_coin=[]


upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
krw = get_balance("KRW")
lastbuyprice = 0


while True: 
    try:

        standard = buying_time()

        if standard == 1:
            bought_coin=[]
            krw = get_balance("KRW")


        elif standard == 2:

            find_ma2_change_flow()
            find_high_value_coin()
            gettable_coin = list(set(attentioncoin) - set(bought_coin))
            final_gettable_coin=list(set(gettable_coin) & set(high_value_coin))

            print("gettable coin")
            print(gettable_coin)
            print("final gettable coin")
            print(final_gettable_coin)
            
            print("변동성을 돌파한 코인")
           
            for i in final_gettable_coin:
                print(str(i))
                bestk = find_bestk("KRW-"+str(i))

                target_price = get_target_price("KRW-"+str(i), bestk)
                current_price = get_current_price("KRW-"+str(i))

                #현재가격이 타킷가격보다 1%이상 높으면 매수 금지하는 조건 추가할 것.
                
                orderbook = pyupbit.get_orderbook("KRW-"+str(i))
                #ask== 매도
                total_ask_size = orderbook['total_ask_size']
                #bid == 매수
                total_bid_size = orderbook['total_bid_size']
                if current_price < target_price:
                    if total_ask_size > total_bid_size*1.2:
                        if get_balance("KRW") > 5000:
                            upbit.buy_market_order("KRW-"+str(i), krw*0.9995)
                            bought_coin.append(str(i))
                   
                time.sleep(10)

                while (get_balance(str(i))!=0):
                    print("--------------변동성 돌파 보유중------------------")
                    #4시간 봉을 통해서 ma2의 추세가 꺽이게 되면 바로 매도

                    if get_current_price("KRW-"+str(coinname[i])) > ((upbit.get_avg_buy_price("KRW-"+str(coinname[i])))*1.02):
                        print(0)
                        btc = get_balance(str(coinname[i]))
                        upbit.sell_market_order("KRW-"+str(coinname[i]), btc)
                        
                        
        else:
            print("rest time")
    

    except Exception as e:
        print(e)
        time.sleep(1)
