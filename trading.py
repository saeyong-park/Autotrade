import time
import pyupbit
import datetime
import schedule
import numpy as np

def get_upper_down_rate(ticker, lastbuyprice):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_price = df.iloc[0]['open']
    rate =  ((get_current_price(ticker)-lastbuyprice)/lastbuyprice)*100

    return rate

def get_ror(ticker,k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=7)
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
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
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
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    ma2 = df['close'].rolling(2).mean().iloc[-1]
    return ma2

def get_delay_ma2(ticker):
    """하루 전 2일 이동 평균선 조회"""
    timegap5 = datetime.datetime.now() - datetime.timedelta(days=1)
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2, to = str(timegap5))
    d_ma2 = df['close'].rolling(2).mean().iloc[-1]
    return d_ma2

def get_delay_delay_ma2(ticker):
    """이틀 전 2일 이동 평균선 조회"""
    timegap5 = datetime.datetime.now() - datetime.timedelta(days=2)
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2, to = str(timegap5))
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
        if ma5 > ma20*1.05:
            if d_d_ma2 > d_ma2:
                if ma2 > d_ma2:
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




access = "E6vAoAxPan8FNkelHFxluymY4SA3FX9SAn7phYC1"
secret = "dJHARvi0ZrZ4kIJ6UYkTWTX9CmzPFadQmzB6DLMi"


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

upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
krw = get_balance("KRW")/3
lastbuyprice = 0



standard = buying_time()

if standard == 1:
    bought_coin=[]
    krw = get_balance("KRW")/3


elif standard == 2:

    find_ma2_change_flow()
    gettable_coin = list(set(attentioncoin) - set(bought_coin))


    print("m5>m20*1.05 and d_d_ma2 > d_ma2 and d_ma2 < ma2 조건 만족")
    print(gettable_coin)
    for i in gettable_coin:
        bestk = find_bestk("KRW-"+str(i))

        target_price = get_target_price("KRW-"+str(i), bestk)
        current_price = get_current_price("KRW-"+str(i))

        #현재가격이 타킷가격보다 1%이상 높으면 매수 금지하는 조건 추가할 것.
        if current_price > target_price:
            orderbook = orderbook = pyupbit.get_orderbook("KRW-"+str(i))
            #ask== 매도
            total_ask_size = orderbook['total_ask_size']
            #bid == 매수
            total_bid_size = orderbook['total_bid_size']
            if total_ask_size > total_bid_size*1.2 and total_ask_size < total_bid_size*2:
                bought_coin.append(str(i))



print("최종 후보군")
print(bought_coin)
    
