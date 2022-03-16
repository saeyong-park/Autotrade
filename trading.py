import time
import pyupbit
import datetime
import schedule


access = ""
secret = ""

coinname =["DOGE","NEAR","WEMIX","BTC","SAND","XRP","ETH","SNT","SXP","MATIC",
      "POWR","MED","CBK","SOL","ETC","ADA","BORA","LINK","ATOM","XLM",
      "KAVA","STX","MANA","ALGO","DOT","PLA","VET","OMG","EOS","RFR",
      "1INCH","BTG","FLOW","NU","BAT","TRX","QTUM","LTC","MLK","IQ",
      "AQT","AXS","ORBS","HUM","SRM","ICX","STORJ","HUNT","XTZ","HIVE",
      "WAXP","HBAR","ANKR","ELF","NEO","AAVE","CHZ","SC","DAWN","ARDR",
      "ZIL","MOC","DKA","ENJ","TON","BCH","STPT","STEEM","TT","CVC",
      "XEM","META","CRO","MTL","KNC","SSX","MBL","POLY","WAVES","THETA",
      "IOTA","UPP","STMX","TFUEL","ZRX","BSV","STRAX","MVL","MFT","ONT",
      "AERGO","GRS","PUNDIX","CRE","REP","GLM","LOOM","ONG","FCT2","ARK",
      "IOST","AHT","GAS","QKC","STRK","JST","SBD","LSK"]

def get_upper_down_rate(ticker, lastbuyprice):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_price = df.iloc[0]['open']
    rate =  ((get_current_price(ticker)-lastbuyprice)/lastbuyprice)*100

    return rate


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

#5일 이평선이 20일 이평선을 돌파했는지 확인하고 양봉이면 집입
def get_delay_ma5(ticker):
    """5일 이동 평균선 조회"""
    timegap5 = datetime.datetime.now() - datetime.timedelta(days=1)
    df = pyupbit.get_ohlcv(ticker, interval="day", count=5, to = str(timegap5))
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5

def get_delay_ma20(ticker):
    """20일 이동 평균선 조회"""
    timegap20 = datetime.datetime.now() - datetime.timedelta(days=1)
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20, to = str(timegap20))
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20

def buy_strategy(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count = 10)
    count= 0
    gap = 0 
    total = 0
    lastestclose = 0
    for i in range(0,7,1):
        #양봉이면서 윗꼬리가 종가의 2%를 넘어가지 않는 것을 카운트 양보으로 취급함
        if df.iloc[i]['close']-df.iloc[i]['open'] > 0 and df.iloc[i]['high'] < df.iloc[i]['close']*1.02:
            
            if df.iloc[i+1]['close']-df.iloc[i+1]['open'] < 0:
                count= 0
                gap = 0 
                total = 0
                print(str(i)+"번째 봉 ")
                for j in range(i+2,10,1):
                    #음봉에 해당하는 경우
                    lastestclose = df.iloc[j-1]['close']
                    
                    if df.iloc[j]['close']-df.iloc[j]['open'] < 0 and df.iloc[j]['open']<lastestclose*1.015  :
                        lastestclose = df.iloc[j]['close']
                        if df.iloc[j]['high']< df.iloc[j-1]['close']*1.03:
                            #첫번째에 해당하는 경우
                            if count == 0:
                                gap = df.iloc[j]['close']-df.iloc[j]['open']
                                count +=1
                                print("1")
                                print(str(gap))

                            #첫번째가 아닌 경우
                            else:
                                #첫번째 기준에 해당하는 경우
                                if df.iloc[j]['close']-df.iloc[j]['open'] < gap*0.8 :
                                    print("2")
                                    count += 1
                                    total = 0
                                #첫번째 기준에 해당하지 않는 경우
                                else:
                                    total += df.iloc[j]['close']-df.iloc[j]['open']
                                    # 앞의 합을 더한 것이 기준을 넘는 경우
                                    print("total = "+ str(total))
                                    if total < gap*0.8:
                                        count +=1
                                        total = 0
                        else:
                            print("음봉이지만 윗꼬리가 길어서 힘을 소진")
                            count=0
                            total=0
                            break

                    #양봉에 해당하는 경우
                    else:
                        if df.iloc[j]['open'] - df.iloc[j]['close'] < (df.iloc[j-1]['close'] - df.iloc[j-1]['open'])*0.4 and df.iloc[j]['open'] - df.iloc[j]['close'] < gap*0.3 :
                            print("기준 음봉을 넘어서는 양봉")
                            count=0
                            total=0
                            break
                        else:
                            if df.iloc[j]['high']< df.iloc[j-1]['close']*1.03:
                                ("양봉이지만 윗꼬리가 길어서 힘을 소진")
                                count=0
                                total=0
                                break
                            else:
                                print("무시가능")

                    print("count=" +str(count)) 

                   
    return count



# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
krw = get_balance("KRW")/3
while True:
      for i in range(0,108,1): 
            
            try:
                  print(str(coinname[i]))

                  #하루의 기준인 오전 9시를 가져옴
                  stand = get_start_time("KRW-"+str(coinname[i]))
                  #변동성 돌파 전략을 사용할 시간을 정함
                  #오전 9시로부터 5분(시작 시간)
                  start_time = stand
                  #오전 9시로부터 10분(끝나는 시간)
                  end_time = stand + datetime.timedelta(minutes=15)
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
                  #익일 09시 1분 전
                  seventh_end_time = stand +datetime.timedelta(minutes=1439)

                  now = datetime.datetime.now()
                
                  #12시 50분 ~ 12시 59분
                  if second_start_time < now < second_end_time:
                        if buy_strategy("KRW-"+str(coinname[i])) > 1:
                              print("--------------매수 조건 충족--------------")
                              if get_balance("KRW") > 5000:
                                    upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                                    lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                   
                  #16시 50분 ~ 16시 59분
                  elif third_start_time < now < third_end_time:
                        if buy_strategy("KRW-"+str(coinname[i])) > 1:
                              print("--------------매수 조건 충족--------------")
                              if get_balance("KRW") > 5000:
                                    upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                                    lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
               
                  #20시 50분 ~ 20시 59분
                  elif fourth_start_time < now < fourth_end_time:
                        if buy_strategy("KRW-"+str(coinname[i])) > 1:
                              print("--------------매수 조건 충족--------------")
                              if get_balance("KRW") > 5000:
                                    upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                                    lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
             
                  #익일 00시 50분 ~ 00시 59분
                  elif fifth_start_time < now < fifth_end_time:
                        if buy_strategy("KRW-"+str(coinname[i])) > 1:
                              print("--------------매수 조건 충족--------------")
                              if get_balance("KRW") > 5000:
                                    upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                                    lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                 
                  #익일 04시 50분 ~ 04시 59분
                  elif sixth_start_time < now < sixth_end_time:
                        if buy_strategy("KRW-"+str(coinname[i])) > 1:
                              print("--------------매수 조건 충족--------------")
                              if get_balance("KRW") > 5000:
                                    upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                                    lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                     
                  #익일 08시 50분 ~ 08시 59분
                  elif seventh_start_time < now < seventh_end_time:
                        if buy_strategy("KRW-"+str(coinname[i])) > 1:
                              print("--------------매수 조건 충족--------------")
                              if get_balance("KRW") > 5000:
                                    upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                                    lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                       
                  #이외의 시간
                  else:
                  
                        #금일의 5일 이동평균선을 구함
                        ma_5 =  get_ma5("KRW-"+str(coinname[i]))
                        #금일의 20일 이동평균선을 구함
                        ma_20 = get_ma20("KRW-"+str(coinname[i]))

                        #전일의 5일 이동평균선을 구함
                        d_ma_5 = get_delay_ma5("KRW-"+str(coinname[i]))
                        #전일의 20일 이동편균선을 구함
                        d_ma_20 = get_delay_ma20("KRW-"+str(coinname[i]))
                        time.sleep(1)
                  
                        if d_ma_5 < d_ma_20:
                              print("전일 5이평선이 20일이평선보다 밑에 존재함")
                              if ma_5 >= ma_20*1.01:
                                    print("금일 5이평선이 20이평선보다 위에 존재함")
                                    if krw > 5000:
                                          upbit.buy_market_order("KRW-"+str(coinname[i]), krw)
                                          lastbuyprice = get_current_price("KRW-"+str(coinname[i]))


                                          while (get_balance(str(coinname[i]))!=0):
                                                print("--------------변동성 돌파 보유중------------------")
                                                #현재 가격이 평균구매가격보다 2% 높은 경우 매도
                                                if get_current_price("KRW-"+str(coinname[i])) > ((upbit.get_avg_buy_price("KRW-"+str(coinname[i])))*1.02):
                                                      btc = get_balance(str(coinname[i]))
                                                      upbit.sell_market_order("KRW-"+str(coinname[i]), btc)
                            
                         
                                                #현재가격이 평균구매가격보다 -1%인 경우 매도
                                                if get_current_price("KRW-"+str(coinname[i])) < upbit.get_avg_buy_price("KRW-"+str(coinname[i]))*0.99:
                                                      btc = get_balance(str(coinname[i]))
                                                      upbit.sell_market_order("KRW-"+str(coinname[i]), btc)
                                    else:
                                          print("잔액 부족")
                              else:
                                    print("ee")
                        else:
                              print("e")
                  
                  while (get_balance(str(coinname[i]))!=0):
                        print("--------------240분봉 보유중------------------")
                        if get_current_price("KRW-"+str(coinname[i])) > ((upbit.get_avg_buy_price("KRW-"+str(coinname[i])))*1.01):
                              print(1)
                              btc = get_balance(str(coinname[i]))
                              upbit.sell_market_order("KRW-"+str(coinname[i]), btc)
                        elif get_upper_down_rate("KRW-"+str(coinname[i]), lastbuyprice) > 1:
                              print(3)
                              upbit.sell_market_order("KRW-"+str(coinname[i]),krw)          

                
                        if get_current_price("KRW-"+str(coinname[i])) < upbit.get_avg_buy_price("KRW-"+str(coinname[i]))*0.985:
                              now = datetime.datetime.now()
                              #12tl 50분 ~ 12시 59분
                              if second_start_time < now < second_end_time:
                                    if get_balance("KRW") > 5000:
                                          upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                                          lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                                          time.sleep(600)
                              #16시 50분 ~ 16시 59분
                              elif third_start_time < now < third_end_time:
                                    if get_balance("KRW") > 5000:
                                          upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                                          lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                                          time.sleep(600)
                              #20시 50분 ~ 20시 59분
                              elif fourth_start_time < now < fourth_end_time:
                                    if get_balance("KRW") > 5000:
                                          upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                                          lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                                          time.sleep(600)
                              #익일 00시 50분 ~ 00시 59분
                              elif fifth_start_time < now < fifth_end_time:
                                    if get_balance("KRW") > 5000:
                                          upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                                          lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                                          time.sleep(600)
                              #익일 04시 50분 ~ 04시 59분
                              elif sixth_start_time < now < sixth_end_time:
                                    if get_balance("KRW") > 5000:
                                          upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                                          lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                                          time.sleep(600)
                              #익일 08시 50분 ~ 08시 59분
                              elif seventh_start_time < now < seventh_end_time:
                                    if get_balance("KRW") > 5000:
                                          upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                                          lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                                          time.sleep(600)
                              #이외의 시간
                              else:
                                    print("1")                
                  
            
            except Exception as e:
                  print(e)
                  time.sleep(1)
