import fractions

import csv
import datetime
import io

import loguru
import requests

import os

'''
解析 CSV
以取得個股每月各交易日盤後資訊為例
'''

class AfterHoursDailyInfo:
    def __init__(
        self,
        code,
        date,
        totalShare,
        totalTurnover,
        openPrice,
        highestPrice,
        lowestPrice,
        closePrice):
        # 代碼
        self.Code = code
        # 日期
        # 國曆年轉為西元年
        parts = date.split('/')
        date = datetime.date(int(parts[0]) + 1911, int(parts[1]), int(parts[2]))
        self.Date = date
        # 成交股數
        self.TotalShare = int(totalShare)
        # 成交金額
        self.TotalTurnover = int(totalTurnover)
        # 開盤價
        self.OpenPrice = fractions.Fraction(openPrice)
        # 最高價
        self.HighestPrice = fractions.Fraction(highestPrice)
        # 最低價
        self.LowestPrice = fractions.Fraction(lowestPrice)
        # 收盤價
        self.ClosePrice = fractions.Fraction(closePrice)
    # 物件表達式
    def __repr__(self):
        return (
            f'class AfterHoursDailyInfo {{ '
            f'Code={self.Code}, '
            f'Date={self.Date:%Y-%m-%d}, '
            f'TotalShare={self.TotalShare}, '
            f'TotalTurnover={self.TotalTurnover}, '
            f'OpenPrice={float(self.OpenPrice):.2f}, '
            f'HighestPrice={float(self.HighestPrice):.2f}, '
            f'LowestPrice={float(self.LowestPrice):.2f}, '
            f'ClosePrice={float(self.ClosePrice):.2f} '
            f'}}'
        )



def main(year, month, code):
    date = f'{year}{month:02}01'
    print('date:{}'.format(date))
    resp = requests.get(
        f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?' +
        f'response=csv&date={date}&stockNo={code}')
    if resp.status_code != 200:
        loguru.logger.error('RESP: status code is not 200')
    loguru.logger.success('RESP: success')

    # 個股每月各交易日盤後資訊清單
    afterHoursDailyInfos = []
    # 取出 CSV 內容，並去除第一行及最後 5 行
    lines = io.StringIO(resp.text).readlines()
    lines = lines[1:-5]
    # 透過 CSV 讀取器載入
    reader = csv.DictReader(io.StringIO('\n'.join(lines)))
    # 依序取出每筆資料行
    for row in reader:
        # 取出日期欄位值
        date = row['日期'].strip()
        # 取出成交股數欄位值
        totalShare = row['成交股數'].replace(',', '').strip()
        # 取出成交金額欄位值
        totalTurnover = row['成交金額'].replace(',', '').strip()
        # 取出開盤價欄位值
        openPrice = row['開盤價']
        # 取出最高價欄位值
        highestPrice = row['最高價']
        # 取出最低價欄位值
        lowestPrice = row['最低價']
        # 取出收盤價欄位值
        closePrice = row['收盤價']
        afterHoursDailyInfo = AfterHoursDailyInfo(
            code=code,
            date=date,
            totalShare=totalShare,
            totalTurnover=totalTurnover,
            openPrice=openPrice,
            highestPrice=highestPrice,
            lowestPrice=lowestPrice,
            closePrice=closePrice
        )
        afterHoursDailyInfos.append(afterHoursDailyInfo)
    loguru.logger.info(afterHoursDailyInfos)

    # 將每筆物件表達式輸出的字串以系統換行符號相接，讓每筆物件表達式各自獨立一行
    message = os.linesep.join([
        str(afterHoursDailyInfo)
        for afterHoursDailyInfo in afterHoursDailyInfos
    ])
    loguru.logger.info('AFTERHOURSDAILYINFOS' + os.linesep + message)

if __name__ == '__main__':
    loguru.logger.add(
        f'{datetime.date.today():%Y%m%d}.log',
        rotation='1 day',
        retention='7 days',
        level='DEBUG'
    )
    # 傳入年、月及股票代碼
    main(2020, 1, '1314')