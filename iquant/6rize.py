#coding:gbk
import time, os, gc, datetime,math
import numpy as np
import pandas as pd
import logging
import talib as ta
import gc

def getMarketCode(strCode):
    if (strCode[0:1] == "6"):
        return strCode + ".SH"
    else:
        return strCode + ".SZ"

def getKeyFromDict(dict, value):
    myfilters = filter(lambda x: value== x[1], dict.items())
    ret = []
    for (key,value) in myfilters:
        ret.append(key)
    return ret

def printBothDebug(information):
    print(information)
    logging.debug(information)
    
def printBoth(information):
    print(information)
    logging.info(information)

def resetHolding(ContextInfo):
    ContextInfo.bought_num = 0
    ContextInfo.boughtkeys = []
    ContextInfo.holdings = {i:0 for i in ContextInfo.s}
    ContextInfo.boughtday = {i:0 for i in ContextInfo.s}
    ContextInfo.buypoint = {}

def personalize():
    pd.set_option('display.max_columns', None)
    pd.options.mode.chained_assignment = None
    os.chdir("C:/StockAnalysis/iquant")
    log = "6rize_"+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".log"
    if (ContextInfo.do_back_test):
        logging.basicConfig(filename=log,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    else:
        logging.basicConfig(filename=log,level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    logging.info('Start to Log.')
    

def init(ContextInfo):
    personalize()
    
    #设置日期字典
    ContextInfo.predate = 19000101
    ContextInfo.dateDict = {}
    ContextInfo.dateindex = 0
    
    
    
    if (ContextInfo.do_back_test):
        logging.info('Do back test:')
        ContextInfo.buydate = pd.DataFrame()
    else:
        #持仓股票的买入日期
        ContextInfo.buydate = pd.read_csv("buydate.csv", index_col=False)
        ContextInfo.capital = 100000
    printBoth("Period:   " + str(ContextInfo.period))
    #设置Universe
    #ContextInfo.s = ContextInfo.get_sector('000050.SH')
    #ContextInfo.s = ContextInfo.get_stock_list_in_sector('沪深300')
    stock1 = ContextInfo.get_stock_list_in_sector('沪深300')
    #logging.debug("HS300")
    #logging.debug(stock1)
    stock2 = ContextInfo.get_stock_list_in_sector('中证500')
    #logging.debug("ZZ500")
    #logging.debug(stock2)
    ContextInfo.s = stock1 + stock2
    #ContextInfo.s = ContextInfo.get_stock_list_in_sector('沪深A股')
    ContextInfo.set_universe(ContextInfo.s)
    ContextInfo.holding_num = 7
    ContextInfo.buy_num_perday = 3
    printBoth("Total Holding Number:   " + str(ContextInfo.holding_num))
    ContextInfo.myfee = 0.0003
    ContextInfo.money = ContextInfo.capital
    resetHolding(ContextInfo)
    ContextInfo.accountID='416600037920'
    printBoth("Initial Money:"+str(ContextInfo.money))


def stop(ContextInfo):
    print("Enter Shutdonw")
    logging.info("Enter Shutdown")
    logging.shutdown()

def printTradeDetail(ContextInfo, showlog):
    if (showlog):
        logging.info("******************************************************************************************")
        logging.info("Account Information - PrintTradeDetail")
    resetHolding(ContextInfo)
    obj_list = get_trade_detail_data(ContextInfo.accountID, 'stock', 'position')
    for obj in obj_list:
        if (obj.m_nVolume < 100):
            continue
        codeKey = getMarketCode(obj.m_strInstrumentID)
        ContextInfo.bought_num +=1
        ContextInfo.buypoint[codeKey] = obj.m_dOpenPrice
        if (ContextInfo.do_back_test):
            tradeDate = obj.m_strOpenDate
        else:
            df = ContextInfo.buydate
            tradeDate = df[df['code'] == codeKey]["buydate"].iloc[0]
        if (len(str(tradeDate))) < 4:
            tradeDate = int(datetime.date.today().strftime('%Y%m%d'))
        ContextInfo.boughtday[codeKey] = int(tradeDate)
        ContextInfo.holdings[codeKey] = obj.m_nVolume
        dateindex = ContextInfo.dateDict[int(tradeDate)]
        if (showlog):
            logging.info("ID " + codeKey + " WITH buy price " + str(obj.m_dOpenPrice) + "-- buy date:" + str(tradeDate) + "("+str(dateindex)+") -- buy quantity " + str(obj.m_nVolume))
        ContextInfo.boughtkeys.append(codeKey)
    if (showlog):
        logging.info("*********")
        logging.info('Holding stock num :  ' + str(ContextInfo.bought_num))
    acct_info = get_trade_detail_data(ContextInfo.accountID, 'stock', 'account')
    for i in acct_info:
        ContextInfo.money = i.m_dAvailable
        if (showlog):
            logging.info("Left Money in system:" + str(i.m_dAvailable))
            logging.info("Account balance:" + str(i.m_dBalance))
    if (showlog):
        logging.info("******************************************************************************************")

def getBoughtMoney(ContextInfo):
    sharenum = ContextInfo.holding_num - ContextInfo.bought_num
    return ContextInfo.money / sharenum

def account_callback(ContextINfo, accountInfo):
    printBoth('come into call back function accountInfo')
    logging.info("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    printBoth(accountInfo.m_strStatus)


def doBuy(ContextInfo, buyday, buyKey, buyprice):
    logging.info('goto buy function ' + str(buyKey))
    if (ContextInfo.bought_num >= ContextInfo.holding_num or ContextInfo.holdings[buyKey] > 0):
        logging.info('Bought enough or already bought, exit')
        return
    nowDate = timetag_to_datetime(ContextInfo.get_bar_timetag(ContextInfo.barpos),'%Y%m%d')
    printBoth(str(nowDate) + ' ready to buy: ' + str(buyKey) + " with price   " + str(buyprice))
    orderQuantity = int((getBoughtMoney(ContextInfo)/ (buyprice * (1 + ContextInfo.myfee + 0.0002)) ) /100)
    logging.debug('Get Money  ' + str(getBoughtMoney(ContextInfo)))
    logging.debug('StockQuantity  ' + str(orderQuantity * 100))
    logging.debug('Buy Price  ' + str(buyprice))
    order_shares(buyKey, int(orderQuantity * 100), 'fix', buyprice, ContextInfo, ContextInfo.accountID)
    printTradeDetail(ContextInfo, False)


def doSell(ContextInfo, sellKey, sellprice):
    logging.info('goto sell function ' + str(sellKey))
    if ContextInfo.holdings[sellKey] < 0.01:
        logging.debug('not hold ' + str(sellKey) + "  and leave the transaction.")
        return
    nowDate = timetag_to_datetime(ContextInfo.get_bar_timetag(ContextInfo.barpos),'%Y%m%d')
    printBoth(str(nowDate) + '-- ready to sell:' + str(sellKey) + " with price  " + str(sellprice) + " and quantity " + str(ContextInfo.holdings[sellKey]))
    order_shares(sellKey,-ContextInfo.holdings[sellKey],'fix',sellprice,ContextInfo,ContextInfo.accountID)
    logging.info("Sell stock " + str(sellKey) + " Done!" )
    printTradeDetail(ContextInfo, False)


def score(ContextInfo, buykey):
    data_close = ContextInfo.get_history_data(3,'1d','close',1)
    data_open = ContextInfo.get_history_data(3,'1d','open',1)
    return (data_open[buykey][-2] / data_close[buykey][-3]) - 1;

def orderBuyKeys(ContextInfo, buykeys):
    maxnum = ContextInfo.buy_num_perday
    nownum = 0
    scores = []
    for buykey in buykeys:
        scores.append(score(ContextInfo, buykey))
        #logging.info("Score for " + buykey + " is " + str(score(ContextInfo, buykey)))
    orderbuy = []
    while (len(scores) > 0):
        nownum = nownum + 1
        if (nownum > maxnum):
            break
        maxid = np.argmax(np.array(scores))
        orderbuy.append(buykeys[maxid])
        scores.pop(maxid)
        buykeys.pop(maxid)
    return orderbuy
    
    
def handlebar(ContextInfo):
    #logging.debug('goto handler bar function ')
    d = ContextInfo.barpos

    nowDate = int(timetag_to_datetime(ContextInfo.get_bar_timetag(d),'%Y%m%d'))
    benchDate = int(datetime.date.today().strftime('%Y%m%d'))
    #benchDate = int(20200914)
    
    if (nowDate > ContextInfo.predate):
        ContextInfo.dateindex +=1
        ContextInfo.dateDict[nowDate] = ContextInfo.dateindex
        ContextInfo.predate = nowDate
        logging.info("******************************************************************************************")
        logging.info("Add date index with date " + str(nowDate) + " and index = " + str(ContextInfo.dateindex))
        logging.debug("barpos:   " + str(d) + " and dateindex " + str(ContextInfo.dateDict[nowDate]) + " and nowdate " + str(nowDate) + " and benchDate " + str(benchDate))
        gc.collect()
    
    if (ContextInfo.do_back_test):
        pass
    else:
        if (benchDate > nowDate):
            return
        else:
            printTradeDetail(ContextInfo, True)


    printBoth("HandlerBar Come into date:   " + str(nowDate))
    buys, sells = signal(ContextInfo, d)
    logging.debug("Buys")
    logging.debug(getKeyFromDict(buys,1))
    logging.debug("Sells")
    logging.debug(getKeyFromDict(sells,1))
    price = ContextInfo.get_history_data(2,'1d','close',1)
    price_open = ContextInfo.get_history_data(2,'1d','open',1)
    order = {}
    for k in list(sells.keys()):
        if (sells[k] > 0):
            sellprice = math.floor(price_open[k][-1] * 100) / 100
            doSell(ContextInfo, k, sellprice)
            #logging.debug("Sell price for " + k + " is " + str(sellprice))
            
    buykeys = getKeyFromDict(buys,1)
    orderBuys = orderBuyKeys(ContextInfo, buykeys)
    for k in orderBuys:
        buyprice1 = math.ceil(price_open[k][-1] * 100) / 100
        buyprice2 = math.ceil(price[k][-2] * 100) / 100
        doBuy(ContextInfo, d, k, min(buyprice1,buyprice2))
        #logging.debug("Buy price for " + k + " is " + str(buyprice))
    if len(orderBuys) > 0:
        printTradeDetail(ContextInfo, True)
    
    if (ContextInfo.is_last_bar()):
        printBoth("Job Done!")

def signal(ContextInfo, day):
    logging.info('goto signal function with signal day ' + str(day))
    buy = {i:0 for i in ContextInfo.s}
    sell = {i:0 for i in ContextInfo.s}

    data_close = ContextInfo.get_history_data(22,'1d','close',1)
    data_open = ContextInfo.get_history_data(22,'1d','open',1)
    data_close_pre = ContextInfo.get_history_data(2,'1d','close',1)
    data_close60 = ContextInfo.get_history_data(200,'1d','close',1)
    #data_open_pre = ContextInfo.get_history_data(2,'1d','open',1)
    data_low_pre = ContextInfo.get_history_data(2,'1d','low',1)
    data_high_pre = ContextInfo.get_history_data(2,'1d','high',1)
    
    #print data_high
    #print data_close
    #print data_close60
    for k in ContextInfo.s:
        if k in data_close60:
            if len(data_close60[k]) == 200 and (data_close60[k][0] != data_close60[k][1] or data_close60[k][2] != data_close60[k][1]):
                #shift = 0时候为当日收盘后判断是否有买入
                #实盘时候需要shift = -1并且low那一行取消注释
                shift = -1
                datalow130 = min(data_close60[k][shift-130:shift-1])
                AVG60 = ta.MA(np.array(data_close60[k]), timeperiod = 60)
                #nowDate = int(timetag_to_datetime(ContextInfo.get_bar_timetag(day),'%Y%m%d'))
                #if (
                #    (k == "603707.SH" )
                #    and (nowDate == 20180301)):
                #    logging.info(data_close60[k])
                #    logging.info(type(data_close60[k]))
                #    logging.info(len(data_close60[k]))
                #    logging.info(AVG60)
                #    logging.info("***********************")
                #    logging.info(str(day))
                #    logging.info("low " + str(datalow130))
                #    logging.info(data_close[k][-12:-1])
                #    logging.info(data_close[k][-6] >= data_close[k][-7] or data_close[k][-6] >= data_open[k][-6]) 
                #    logging.info(data_close[k][-7] >= data_close[k][-8] or data_close[k][-7] >= data_open[k][-7])
                #    logging.info(data_close[k][-8] >= data_close[k][-9] or data_close[k][-8] >= data_open[k][-8])
                #    logging.info(data_close[k][-9] >= data_close[k][-10] or data_close[k][-9] >= data_open[k][-9])
                #    logging.info(data_close[k][-10] >= data_close[k][-11] or data_close[k][-10] >= data_open[k][-10])
                #    logging.info(data_close[k][-11] >= data_close[k][-12] or data_close[k][-11] >= data_open[k][-11])
                #    logging.info(data_close[k][-12] * 1.14 > data_close[k][-2] or data_close[k][-2] < AVG60[-2])
                #    logging.info(data_close[k][-2] > data_close[k][-6])
                #    logging.info(data_close[k][-2] > datalow130 * 1.3)
                #    logging.info(data_low_pre[k][-2] < data_close60[k][-2])
                #    logging.info(data_high_pre[k][shift-1] < data_close[k][shift-1] * 1.03)
                #    logging.info(data_low_pre[k][shift-1] * 1.01 < data_close[k][shift-1])
 
                if ( (data_close[k][shift-5] >= data_close[k][shift-6] or data_close[k][shift-5] >= data_open[k][shift-5])  
                    and (data_close[k][shift-6] >= data_close[k][shift-7] or data_close[k][shift-6] >= data_open[k][shift-6])
                    and (data_close[k][shift-7] >= data_close[k][shift-8] or data_close[k][shift-7] >= data_open[k][shift-7])
                    and (data_close[k][shift-8] >= data_close[k][shift-9] or data_close[k][shift-8] >= data_open[k][shift-8])
                    and (data_close[k][shift-9] >= data_close[k][shift-10] or data_close[k][shift-9] >= data_open[k][shift-9])
                    and (data_close[k][shift-10] >= data_close[k][shift-11] or data_close[k][shift-10] >= data_open[k][shift-10])
                    #and (data_close[k][-12] < data_close[k][-13] )
                    and (data_close[k][shift-11] * 1.14 > data_close[k][shift-1] or data_close[k][shift-5] < AVG60[shift-1])
                    and data_close[k][shift-1] > data_close[k][shift-5]
                    and data_close[k][shift-5] > datalow130 * 1.3
                    and data_close[k][shift-1] < 100
                    and data_low_pre[k][shift] < data_close[k][shift-1] #canbuy
                    and data_high_pre[k][shift-1] < data_close[k][shift-1] * 1.03
                    and data_low_pre[k][shift-1] * 1.01 < data_close[k][shift-1]
                ):
                    buy[k] = 1           
                elif (int(ContextInfo.boughtday[k]) > 0):
                    nowDate = int(timetag_to_datetime(ContextInfo.get_bar_timetag(day),'%Y%m%d'))
                    boughtDate = int(ContextInfo.boughtday[k])
                    boughtDateIndex = ContextInfo.dateDict[boughtDate]
                    nowDateIndex = ContextInfo.dateDict[nowDate]
                    if (boughtDateIndex + 20 <= nowDateIndex
                    ):
                        sell[k] = 1           
    #print buy
    #print sell
    return buy,sell           #买入卖出备选


