import argparse
import csv
import datetime

import loguru

#解析命令列參數

today = datetime.date.today()

def process_taiex(row):
    pass

def predict_taiex():
    # 以指定日期取出 day08.py 每日取得並儲存的結果進行運算
    with open(f'day-08-{today:%Y%m%d}.csv', 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            process_taiex(row)

def main(args):
    global today

    if args.check:
        loguru.logger.info(f'[-c|--check] is used')
    else:
        loguru.logger.info(f'[-c|--check] is not used')
    
    if args.today:
        loguru.logger.info(f'[-t|--today] [value:{args.today}]')
        # 假設今日為指定日期
        today = args.today
    else:
        loguru.logger.info(f'[-t|--today] is not used')

    predict_taiex()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # -t [value:yyyy-mm-dd]
    # --today [value:yyyy-mm-dd]
    parser.add_argument(
        '-t',
        '--today',
        help='set today in yyyy-mm-dd format',
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d')
    )
    # -c
    # --check
    parser.add_argument(
        '-c',
        '--check',
        help='enable check mode',
        action='store_true'
    )

    args = parser.parse_args()

    main(args)