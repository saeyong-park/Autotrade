import time
import pyupbit
import datetime
import schedule

access = ""
secret = ""


coinname = ["BTC","ETH","BCH","AAVE","LTC","SOL","BSV","AVAX","AXS","STRK",
"BTG","ETC","ATOM","NEO","DOT","LINK","REP","NEAR","QTUM","WAVES",
"FLOW","WEMIX","GAS","SBD","OMG","TON","XTZ","KAVA","SAND","THETA",
"MANA","AQT","HUNT","ONG","PUNDIX","XRP","IOTA","BAT","ZRX","POWR",
"GLM","NU","META","ORBS","ANKR","TRX","SNT","VET","JST","TT",
"CRE","MFT","MBL","XEC"]


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

def get_ma5(ticker):
    """5일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=5)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5

def get_ma10(ticker):
    """10일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=10)
    ma10 = df['close'].rolling(10).mean().iloc[-1]
    return ma10

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_ma25(ticker):
    """25일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=25)
    ma25 = df['close'].rolling(25).mean().iloc[-1]
    return ma25

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price     
                              

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

def get_upper_down_rate(ticker, lastbuyprice):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_price = df.iloc[0]['open']
    rate =  ((get_current_price(ticker)-lastbuyprice)/lastbuyprice)*100

    return rate

def short_trading(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute15", count=10)
    ma_5 = get_ma5(ticker)
    ma_10 = get_ma10(ticker)
    ma_15 = get_ma15(ticker)
    ma_25 = get_ma25(ticker)
    print(ma_5)
    print(ma_10)
    print(ma_15)
    print(ma_25)

    if get_current_price(ticker) > df.iloc[-3]['close']:
        if ma_10 *1.1 > ma_5 > ma_10*1.03:
            if ma_15 *1.1 > ma_10 > ma_15*1.01:
                if ma_25 *1.1 > ma_15 > ma_25*1.01:
                    if ma_5 > ma_10 and ma_10 > ma_15  and ma_15 > ma_25 :
                        return 1
                
    return 0



# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
krw = get_balance("KRW")/3
lastbuyprice = 0
while True:
    for i in range(0,54,1):
        
        try:
            krw = get_balance("KRW")/3
            now = datetime.datetime.now()
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
            seventh_end_time = stand +datetime.timedelta(minutes=1429)

            
            print(str(coinname[i]))
            lastbuyprice = 0
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
                    print("eeeeeeeeee")
                    #변동성 돌파 전략의 전략 가격< 현재 가격
                    if short_trading("KRW-"+str(coinname[i])) == 1:
                        if krw > 5000:
                            upbit.buy_market_order("KRW-"+str(coinname[i]), krw)
                            lastbuyprice = get_current_price("KRW-"+str(coinname[i]))

                    while (get_balance(str(coinname[i]))!=0):
                        print("--------------변동성 돌파 보유중------------------")
                        #현재 가격이 평균구매가격보다 1% 높은 경우 매도
                        if get_current_price("KRW-"+str(coinname[i])) > ((upbit.get_avg_buy_price("KRW-"+str(coinname[i])))*1.01):
                            btc = get_balance(str(coinname[i]))
                            upbit.sell_market_order("KRW-"+str(coinname[i]), btc)
                            #매도후 30분의 대기를 통해서 한번의 거래만 이루어질 수 있도록 조절
                            time.sleep(1800)
                         
                        #현재가격이 평균구매가격보다 -2%인 경우 매도
                        if get_current_price("KRW-"+str(coinname[i])) < upbit.get_avg_buy_price("KRW-"+str(coinname[i]))*0.98:
                            btc = get_balance(str(coinname[i]))
                            upbit.sell_market_order("KRW-"+str(coinname[i]), btc)
                            #매도후 30분의 대기를 통해서 한번의 거래만 이루어질 수 있도록 조절
                            time.sleep(1800)
               
            while (get_balance(str(coinname[i]))!=0):
                print("--------------240분봉 보유중------------------")
                if get_current_price("KRW-"+str(coinname[i])) > ((upbit.get_avg_buy_price("KRW-"+str(coinname[i])))*1.007):
                    print(1)
                    btc = get_balance(str(coinname[i]))
                    upbit.sell_market_order("KRW-"+str(coinname[i]), btc)
                elif get_upper_down_rate("KRW-"+str(coinname[i]), lastbuyprice) > 1:
                    print(3)
                    upbit.sell_market_order("KRW-"+str(coinname[i]),krw)          

                
                if get_current_price("KRW-"+str(coinname[i])) < upbit.get_avg_buy_price("KRW-"+str(coinname[i]))*0.985:
                    now = datetime.datetime.now()
                    if second_start_time < now < second_end_time:
                        if get_balance("KRW") > 5000:
                            upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                            lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                    #16시 50분 ~ 16시 59분
                    elif third_start_time < now < third_end_time:
                        if get_balance("KRW") > 5000:
                            upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                            lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                    #20시 50분 ~ 20시 59분
                    elif fourth_start_time < now < fourth_end_time:
                        if get_balance("KRW") > 5000:
                            upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                            lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                    #익일 00시 50분 ~ 00시 59분
                    elif fifth_start_time < now < fifth_end_time:
                        if get_balance("KRW") > 5000:
                            upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                            lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                    #익일 04시 50분 ~ 04시 59분
                    elif sixth_start_time < now < sixth_end_time:
                        if get_balance("KRW") > 5000:
                            upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                            lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                    #익일 08시 50분 ~ 08시 59분
                    elif seventh_start_time < now < seventh_end_time:
                        if get_balance("KRW") > 5000:
                            upbit.buy_market_order("KRW-"+str(coinname[i]), krw*0.9995)
                            lastbuyprice = get_current_price("KRW-"+str(coinname[i]))
                    #이외의 시간
                    else:
                        print("1")

        
            time.sleep(1)    

        except Exception as e:
            print(e)
            time.sleep(1)
