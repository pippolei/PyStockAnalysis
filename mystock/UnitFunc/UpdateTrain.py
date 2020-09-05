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

def listDiff(list1, list2):
    ret1 = [i for i in list1 if i not in list2]
    ret2 = [i for i in list2 if i not in list1]
    return ret1 + ret2

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

#hs300 = hs300_jq
zz500 = ['603877.SH', '002946.SZ', '002941.SZ', '002957.SZ', '600917.SH', '603256.SH', '601068.SH', '603025.SH', '600939.SH', '002423.SZ', '001872.SZ', '603868.SH', '601865.SH', '603355.SH', '603317.SH', '603650.SH', '603225.SH', '601811.SH', '603379.SH', '601969.SH', '601860.SH', '000025.SZ', '600335.SH', '600996.SH', '300199.SZ', '603983.SH', '601869.SH', '002818.SZ', '601003.SH', '600707.SH', '600874.SH', '603556.SH', '601127.SH', '603056.SH', '002948.SZ', '601801.SH', '002653.SZ', '600053.SH', '600350.SH', '002482.SZ', '600903.SH', '002437.SZ', '601615.SH', '600058.SH', '600338.SH', '600657.SH', '603486.SH', '000600.SZ', '000980.SZ', '600098.SH', '002366.SZ', '000426.SZ', '600006.SH', '002672.SZ', '002424.SZ', '601001.SH', '002503.SZ', '000990.SZ', '300257.SZ', '600623.SH', '600757.SH', '000536.SZ', '000766.SZ', '000061.SZ', '002416.SZ', '603766.SH', '000937.SZ', '000869.SZ', '002358.SZ', '600329.SH', '002625.SZ', '600575.SH', '601016.SH', '600694.SH', '600428.SH', '002093.SZ', '002867.SZ', '600770.SH', '002573.SZ', '300376.SZ', '603515.SH', '300297.SZ', '300197.SZ', '603377.SH', '000564.SZ', '000537.SZ', '600985.SH', '603568.SH', '601019.SH', '600759.SH', '603888.SH', '002470.SZ', '000062.SZ', '002176.SZ', '601139.SH', '300459.SZ', '603328.SH', '000553.SZ', '002681.SZ', '601326.SH', '002285.SZ', '600639.SH', '600787.SH', '000848.SZ', '300159.SZ', '002382.SZ', '002375.SZ', '002544.SZ', '603198.SH', '002505.SZ', '002051.SZ', '002118.SZ', '600317.SH', '600126.SH', '002128.SZ', '002920.SZ', '002491.SZ', '000006.SZ', '002434.SZ', '002419.SZ', '601200.SH', '600478.SH', '600259.SH', '600565.SH', '002745.SZ', '600073.SH', '000543.SZ', '600141.SH', '600312.SH', '600582.SH', '600751.SH', '000987.SZ', '000519.SZ', '002839.SZ', '600835.SH', '600017.SH', '600125.SH', '600499.SH', '600859.SH', '600869.SH', '603233.SH', '000761.SZ', '600748.SH', '002249.SZ', '600645.SH', '601678.SH', '000813.SZ', '600316.SH', '601611.SH', '603712.SH', '000959.SZ', '600339.SH', '600901.SH', '601975.SH', '000727.SZ', '002709.SZ', '002302.SZ', '600664.SH', '002426.SZ', '000717.SZ', '600545.SH', '002635.SZ', '600765.SH', '002444.SZ', '000718.SZ', '601928.SH', '000967.SZ', '600195.SH', '600291.SH', '300324.SZ', '002280.SZ', '300134.SZ', '002603.SZ', '002203.SZ', '000156.SZ', '002640.SZ', '000681.SZ', '002925.SZ', '000758.SZ', '000501.SZ', '002390.SZ', '002244.SZ', '000732.SZ', '002815.SZ', '600557.SH', '600862.SH', '000078.SZ', '002701.SZ', '002183.SZ', '000301.SZ', '600277.SH', '601880.SH', '600717.SH', '002408.SZ', '300002.SZ', '600307.SH', '002030.SZ', '601608.SH', '002002.SZ', '600648.SH', '000400.SZ', '002266.SZ', '000826.SZ', '000158.SZ', '600348.SH', '002155.SZ', '600418.SH', '000887.SZ', '600563.SH', '002056.SZ', '600823.SH', '601598.SH', '601717.SH', '000028.SZ', '600158.SH', '000488.SZ', '600062.SH', '002665.SZ', '000712.SZ', '600598.SH', '000090.SZ', '600120.SH', '600056.SH', '002831.SZ', '600515.SH', '000012.SZ', '000008.SZ', '601228.SH', '601718.SH', '600633.SH', '600500.SH', '600908.SH', '000528.SZ', '600827.SH', '300182.SZ', '600649.SH', '600039.SH', '000685.SZ', '002399.SZ', '600138.SH', '600388.SH', '600507.SH', '600729.SH', '600970.SH', '000930.SZ', '603883.SH', '601689.SH', '000559.SZ', '300026.SZ', '000027.SZ', '300072.SZ', '000877.SZ', '600008.SH', '601179.SH', '000738.SZ', '300180.SZ', '603806.SH', '002242.SZ', '002583.SZ', '002440.SZ', '601000.SH', '600597.SH', '601958.SH', '002048.SZ', '300133.SZ', '002004.SZ', '600409.SH', '603077.SH', '002414.SZ', '603228.SH', '601106.SH', '600863.SH', '000807.SZ', '002064.SZ', '000932.SZ', '002038.SZ', '000883.SZ', '600782.SH', '002936.SZ', '300244.SZ', '600511.SH', '603816.SH', '600640.SH', '000598.SZ', '002317.SZ', '002372.SZ', '002028.SZ', '601118.SH', '603866.SH', '000031.SZ', '600064.SH', '600060.SH', '600777.SH', '601098.SH', '600435.SH', '601699.SH', '600026.SH', '600804.SH', '000563.SZ', '600037.SH', '603885.SH', '600171.SH', '603707.SH', '300010.SZ', '000021.SZ', '002221.SZ', '600967.SH', '002407.SZ', '002233.SZ', '600216.SH', '300027.SZ', '600167.SH', '600737.SH', '600266.SH', '002085.SZ', '000970.SZ', '600282.SH', '000729.SZ', '600808.SH', '600373.SH', '600754.SH', '002589.SZ', '000825.SZ', '600094.SH', '600580.SH', '600643.SH', '603882.SH', '600022.SH', '300009.SZ', '600755.SH', '600392.SH', '600166.SH', '002368.SZ', '000983.SZ', '000402.SZ', '300115.SZ', '600155.SH', '000690.SZ', '600718.SH', '603338.SH', '600776.SH', '600959.SH', '600811.SH', '600160.SH', '000089.SZ', '600380.SH', '002191.SZ', '300316.SZ', '600779.SH', '002807.SZ', '600875.SH', '600258.SH', '601866.SH', '300001.SZ', '600376.SH', '601333.SH', '002217.SZ', '600315.SH', '600881.SH', '300251.SZ', '000960.SZ', '000039.SZ', '600021.SH', '600415.SH', '002690.SZ', '600884.SH', '000636.SZ', '300113.SZ', '300274.SZ', '000060.SZ', '000830.SZ', '600839.SH', '600260.SH', '601005.SH', '603000.SH', '002075.SZ', '300166.SZ', '600549.SH', '002212.SZ', '601966.SH', '603939.SH', '600845.SH', '600466.SH', '603659.SH', '000581.SZ', '300308.SZ', '600497.SH', '300058.SZ', '600273.SH', '600410.SH', '600521.SH', '600820.SH', '002110.SZ', '000547.SZ', '600572.SH', '300418.SZ', '002152.SZ', '002074.SZ', '000878.SZ', '000997.SZ', '002092.SZ', '000778.SZ', '603858.SH', '600895.SH', '002019.SZ', '002281.SZ', '600567.SH', '600460.SH', '002223.SZ', '002670.SZ', '002174.SZ', '600446.SH', '000999.SZ', '000513.SZ', '002013.SZ', '002385.SZ', '600728.SH', '601231.SH', '600132.SH', '601168.SH', '002250.SZ', '600079.SH', '600486.SH', '600528.SH', '603444.SH', '600879.SH', '000686.SZ', '002387.SZ', '600143.SH', '601799.SH', '601100.SH', '600909.SH', '600325.SH', '600704.SH', '002572.SZ', '002373.SZ', '000975.SZ', '600256.SH', '000998.SZ', '300168.SZ', '300296.SZ', '002131.SZ', '600699.SH', '002500.SZ', '603517.SH', '600642.SH', '002926.SZ', '600161.SH', '002507.SZ', '002195.SZ', '600150.SH', '300529.SZ', '002268.SZ', '600298.SH', '002078.SZ', '300285.SZ', '000623.SZ', '600885.SH', '600673.SH', '000750.SZ', '000009.SZ', '000401.SZ', '000988.SZ', '601233.SH', '000050.SZ', '300315.SZ', '002797.SZ', '002180.SZ', '002353.SZ', '002821.SZ', '600801.SH', '002273.SZ', '600739.SH', '002127.SZ', '300088.SZ', '002065.SZ', '300253.SZ', '002129.SZ', '600763.SH', '300012.SZ', '002465.SZ', '601872.SH', '002340.SZ', '002812.SZ', '600201.SH', '300207.SZ', '002439.SZ', '600536.SH', '002371.SZ', '002049.SZ', '300383.SZ', '600426.SH', '300014.SZ', '600584.SH', '601128.SH', '601099.SH', '002384.SZ', '002463.SZ', '000066.SZ', '600745.SH']
zz1000 = ['000567.SZ', '000019.SZ', '603848.SH', '000011.SZ', '000560.SZ', '000016.SZ', '000836.SZ', '000030.SZ', '000035.SZ', '000036.SZ', '000507.SZ', '000055.SZ', '000058.SZ', '000498.SZ', '000065.SZ', '000552.SZ', '600483.SH', '000639.SZ', '002792.SZ', '002928.SZ', '000517.SZ', '000885.SZ', '000662.SZ', '000540.SZ', '000615.SZ', '603590.SH', '000429.SZ', '000525.SZ', '000796.SZ', '000514.SZ', '000516.SZ', '000620.SZ', '002668.SZ', '000720.SZ', '000550.SZ', '000688.SZ', '000582.SZ', '000532.SZ', '000557.SZ', '002073.SZ', '000546.SZ', '000545.SZ', '000576.SZ', '000822.SZ', '000710.SZ', '000555.SZ', '000592.SZ', '000561.SZ', '000672.SZ', '000597.SZ', '000708.SZ', '000584.SZ', '000544.SZ', '000626.SZ', '603956.SH', '000591.SZ', '002068.SZ', '000603.SZ', '000650.SZ', '000601.SZ', '000935.SZ', '000958.SZ', '000928.SZ', '000697.SZ', '000657.SZ', '002034.SZ', '000838.SZ', '000665.SZ', '000666.SZ', '000676.SZ', '000795.SZ', '000682.SZ', '000918.SZ', '000950.SZ', '000683.SZ', '000687.SZ', '603220.SH', '002041.SZ', '000815.SZ', '000735.SZ', '000818.SZ', '000751.SZ', '000793.SZ', '000726.SZ', '000829.SZ', '000733.SZ', '000913.SZ', '000828.SZ', '000739.SZ', '600971.SH', '000810.SZ', '000799.SZ', '000791.SZ', '000789.SZ', '000800.SZ', '001896.SZ', '000797.SZ', '000801.SZ', '000802.SZ', '000821.SZ', '000831.SZ', '000811.SZ', '603619.SH', '000900.SZ', '000976.SZ', '000926.SZ', '000851.SZ', '000892.SZ', '000881.SZ', '000875.SZ', '000882.SZ', '000927.SZ', '000889.SZ', '000902.SZ', '000923.SZ', '000901.SZ', '002840.SZ', '000905.SZ', '603098.SH', '000917.SZ', '000915.SZ', '002029.SZ', '000925.SZ', '002305.SZ', '000951.SZ', '001696.SZ', '000957.SZ', '000965.SZ', '000969.SZ', '000989.SZ', '603557.SH', '000996.SZ', '600975.SH', '002251.SZ', '600978.SH', '002276.SZ', '002061.SZ', '002091.SZ', '002043.SZ', '002047.SZ', '002016.SZ', '002020.SZ', '002216.SZ', '002025.SZ', '002035.SZ', '002023.SZ', '603808.SH', '002031.SZ', '002274.SZ', '002036.SZ', '002063.SZ', '002042.SZ', '600227.SH', '000903.SZ', '603919.SH', '002055.SZ', '002060.SZ', '002124.SZ', '002067.SZ', '002022.SZ', '603185.SH', '002079.SZ', '002080.SZ', '002135.SZ', '002345.SZ', '002100.SZ', '002094.SZ', '002095.SZ', '002141.SZ', '002097.SZ', '002099.SZ', '002101.SZ', '002168.SZ', '002104.SZ', '002108.SZ', '002123.SZ', '002308.SZ', '002115.SZ', '002117.SZ', '002121.SZ', '002126.SZ', '002130.SZ', '002137.SZ', '002138.SZ', '002139.SZ', '603777.SH', '002145.SZ', '002148.SZ', '002151.SZ', '002156.SZ', '002277.SZ', '603686.SH', '000667.SZ', '002166.SZ', '002167.SZ', '603687.SH', '603896.SH', '603997.SH', '002192.SZ', '002219.SZ', '002243.SZ', '002182.SZ', '002204.SZ', '002185.SZ', '603678.SH', '002206.SZ', '002320.SZ', '002197.SZ', '002258.SZ', '600136.SH', '002239.SZ', '002234.SZ', '002226.SZ', '603727.SH', '002215.SZ', '002218.SZ', '002222.SZ', '002224.SZ', '002237.SZ', '002229.SZ', '603876.SH', '002232.SZ', '002235.SZ', '002262.SZ', '002246.SZ', '002245.SZ', '002254.SZ', '002261.SZ', '002256.SZ', '002293.SZ', '002292.SZ', '603803.SH', '002267.SZ', '000150.SZ', '002343.SZ', '000070.SZ', '002396.SZ', '000155.SZ', '002279.SZ', '002283.SZ', '002284.SZ', '603989.SH', '002309.SZ', '002301.SZ', '600810.SH', '600596.SH', '002298.SZ', '600131.SH', '603583.SH', '002327.SZ', '002303.SZ', '603393.SH', '002307.SZ', '002314.SZ', '002313.SZ', '002335.SZ', '002318.SZ', '002344.SZ', '002322.SZ', '603915.SH', '002326.SZ', '603920.SH', '002332.SZ', '600790.SH', '603421.SH', '603383.SH', '002370.SZ', '002341.SZ', '002346.SZ', '000056.SZ', '603636.SH', '603609.SH', '002351.SZ', '603881.SH', '002355.SZ', '300568.SZ', '002393.SZ', '002409.SZ', '002405.SZ', '002364.SZ', '002367.SZ', '002430.SZ', '002377.SZ', '002376.SZ', '002481.SZ', '603018.SH', '002895.SZ', '002383.SZ', '600035.SH', '600831.SH', '002400.SZ', '002389.SZ', '002798.SZ', '002413.SZ', '002402.SZ', '600738.SH', '002428.SZ', '002851.SZ', '002498.SZ', '002447.SZ', '002421.SZ', '002429.SZ', '002425.SZ', '002464.SZ', '002435.SZ', '002433.SZ', '603737.SH', '002436.SZ', '002461.SZ', '603979.SH', '002443.SZ', '603773.SH', '002446.SZ', '002489.SZ', '002449.SZ', '002451.SZ', '300788.SZ', '002478.SZ', '002458.SZ', '603733.SH', '002782.SZ', '002462.SZ', '002538.SZ', '002467.SZ', '600076.SH', '002850.SZ', '603660.SH', '002485.SZ', '002474.SZ', '603728.SH', '002488.SZ', '002621.SZ', '002484.SZ', '002515.SZ', '600067.SH', '002511.SZ', '002776.SZ', '603693.SH', '002497.SZ', '603680.SH', '600691.SH', '002512.SZ', '002585.SZ', '002522.SZ', '002530.SZ', '002510.SZ', '002539.SZ', '002537.SZ', '600481.SH', '002516.SZ', '002518.SZ', '002519.SZ', '300558.SZ', '600636.SH', '002930.SZ', '600635.SH', '002913.SZ', '002534.SZ', '002545.SZ', '002531.SZ', '002955.SZ', '002568.SZ', '002619.SZ', '002582.SZ', '002542.SZ', '002562.SZ', '002675.SZ', '002547.SZ', '002683.SZ', '002550.SZ', '002565.SZ', '002657.SZ', '002556.SZ', '002918.SZ', '600517.SH', '002564.SZ', '300533.SZ', '002581.SZ', '002567.SZ', '600984.SH', '002648.SZ', '603898.SH', '002951.SZ', '002950.SZ', '002907.SZ', '002906.SZ', '002639.SZ', '002663.SZ', '002947.SZ', '002590.SZ', '002596.SZ', '002597.SZ', '002929.SZ', '002912.SZ', '002705.SZ', '002911.SZ', '002605.SZ', '002647.SZ', '603368.SH', '002609.SZ', '002610.SZ', '002611.SZ', '002614.SZ', '603180.SH', '002617.SZ', '002618.SZ', '002631.SZ', '002646.SZ', '603298.SH', '002626.SZ', '002755.SZ', '002651.SZ', '002630.SZ', '002636.SZ', '601567.SH', '002638.SZ', '601369.SH', '002656.SZ', '002717.SZ', '002643.SZ', '601519.SH', '601069.SH', '002649.SZ', '002650.SZ', '603839.SH', '601015.SH', '603826.SH', '002832.SZ', '002727.SZ', '603869.SH', '002664.SZ', '002756.SZ', '300531.SZ', '603900.SH', '600929.SH', '002685.SZ', '603980.SH', '603096.SH', '002677.SZ', '603718.SH', '601330.SH', '603711.SH', '002698.SZ', '600269.SH', '603605.SH', '002695.SZ', '300007.SZ', '002737.SZ', '600503.SH', '600366.SH', '002733.SZ', '002697.SZ', '002852.SZ', '002759.SZ', '002746.SZ', '002822.SZ', '002768.SZ', '002769.SZ', '002933.SZ', '002741.SZ', '002712.SZ', '002796.SZ', '002859.SZ', '002901.SZ', '002721.SZ', '002751.SZ', '002777.SZ', '002747.SZ', '300066.SZ', '300595.SZ', '603626.SH', '300759.SZ', '300006.SZ', '600012.SH', '300755.SZ', '603612.SH', '300011.SZ', '300783.SZ', '300043.SZ', '300602.SZ', '300016.SZ', '300506.SZ', '300020.SZ', '300021.SZ', '300502.SZ', '300031.SZ', '603533.SH', '603466.SH', '300036.SZ', '600239.SH', '300034.SZ', '600055.SH', '300785.SZ', '300037.SZ', '300038.SZ', '600261.SH', '300782.SZ', '300044.SZ', '300045.SZ', '300047.SZ', '300107.SZ', '300085.SZ', '300055.SZ', '600059.SH', '300061.SZ', '300053.SZ', '300054.SZ', '300078.SZ', '603458.SH', '300747.SZ', '300065.SZ', '300064.SZ', '600072.SH', '300068.SZ', '600180.SH', '600197.SH', '300073.SZ', '300741.SZ', '300075.SZ', '600069.SH', '300081.SZ', '600162.SH', '300079.SZ', '300497.SZ', '002228.SZ', '300496.SZ', '300083.SZ', '300737.SZ', '300765.SZ', '300091.SZ', '000936.SZ', '300123.SZ', '300482.SZ', '300096.SZ', '300098.SZ', '000910.SZ', '300100.SZ', '300101.SZ', '300102.SZ', '300109.SZ', '300495.SZ', '300110.SZ', '603555.SH', '300510.SZ', '300114.SZ', '000520.SZ', '300118.SZ', '300559.SZ', '300673.SZ', '300149.SZ', '300128.SZ', '300237.SZ', '300130.SZ', '300131.SZ', '603801.SH', '300735.SZ', '300236.SZ', '300137.SZ', '300145.SZ', '300140.SZ', '300143.SZ', '603318.SH', '600096.SH', '300148.SZ', '300674.SZ', '300266.SZ', '300158.SZ', '300766.SZ', '300775.SZ', '300232.SZ', '300777.SZ', '300463.SZ', '300751.SZ', '300458.SZ', '300233.SZ', '300773.SZ', '300726.SZ', '300476.SZ', '600123.SH', '600093.SH', '300776.SZ', '300170.SZ', '300171.SZ', '300748.SZ', '300176.SZ', '300177.SZ', '300178.SZ', '300184.SZ', '300616.SZ', '300183.SZ', '300185.SZ', '600169.SH', '603429.SH', '300188.SZ', '300451.SZ', '300194.SZ', '300191.SZ', '603337.SH', '603323.SH', '600242.SH', '603305.SH', '300198.SZ', '300208.SZ', '300278.SZ', '300256.SZ', '300203.SZ', '603327.SH', '300205.SZ', '603345.SH', '300740.SZ', '300209.SZ', '300212.SZ', '300213.SZ', '300215.SZ', '300699.SZ', '300685.SZ', '300219.SZ', '300222.SZ', '300223.SZ', '300224.SZ', '300226.SZ', '300298.SZ', '300724.SZ', '300229.SZ', '300771.SZ', '300607.SZ', '600020.SH', '300630.SZ', '300238.SZ', '300618.SZ', '300252.SZ', '300676.SZ', '300248.SZ', '300723.SZ', '300255.SZ', '600389.SH', '300572.SZ', '300323.SZ', '300424.SZ', '300487.SZ', '300262.SZ', '300263.SZ', '300406.SZ', '300666.SZ', '300394.SZ', '300504.SZ', '300271.SZ', '300474.SZ', '300386.SZ', '300664.SZ', '300276.SZ', '300284.SZ', '300287.SZ', '300423.SZ', '300613.SZ', '300288.SZ', '300457.SZ', '300292.SZ', '300327.SZ', '300294.SZ', '300725.SZ', '300770.SZ', '300317.SZ', '300299.SZ', '300428.SZ', '300300.SZ', '300326.SZ', '300302.SZ', '300303.SZ', '300309.SZ', '300409.SZ', '300307.SZ', '300624.SZ', '300310.SZ', '300311.SZ', '300661.SZ', '603113.SH', '300393.SZ', '603081.SH', '300322.SZ', '300467.SZ', '300634.SZ', '603063.SH', '300348.SZ', '300328.SZ', '300456.SZ', '300332.SZ', '300682.SZ', '300527.SZ', '300450.SZ', '300336.SZ', '603012.SH', '300339.SZ', '600702.SH', '300343.SZ', '300364.SZ', '300365.SZ', '300349.SZ', '300679.SZ', '300352.SZ', '300353.SZ', '300355.SZ', '300357.SZ', '300366.SZ', '300662.SZ', '300359.SZ', '300401.SZ', '300684.SZ', '300363.SZ', '300410.SZ', '300439.SZ', '300367.SZ', '300368.SZ', '300369.SZ', '300429.SZ', '300633.SZ', '300438.SZ', '300373.SZ', '300638.SZ', '300477.SZ', '300377.SZ', '300378.SZ', '300379.SZ', '300398.SZ', '300768.SZ', '300388.SZ', '300441.SZ', '600054.SH', '600075.SH', '600057.SH', '600110.SH', '600063.SH', '600736.SH', '603267.SH', '600103.SH', '603676.SH', '603708.SH', '603222.SH', '600146.SH', '600105.SH', '600106.SH', '600108.SH', '600308.SH', '600114.SH', '600116.SH', '600305.SH', '603618.SH', '600175.SH', '600129.SH', '600229.SH', '600133.SH', '600300.SH', '601636.SH', '601858.SH', '600587.SH', '600897.SH', '600184.SH', '600337.SH', '600172.SH', '600211.SH', '603588.SH', '600185.SH', '600217.SH', '600320.SH', '603399.SH', '600200.SH', '600207.SH', '600206.SH', '000034.SZ', '603387.SH', '600210.SH', '601666.SH', '600231.SH', '600226.SH', '603613.SH', '600230.SH', '603348.SH', '600322.SH', '603367.SH', '600252.SH', '600351.SH', '600255.SH', '603359.SH', '600611.SH', '002833.SZ', '600278.SH', '600284.SH', '600283.SH', '600285.SH', '600681.SH', '600295.SH', '601595.SH', '000059.SZ', '000040.SZ', '600378.SH', '600618.SH', '600310.SH', '603666.SH', '600318.SH', '603357.SH', '600323.SH', '600326.SH', '603118.SH', '600330.SH', '600331.SH', '603279.SH', '603218.SH', '600343.SH', '603363.SH', '603638.SH', '603169.SH', '600360.SH', '600363.SH', '000038.SZ', '600533.SH', '600449.SH', '600529.SH', '600456.SH', '600382.SH', '603599.SH', '600490.SH', '600458.SH', '600391.SH', '600512.SH', '600581.SH', '600400.SH', '600422.SH', '600420.SH', '600459.SH', '600467.SH', '600546.SH', '603596.SH', '600477.SH', '600480.SH', '600491.SH', '600569.SH', '600496.SH', '600495.SH', '600508.SH', '600548.SH', '600502.SH', '600550.SH', '600523.SH', '600603.SH', '600775.SH', '603587.SH', '600531.SH', '600552.SH', '600559.SH', '601606.SH', '600562.SH', '603105.SH', '600568.SH', '600571.SH', '600577.SH', '600612.SH', '600590.SH', '600619.SH', '600601.SH', '600602.SH', '600604.SH', '601126.SH', '600641.SH', '000711.SZ', '603058.SH', '603103.SH', '600621.SH', '600622.SH', '600624.SH', '600626.SH', '600894.SH', '600638.SH', '601010.SH', '600711.SH', '600650.SH', '600658.SH', '600685.SH', '600720.SH', '600936.SH', '600662.SH', '001914.SZ', '600667.SH', '600668.SH', '600676.SH', '600677.SH', '600773.SH', '600783.SH', '600803.SH', '600684.SH', '600686.SH', '601677.SH', '000088.SZ', '600715.SH', '603026.SH', '603595.SH', '600710.SH', '600761.SH', '600708.SH', '603236.SH', '600812.SH', '600764.SH', '601588.SH', '600734.SH', '600750.SH', '603068.SH', '600740.SH', '603039.SH', '600758.SH', '600742.SH', '600798.SH', '000973.SZ', '603043.SH', '600756.SH', '601375.SH', '600993.SH', '600825.SH', '600771.SH', '601619.SH', '601949.SH', '000931.SZ', '600963.SH', '603013.SH', '601929.SH', '603127.SH', '600789.SH', '601908.SH', '600797.SH', '600800.SH', '000968.SZ', '600851.SH', '600981.SH', '600864.SH', '600997.SH', '601886.SH', '600876.SH', '601163.SH', '600873.SH', '600850.SH', '600846.SH', '600868.SH', '600855.SH', '000933.SZ', '601952.SH', '600933.SH', '601566.SH', '601918.SH', '603027.SH', '000921.SZ', '600986.SH', '600966.SH', '601020.SH', '601011.SH', '603959.SH', '600987.SH', '600988.SH', '600990.SH', '600995.SH', '601137.SH', '601116.SH', '601101.SH', '601107.SH', '601058.SH', '601366.SH', '601515.SH', '601222.SH', '000049.SZ', '601700.SH', '601789.SH', '603508.SH', '603108.SH', '601890.SH', '603111.SH', '603456.SH', '603313.SH', '603008.SH', '603299.SH', '603128.SH', '603606.SH', '603308.SH', '603603.SH', '603648.SH', '002158.SZ', '603713.SH', '002171.SZ', '002240.SZ', '603579.SH', '002378.SZ', '002557.SZ', '300039.SZ', '002662.SZ', '002726.SZ', '300761.SZ', '300702.SZ', '300571.SZ', '300596.SZ', '300623.SZ', '300520.SZ', '300567.SZ', '300523.SZ', '600090.SH']
stocklist = hs300 + zz500
stocklist2 = zz1000
print(len(stocklist))


for root, dirs, files in os.walk(rootdir + "train2"):
    for filename in files:
        os.remove(rootdir + "train2/" + filename)

for root, dirs, files in os.walk(rootdir + "train3"):
    for filename in files:
        os.remove(rootdir + "train3/" + filename)



count = 0
for code in stocklist:
    count+=1
    filename = getMarketCode(code)
    print("Times:" + str(count))
    mycopyfile(rootdir + "train/" + filename,rootdir + "train2/" + filename)

count = 0
for code in stocklist2:
    count+=1
    filename = getMarketCode(code)
    print("Times:" + str(count))
    mycopyfile(rootdir + "train/" + filename,rootdir + "train3/" + filename)
print("Update Done")    