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

def find_bestk(ticker):
  for k in range(0.1, 1.0, 0.1):
    df = pyupbit.get_ohlcv(ticker, count=7)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)

    ror = df['ror'].cumprod()[-2]

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
    ma10 = df['close'].rolling(20).mean().iloc[-1]
    return ma10
def get_delay_ma3(ticker):
    """3일 이동 평균선 조회"""
    timegap5 = datetime.datetime.now() - datetime.timedelta(days=1)
    df = pyupbit.get_ohlcv(ticker, interval="day", count=3, to = str(timegap5))
    ma3 = df['close'].rolling(3).mean().iloc[-1]
    return ma3

#하루전 일봉의 5일 이동 평균선 조회
def get_delay_ma5(ticker):
    """5일 이동 평균선 조회"""
    timegap5 = datetime.datetime.now() - datetime.timedelta(days=1)
    df = pyupbit.get_ohlcv(ticker, interval="day", count=5, to = str(timegap5))
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5


#하루전 일봉의 20일 이동 평균선 조회
def get_delay_ma20(ticker):
    """20일 이동 평균선 조회"""
    timegap20 = datetime.datetime.now() - datetime.timedelta(days=1)
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20, to = str(timegap20))
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20
    
def get_delay_delay_ma3(ticker):
    """5일 이동 평균선 조회"""
    timegap5 = datetime.datetime.now() - datetime.timedelta(days=2)
    df = pyupbit.get_ohlcv(ticker, interval="day", count=3, to = str(timegap5))
    ma3 = df['close'].rolling(3).mean().iloc[-1]
    return ma3

def find_ma2_change_flow():
    for i in range(0,104,1):
        print(str(coinname[i]))
        #이틀 전의 3일 이동평균선을 찾음
        d_d_ma2 = get_delay_delay_ma2("KRW-"+str(coinname[i]))
        #하루 전의 3일 이동평균선을 찾음
        d_ma2 = get_delay_ma2("KRW-"+str(coinname[i]))
        #오늘의 3일 이동평균선을 찾음
        ma2 = get_ma2("KRW-"+str(coinname[i]))
        
        ma5 = get_ma5("KRW-"+str(coinname[i]))
        ma20= get_ma5("KRW-"+str(coinname[i]))

        time.sleep(0.3)
        if ma5 > ma20:
            if d_d_ma2 > d_ma2:
                if ma2 > d_ma2:
                    print("금일 5이평선이 20이평선보다 위에 존재함")
                    attentioncoin.append(str(coinname[i]))

def buying_time():
    #하루의 기준인 오전 9시를 가져옴
    stand = get_start_time("KRW-BTC")
    #변동성 돌파 전략을 사용할 시간을 정함
    #오전 9시로부터 5분(시작 시간)
    start_time = stand
    #오전 9시로부터 20분(끝나는 시간)
    end_time = stand + datetime.timedelta(minutes=30)
    #13시 10분 전
    second_start_time  = stand +datetime.timedelta(minutes=230)
    #13시 1분 전
    second_end_time = stand +datetime.timedelta(minutes=239)
    #17시 10분 전
    third_start_time  = stand +datetime.timedelta(minutes=470)
    #17시 1분 전
    third_end_time = stand +datetime.timedelta(minutes=479)
    #21시 10분 전
    fourth_start_time  = stand +datetime.timedelta(minutes=710)
    #21시 1분 전
    fourth_end_time = stand +datetime.timedelta(minutes=719)
    #익일 01시 10분 전
    fifth_start_time  = stand +datetime.timedelta(minutes=950)
    #익일 01시 1분 전
    fifth_end_time = stand +datetime.timedelta(minutes=959)
    #익일 05시 10분 전 
    sixth_start_time  = stand +datetime.timedelta(minutes=1190)
    #익일 05시 1분 전
    sixth_end_time = stand +datetime.timedelta(minutes=1199)
    #익일 09시 10분 전 
    seventh_start_time  = stand +datetime.timedelta(minutes=1430)
    #익일 09시 4분 전
    seventh_end_time = stand +datetime.timedelta(minutes=1436)
    #익일 09시 2분 전 
    eighth_start_time  = stand +datetime.timedelta(minutes=1438)
    #익일 09시
    eighth_end_time = stand +datetime.timedelta(minutes=1440)
    now = datetime.datetime.now()
 
    #12시 50분 ~ 12시 59분
    if second_start_time < now < second_end_time:
        return 1
    #16시 50분 ~ 16시 59분
    elif third_start_time < now < third_end_time:
        return 1
    #20시 50분 ~ 20시 59분
    elif fourth_start_time < now < fourth_end_time:
        return 1                        
    #익일 00시 50분 ~ 00시 59분
    elif fifth_start_time < now < fifth_end_time:
        return 1
    #익일 04시 50분 ~ 04시 59분
    elif sixth_start_time < now < sixth_end_time:                     
        return 1
    #익일 08시 50분 ~ 08시 59분
    elif seventh_start_time < now < seventh_end_time:
        return 1
    #Bought_coin 리스트 초기화 시간
    elif eighth_start_time < now < eighth_end_time:
        return 2
    #ma5_over_ma20 시간
    else:
        return 3





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

def find_ma5_over_ma20():
    for i in range(0,104,1):
        print(str(coinname[i]))
        #금일의 5일 이동평균선을 구함
        ma_5 =  get_ma5("KRW-"+str(coinname[i]))
        #금일의 20일 이동평균선을 구함
        ma_20 = get_ma20("KRW-"+str(coinname[i]))
        #전일의 5일 이동평균선을 구함
        d_ma_5 = get_delay_ma5("KRW-"+str(coinname[i]))
        #전일의 20일 이동편균선을 구함
        d_ma_20 = get_delay_ma20("KRW-"+str(coinname[i]))
        time.sleep(0.3)
        
        if d_ma_5 < d_ma_20:
            if ma_5 >= ma_20:
                print("금일 5이평선이 20이평선보다 위에 존재함")
                attentioncoin.append(str(coinname[i]))
        else:
            print("e")


attentioncoin=[]
coinwallet=[]
bought_coin=[]


upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
krw = get_balance("KRW")/3
lastbuyprice = 0

while True: 
    try:

        standard = buying_time()

        if standard == 2:
            bought_coin=[]
            krw = get_balance("KRW")/3


        elif standard == 3:

            find_ma5_over_ma20()
            gettable_coin = list(set(attentioncoin) - set(bought_coin))

            for i in gettable_coin:
                bestk = find_bestk(i)
                target_price = get_target_price("KRW-"+str(i), bestk)
                current_price = get_current_price("KRW-"+str(i))
                if current_price > target_price:
                    print("구매가능")
                    if get_balance("KRW") > 5000:
                        upbit.buy_market_order("KRW-"+str(i), krw*0.9995)
                        bought_coin.append("KRW-"+str(i))
                        time.sleep(1)
                        
            
                    while (get_balance(str(i))!=0):
                        print("--------------변동성 돌파 보유중------------------")
                        #현재 가격이 평균구매가격보다 3% 높은 경우 매도
                        ma2 = get_ma("KRW-"+str(i))
                        if get_current_price("KRW-"+str(i)) > ((upbit.get_avg_buy_price("KRW-"+str(i)))*1.03):
                            btc = get_balance(str(coinname[i]))
                            upbit.sell_market_order("KRW-"+str(i), btc)
                
                        elif ma2 < get_current_price("KRW-"+str(i)):
                            btc = get_balance(str(i))
                            upbit.sell_market_order("KRW-"+str(i), btc)



        else:
            print("rest time")
    

    except Exception as e:
        print(e)
        time.sleep(1)
