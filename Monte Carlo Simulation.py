import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Analyzer
import DBUpdater

dbu = DBUpdater.DBUpdater()


mk = Analyzer.MarketDB()
stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
df = pd.DataFrame()
for s in stocks:
    df[s] = mk.get_daily_price(s, '2017-07-19', '2021-08-11')['close']

daily_ret = df.pct_change()  # 수익률 계산 함수
annual_ret = daily_ret.mean() * 252  # 252는 1년 평균 개장일
daily_cov = daily_ret.cov()  # 공분산 함수를 통해 일간 리스크를 구한다.
annual_cov = daily_cov * 252

port_ret = []
port_risk = []
port_weights = []

# 몬테카를로 시뮬레이션
for _ in range(20000):
    weights = np.random.random(len(stocks))
    weights /= np.sum(weights)

    returns = np.dot(weights, annual_ret)
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))

    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)

portfolio = {'Returns' : port_ret, 'Risk' : port_risk}
for i, s in enumerate(stocks):
    portfolio[s] = [weight[i] for weight in port_weights]
df = pd.DataFrame(portfolio)
df = df[['Returns', 'Risk'] + [s for s in stocks]]
df = df.sort_values(by=['Risk'], axis=0, ascending=False)
print(df)
df = df.sort_values(by=['Returns'], axis=0, ascending=False)
print(df)



df.plot.scatter(x='Risk', y='Returns', figsize=(10,7), grid=False)
plt.title('Efficient Frontier')
plt.xlabel('Risk')
plt.ylabel('Expected Returns')
plt.show()