import pandas as pd
import pymysql
import datetime
from datetime import timedelta
import re

class MarketDB:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', user='root', password='chovionon2982#', db='stockdata', charset='utf8')
        self.codes = {}
        self.get_comp_info()

    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()

    def get_comp_info(self):
        """company_info 테이블에서 읽어와서 codes에 저장"""


    def get_daily_price(self, code, start_date=None, end_date=None):
        """KRX 종목별 시세를 데이터프레임 형태로 반환"""
        if start_date is None:
            one_year_ago = datetime.today() - timedelta(days=365)
            start_date = one_year_ago.strftime('%Y-%m-%d')
            print('start_date is initialized to "{}"'.format(start_date))
        else:
            start_lst = re.split('\D+', start_date)
            start_year = int(start_lst[0])
            start_month = int(start_lst[1])
            start_day = int(start_lst[2])
            start_date = f"{start_year:04d}-{start_month:02d}-{start_day:02d}"
            print("start_date: ", start_date)

        sql = f"SELECT * FROM daily_price WHERE code = '{code}'"\
            f" and date >= '{start_date}' and date <= '{end_date}'"
        df = pd.read_sql(sql, self.conn)
        df.index = df['date']
        return df
