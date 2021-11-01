from datetime import datetime,timedelta
import calendar
import math

callmonth = ['0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
putmonth = ['0', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']



# 回傳當月月選結算日期時間
def getThirdWendesday(td):
    # 當月第一天的日期
    first_day_of_month = datetime(td.year, td.month, 1)
    # 第一個週三的日期
    firstWendesday = first_day_of_month + timedelta(days=(9-calendar.monthrange(td.year, td.month)[0])%7)
    # 第三個周三的下午1:30 (月選結算時間)
    res = firstWendesday + timedelta(days=14) + timedelta(hours=13,minutes=30)
    return res 

# 該datetime是否已結算
def isTimetoMaturity(td):
    thirdWendesday = getThirdWendesday(td)
    return td.strftime('%Y%m%d') >= thirdWendesday.strftime('%Y%m%d')# :  True
    # return False

# 取得該datetime的當前月選
def getNearbyMonth(td):
    month = td.month
    year = int(str(td.year)[-1])
    if isTimetoMaturity(td): 
        month += 1
        if(month>12):
            year+=1
            month=1
    return year%10, month




def getSymbolName(price,type,dt):
    nearby = getNearbyMonth(dt)
    if type in ['call','c','C','Call']:
        return 'TXO'+str(price)+callmonth[nearby[1]]+str(nearby[0])
    else:
        return 'TXO'+str(price)+putmonth[nearby[1]]+str(nearby[0])

def getMiddleLine(_pointlist):
    Midline = 0
    for key, value in _pointlist.items():
        Midline += float(value)
        
    # 取輸入價格平均
    Midline /= len(_pointlist)

    # 向上取整
    Midceil = math.ceil(Midline/100)*100
    # 向下取整
    Midfloor = math.floor(Midline/100)*100

    if abs(Midline-Midfloor) < abs(Midline-Midceil):
        Midline = Midfloor
    else:
        Midline = Midceil
    # print('確定中線為',str(Midline))
    return Midline