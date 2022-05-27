import datetime
import fractions
import json
import os
import re

import loguru
import requests

#取得個股盤後資訊 + 解析 JSON

class AfterHoursInfo:
    def __init__(
        self,
        code,
        name,
        totalShare,
        totalTurnover,
        openPrice,
        highestPrice,
        lowestPrice,
        closePrice):
        # 代碼
        self.Code = code
        # 名稱
        self.Name = name
        # 成交股數
        self.TotalShare = self.checkNumber(totalShare)
        if self.TotalShare is not None:
            self.TotalShare = int(totalShare)
        # 成交金額
        self.TotalTurnover = self.checkNumber(totalTurnover)
        if self.TotalTurnover is not None:
            self.TotalTurnover = int(totalTurnover)
        # 開盤價
        self.OpenPrice = self.checkNumber(openPrice)
        if self.OpenPrice is not None:
            self.OpenPrice = fractions.Fraction(openPrice)
        # 最高價
        self.HighestPrice = self.checkNumber(highestPrice)
        if self.HighestPrice is not None:
            self.HighestPrice = fractions.Fraction(highestPrice)
        # 最低價
        self.LowestPrice = self.checkNumber(lowestPrice)
        if self.LowestPrice is not None:
            self.LowestPrice = fractions.Fraction(lowestPrice)
        # 收盤價
        self.ClosePrice = self.checkNumber(closePrice)
        if self.ClosePrice is not None:
            self.ClosePrice = fractions.Fraction(closePrice)
    # 物件表達式
    def __repr__(self):
        totalShare = self.TotalShare
        if totalShare is not None:
            totalShare = f'{totalShare}'
        totalTurnover = self.TotalTurnover
        if totalTurnover is not None:
            totalTurnover = f'{totalTurnover}'
        openPrice = self.OpenPrice
        if openPrice is not None:
            openPrice = f'{float(openPrice):.2f}'
        highestPrice = self.HighestPrice
        if highestPrice is not None:
            highestPrice = f'{float(highestPrice):.2f}'
        lowestPrice = self.LowestPrice
        if lowestPrice is not None:
            lowestPrice = f'{float(lowestPrice):.2f}'
        closePrice = self.ClosePrice
        if closePrice is not None:
            closePrice = f'{float(closePrice):.2f}'
        return (
            f'class AfterHoursInfo {{ '
            f'Code={self.Code}, '
            f'Name={self.Name}, '
            f'TotalShare={totalShare}, '
            f'TotalTurnover={totalTurnover}, '
            f'OpenPrice={openPrice}, '
            f'HighestPrice={highestPrice}, '
            f'LowestPrice={lowestPrice}, '
            f'ClosePrice={closePrice} '
            f'}}'
        )
    # 檢查數值是否有效
    def checkNumber(self, value):
        if value == '--':
            return None
        else:
            return value

def main():
    resp = requests.get(
        f'https://www.twse.com.tw/exchangeReport/MI_INDEX?' +
        f'response=json&' +
        f'type=ALLBUT0999' +
        f'&date={datetime.date.today():%Y%m%d}'
    )
    if resp.status_code != 200:
        loguru.logger.error('RESP: status code is not 200')
    loguru.logger.success('RESP: success')

    afterHoursInfos = []

    body = resp.json()
    stat = body['stat']
    if stat != 'OK':
        loguru.logger.error(f'RESP: body.stat error is {stat}.')
        return
    records = body['data9']
    for record in records:
        code = record[0].strip()
        if re.match(r'^[1-9][0-9][0-9][0-9]$', code) is not None:
            name = record[1].strip()
            totalShare = record[2].replace(',', '').strip()
            totalTurnover = record[4].replace(',', '').strip()
            openPrice = record[5].replace(',', '').strip()
            highestPrice = record[6].replace(',', '').strip()
            lowestPrice = record[7].replace(',', '').strip()
            closePrice = record[8].replace(',', '').strip()
            afterHoursInfo = AfterHoursInfo(
                code=code,
                name=name,
                totalShare=totalShare,
                totalTurnover=totalTurnover,
                openPrice=openPrice,
                highestPrice=highestPrice,
                lowestPrice=lowestPrice,
                closePrice=closePrice
            )
            afterHoursInfos.append(afterHoursInfo)

    message = os.linesep.join([
        str(afterHoursInfo)
        for afterHoursInfo in afterHoursInfos
    ])
    loguru.logger.info('AFTERHOURSINFOS' + os.linesep + message)

if __name__ == '__main__':
    loguru.logger.add(
        f'{datetime.date.today():%Y%m%d}.log',
        rotation='1 day',
        retention='7 days',
        level='DEBUG'
    )
    main()