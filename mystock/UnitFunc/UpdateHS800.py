#coding=gbk
import os,shutil
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib
import datetime, time
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import math
from dateutil.relativedelta import relativedelta
from sklearn.model_selection import GridSearchCV

rootdir = "C:/StockAnalysis/"
os.chdir(rootdir)
pd.set_option('display.max_columns', None)

def getMarketCode(strCode):
    strCode = strCode[:-3]
    if (strCode[0:1] == "6"):
        return "SH#" + strCode + ".txt"
    else:
        return "SZ#" + strCode + ".txt"

def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print (srcfile + " not exist!")
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print ("copy " + srcfile + " -> " + dstfile)

hs300 = ['000001.SZ', '000002.SZ', '603833.SH', '000703.SZ', '000783.SZ', '300003.SZ', '001979.SZ', '000413.SZ', '600061.SH', '600968.SH', '000100.SZ', '002555.SZ', '601698.SH', '002508.SZ', '000063.SZ', '000423.SZ', '000338.SZ', '000069.SZ', '002304.SZ', '002466.SZ', '600383.SH', '600928.SH', '000157.SZ', '600436.SH', '002044.SZ', '603501.SH', '601888.SH', '600674.SH', '603019.SH', '002252.SZ', '000425.SZ', '600637.SH', '002422.SZ', '601988.SH', '601997.SH', '000898.SZ', '601992.SH', '601088.SH', '000938.SZ', '600018.SH', '600346.SH', '000538.SZ', '600588.SH', '002736.SZ', '600369.SH', '002010.SZ', '600663.SH', '002493.SZ', '600068.SH', '000568.SZ', '601618.SH', '000895.SZ', '000661.SZ', '002468.SZ', '601788.SH', '603986.SH', '000625.SZ', '300122.SZ', '000630.SZ', '002594.SZ', '000651.SZ', '600048.SH', '601018.SH', '000786.SZ', '002050.SZ', '600025.SH', '000728.SZ', '000709.SZ', '000776.SZ', '002352.SZ', '601169.SH', '300015.SZ', '002411.SZ', '002714.SZ', '300059.SZ', '300347.SZ', '002120.SZ', '000768.SZ', '002739.SZ', '000961.SZ', '601006.SH', '002202.SZ', '300413.SZ', '002146.SZ', '601319.SH', '600109.SH', '601933.SH', '600438.SH', '601155.SH', '002294.SZ', '002916.SZ', '600297.SH', '000858.SZ', '002142.SZ', '000876.SZ', '600176.SH', '600655.SH', '600398.SH', '000963.SZ', '002460.SZ', '002007.SZ', '601901.SH', '300017.SZ', '601877.SH', '601989.SH', '002456.SZ', '300408.SZ', '002230.SZ', '002008.SZ', '002624.SZ', '601166.SH', '603260.SH', '600271.SH', '601857.SH', '600516.SH', '600733.SH', '603799.SH', '002179.SZ', '002027.SZ', '601818.SH', '600000.SH', '601668.SH', '601766.SH', '600183.SH', '600027.SH', '002241.SZ', '002236.SZ', '600009.SH', '600010.SH', '000415.SZ', '600816.SH', '600015.SH', '600016.SH', '600019.SH', '600352.SH', '601138.SH', '002271.SZ', '600028.SH', '600029.SH', '600030.SH', '600031.SH', '000725.SZ', '601939.SH', '600036.SH', '601898.SH', '600050.SH', '600066.SH', '300433.SZ', '600111.SH', '601919.SH', '000596.SZ', '603288.SH', '601398.SH', '600089.SH', '600085.SH', '002945.SZ', '000166.SZ', '300024.SZ', '600276.SH', '002607.SZ', '603160.SH', '600100.SH', '600115.SH', '600705.SH', '600104.SH', '601808.SH', '600606.SH', '600118.SH', '601878.SH', '601838.SH', '601198.SH', '600332.SH', '600219.SH', '600153.SH', '600482.SH', '600170.SH', '601009.SH', '600177.SH', '002475.SZ', '600188.SH', '601360.SH', '600196.SH', '600208.SH', '601600.SH', '000671.SZ', '600498.SH', '601211.SH', '600221.SH', '002673.SZ', '601318.SH', '600570.SH', '600390.SH', '002001.SZ', '300498.SZ', '601688.SH', '600535.SH', '600406.SH', '002958.SZ', '600372.SH', '600309.SH', '600340.SH', '601328.SH', '600566.SH', '601985.SH', '601828.SH', '600362.SH', '600522.SH', '000656.SZ', '002773.SZ', '600004.SH', '300136.SZ', '601881.SH', '600519.SH', '601727.SH', '601669.SH', '002410.SZ', '600583.SH', '600585.SH', '601236.SH', '601555.SH', '600760.SH', '601238.SH', '002311.SZ', '300144.SZ', '601377.SH', '601607.SH', '600919.SH', '601633.SH', '601288.SH', '601021.SH', '000627.SZ', '601108.SH', '601229.SH', '002032.SZ', '601111.SH', '601225.SH', '603156.SH', '600660.SH', '603899.SH', '601216.SH', '601117.SH', '600703.SH', '600690.SH', '300124.SZ', '600547.SH', '600926.SH', '600809.SH', '600011.SH', '601998.SH', '601390.SH', '601298.SH', '600741.SH', '000629.SZ', '002841.SZ', '300033.SZ', '600489.SH', '600998.SH', '000333.SZ', '002558.SZ', '601212.SH', '600837.SH', '600795.SH', '601899.SH', '601066.SH', '600867.SH', '600958.SH', '600886.SH', '603993.SH', '000723.SZ', '600893.SH', '601012.SH', '600977.SH', '601186.SH', '300142.SZ', '002415.SZ', '601162.SH', '601601.SH', '601577.SH', '600999.SH', '601336.SH', '002601.SZ', '300070.SZ', '600887.SH', '002939.SZ', '601628.SH', '600848.SH', '600900.SH', '603259.SH', '002602.SZ', '002081.SZ', '002153.SZ', '002024.SZ', '601800.SH', '600487.SH', '600299.SH', '600023.SH', '600038.SH', '002938.SZ', '600989.SH', '600233.SH']
zz500 = ['603877.SH', '002946.SZ', '002941.SZ', '002957.SZ', '600917.SH', '603256.SH', '601068.SH', '603025.SH', '600939.SH', '002423.SZ', '001872.SZ', '603868.SH', '601865.SH', '603355.SH', '603317.SH', '603650.SH', '603225.SH', '601811.SH', '603379.SH', '601969.SH', '601860.SH', '000025.SZ', '600335.SH', '600996.SH', '300199.SZ', '603983.SH', '601869.SH', '002818.SZ', '601003.SH', '600707.SH', '600874.SH', '603556.SH', '601127.SH', '603056.SH', '002948.SZ', '601801.SH', '002653.SZ', '600053.SH', '600350.SH', '002482.SZ', '600903.SH', '002437.SZ', '601615.SH', '600058.SH', '600338.SH', '600657.SH', '603486.SH', '000600.SZ', '000980.SZ', '600098.SH', '002366.SZ', '000426.SZ', '600006.SH', '002672.SZ', '002424.SZ', '601001.SH', '002503.SZ', '000990.SZ', '300257.SZ', '600623.SH', '600757.SH', '000536.SZ', '000766.SZ', '000061.SZ', '002416.SZ', '603766.SH', '000937.SZ', '000869.SZ', '002358.SZ', '600329.SH', '002625.SZ', '600575.SH', '601016.SH', '600694.SH', '600428.SH', '002093.SZ', '002867.SZ', '600770.SH', '002573.SZ', '300376.SZ', '603515.SH', '300297.SZ', '300197.SZ', '603377.SH', '000564.SZ', '000537.SZ', '600985.SH', '603568.SH', '601019.SH', '600759.SH', '603888.SH', '002470.SZ', '000062.SZ', '002176.SZ', '601139.SH', '300459.SZ', '603328.SH', '000553.SZ', '002681.SZ', '601326.SH', '002285.SZ', '600639.SH', '600787.SH', '000848.SZ', '300159.SZ', '002382.SZ', '002375.SZ', '002544.SZ', '603198.SH', '002505.SZ', '002051.SZ', '002118.SZ', '600317.SH', '600126.SH', '002128.SZ', '002920.SZ', '002491.SZ', '000006.SZ', '002434.SZ', '002419.SZ', '601200.SH', '600478.SH', '600259.SH', '600565.SH', '002745.SZ', '600073.SH', '000543.SZ', '600141.SH', '600312.SH', '600582.SH', '600751.SH', '000987.SZ', '000519.SZ', '002839.SZ', '600835.SH', '600017.SH', '600125.SH', '600499.SH', '600859.SH', '600869.SH', '603233.SH', '000761.SZ', '600748.SH', '002249.SZ', '600645.SH', '601678.SH', '000813.SZ', '600316.SH', '601611.SH', '603712.SH', '000959.SZ', '600339.SH', '600901.SH', '601975.SH', '000727.SZ', '002709.SZ', '002302.SZ', '600664.SH', '002426.SZ', '000717.SZ', '600545.SH', '002635.SZ', '600765.SH', '002444.SZ', '000718.SZ', '601928.SH', '000967.SZ', '600195.SH', '600291.SH', '300324.SZ', '002280.SZ', '300134.SZ', '002603.SZ', '002203.SZ', '000156.SZ', '002640.SZ', '000681.SZ', '002925.SZ', '000758.SZ', '000501.SZ', '002390.SZ', '002244.SZ', '000732.SZ', '002815.SZ', '600557.SH', '600862.SH', '000078.SZ', '002701.SZ', '002183.SZ', '000301.SZ', '600277.SH', '601880.SH', '600717.SH', '002408.SZ', '300002.SZ', '600307.SH', '002030.SZ', '601608.SH', '002002.SZ', '600648.SH', '000400.SZ', '002266.SZ', '000826.SZ', '000158.SZ', '600348.SH', '002155.SZ', '600418.SH', '000887.SZ', '600563.SH', '002056.SZ', '600823.SH', '601598.SH', '601717.SH', '000028.SZ', '600158.SH', '000488.SZ', '600062.SH', '002665.SZ', '000712.SZ', '600598.SH', '000090.SZ', '600120.SH', '600056.SH', '002831.SZ', '600515.SH', '000012.SZ', '000008.SZ', '601228.SH', '601718.SH', '600633.SH', '600500.SH', '600908.SH', '000528.SZ', '600827.SH', '300182.SZ', '600649.SH', '600039.SH', '000685.SZ', '002399.SZ', '600138.SH', '600388.SH', '600507.SH', '600729.SH', '600970.SH', '000930.SZ', '603883.SH', '601689.SH', '000559.SZ', '300026.SZ', '000027.SZ', '300072.SZ', '000877.SZ', '600008.SH', '601179.SH', '000738.SZ', '300180.SZ', '603806.SH', '002242.SZ', '002583.SZ', '002440.SZ', '601000.SH', '600597.SH', '601958.SH', '002048.SZ', '300133.SZ', '002004.SZ', '600409.SH', '603077.SH', '002414.SZ', '603228.SH', '601106.SH', '600863.SH', '000807.SZ', '002064.SZ', '000932.SZ', '002038.SZ', '000883.SZ', '600782.SH', '002936.SZ', '300244.SZ', '600511.SH', '603816.SH', '600640.SH', '000598.SZ', '002317.SZ', '002372.SZ', '002028.SZ', '601118.SH', '603866.SH', '000031.SZ', '600064.SH', '600060.SH', '600777.SH', '601098.SH', '600435.SH', '601699.SH', '600026.SH', '600804.SH', '000563.SZ', '600037.SH', '603885.SH', '600171.SH', '603707.SH', '300010.SZ', '000021.SZ', '002221.SZ', '600967.SH', '002407.SZ', '002233.SZ', '600216.SH', '300027.SZ', '600167.SH', '600737.SH', '600266.SH', '002085.SZ', '000970.SZ', '600282.SH', '000729.SZ', '600808.SH', '600373.SH', '600754.SH', '002589.SZ', '000825.SZ', '600094.SH', '600580.SH', '600643.SH', '603882.SH', '600022.SH', '300009.SZ', '600755.SH', '600392.SH', '600166.SH', '002368.SZ', '000983.SZ', '000402.SZ', '300115.SZ', '600155.SH', '000690.SZ', '600718.SH', '603338.SH', '600776.SH', '600959.SH', '600811.SH', '600160.SH', '000089.SZ', '600380.SH', '002191.SZ', '300316.SZ', '600779.SH', '002807.SZ', '600875.SH', '600258.SH', '601866.SH', '300001.SZ', '600376.SH', '601333.SH', '002217.SZ', '600315.SH', '600881.SH', '300251.SZ', '000960.SZ', '000039.SZ', '600021.SH', '600415.SH', '002690.SZ', '600884.SH', '000636.SZ', '300113.SZ', '300274.SZ', '000060.SZ', '000830.SZ', '600839.SH', '600260.SH', '601005.SH', '603000.SH', '002075.SZ', '300166.SZ', '600549.SH', '002212.SZ', '601966.SH', '603939.SH', '600845.SH', '600466.SH', '603659.SH', '000581.SZ', '300308.SZ', '600497.SH', '300058.SZ', '600273.SH', '600410.SH', '600521.SH', '600820.SH', '002110.SZ', '000547.SZ', '600572.SH', '300418.SZ', '002152.SZ', '002074.SZ', '000878.SZ', '000997.SZ', '002092.SZ', '000778.SZ', '603858.SH', '600895.SH', '002019.SZ', '002281.SZ', '600567.SH', '600460.SH', '002223.SZ', '002670.SZ', '002174.SZ', '600446.SH', '000999.SZ', '000513.SZ', '002013.SZ', '002385.SZ', '600728.SH', '601231.SH', '600132.SH', '601168.SH', '002250.SZ', '600079.SH', '600486.SH', '600528.SH', '603444.SH', '600879.SH', '000686.SZ', '002387.SZ', '600143.SH', '601799.SH', '601100.SH', '600909.SH', '600325.SH', '600704.SH', '002572.SZ', '002373.SZ', '000975.SZ', '600256.SH', '000998.SZ', '300168.SZ', '300296.SZ', '002131.SZ', '600699.SH', '002500.SZ', '603517.SH', '600642.SH', '002926.SZ', '600161.SH', '002507.SZ', '002195.SZ', '600150.SH', '300529.SZ', '002268.SZ', '600298.SH', '002078.SZ', '300285.SZ', '000623.SZ', '600885.SH', '600673.SH', '000750.SZ', '000009.SZ', '000401.SZ', '000988.SZ', '601233.SH', '000050.SZ', '300315.SZ', '002797.SZ', '002180.SZ', '002353.SZ', '002821.SZ', '600801.SH', '002273.SZ', '600739.SH', '002127.SZ', '300088.SZ', '002065.SZ', '300253.SZ', '002129.SZ', '600763.SH', '300012.SZ', '002465.SZ', '601872.SH', '002340.SZ', '002812.SZ', '600201.SH', '300207.SZ', '002439.SZ', '600536.SH', '002371.SZ', '002049.SZ', '300383.SZ', '600426.SH', '300014.SZ', '600584.SH', '601128.SH', '601099.SH', '002384.SZ', '002463.SZ', '000066.SZ', '600745.SH']
stocklist = hs300 + zz500


for root, dirs, files in os.walk(rootdir + "hs300"):
    for filename in files:
        os.remove(rootdir + "hs300/" + filename)

for root, dirs, files in os.walk(rootdir + "live2"):
    for filename in files:
        os.remove(rootdir + "live2/" + filename)

for root, dirs, files in os.walk(rootdir + "houfu2"):
    for filename in files:
        os.remove(rootdir + "houfu2/" + filename)

count = 0              
for code in hs300:
    count+=1
    filename = getMarketCode(code)
    print("Times:" + str(count))
    mycopyfile(rootdir + "live/" + filename,rootdir + "hs300/" + filename)


count = 0
for code in stocklist:
    count+=1
    filename = getMarketCode(code)
    print("Times:" + str(count))
    mycopyfile(rootdir + "live/" + filename,rootdir + "live2/" + filename)
    mycopyfile(rootdir + "houfu/" + filename,rootdir + "houfu2/" + filename)

print("Update Done")    