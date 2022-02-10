import Analyzer

mk = Analyzer.MarketDB()

print(mk.get_daily_price('삼성전자', '2020-01-01', '2021-08-22'))