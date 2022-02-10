import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Analyzer

mk = Analyzer.MarketDB()
stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
df = pd.DataFrame()
for s in stocks:
    df[s] = mk.get_daily_price(s, '2017-07-19', '2021-08-11')['close']

daily_ret = df.pct_change()  # 수익률 계산 함수
annual_ret = daily_ret.mean() * 252  # 252는 1년 평균 개장일
daily_cov = daily_ret.cov()  # 공분산 함수를 통해 일간 리스크를 구한다.
annual_cov = daily_cov * 252

port_ret = []   # 수익률
port_risk = []  # 리스크
port_weights = []   # 종목별 비중
sharpe_ratio = []   # 샤프 지수, 샤프 지수는 측정된 위험 단위당 수익률을 계산함. 즉, 샤프 지수가 높을수록 위험에 대한 보상이 더 크다.

for _ in range(20000):
    weights = np.random.random(len(stocks))  # 4개의 랜덤 숫자로 구성된 배열 생성
    weights /= np.sum(weights)  # 4개의 랜덤 숫자를 랜덤 숫자의 총합으로 나눠 종목 비중의 합이 1이 되도록 함

    returns = np.dot(weights, annual_ret)  # 랜덤하게 생성된 종목별 비중 배열과 종목별 연간 수익률을 곱해 해당 포트폴리오의 전체 수익률을 구함
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))  # 포트폴리오의 리스크를 계산하는 함수

    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)
    sharpe_ratio.append(returns/risk)

portfolio = {'Returns' : port_ret, 'Risk' : port_risk, 'Sharpe' : sharpe_ratio}
for i, s in enumerate(stocks):  # i는 0~4, s는 상장회사명으로 지정
    portfolio[s] = [weight[i] for weight in port_weights]   # 상장회사 순서대로 비중값을 추가
df = pd.DataFrame(portfolio)
df = df[['Returns', 'Risk', 'Sharpe'] + [s for s in stocks]]
print(df.sort_values(by=['Sharpe'], axis=0, ascending=True))  # 오름차순 정렬

max_sharpe = df.loc[df['Sharpe'] == df['Sharpe'].max()]
min_risk = df.loc[df['Risk'] == df['Risk'].min()]

df.plot.scatter(x='Risk', y='Returns', c='Sharpe', cmap='viridis', edgecolors='k', figsize=(11, 7), grid=True)
plt.scatter(x=max_sharpe['Risk'], y=max_sharpe['Returns'], c='r', marker='*', s=300)    # 샤프 지수가 가장 큰 포트폴리오를 300 크기의 별표로 표시
plt.scatter(x=min_risk['Risk'], y=min_risk['Returns'], c='r', marker='X', s=200)    # 리스크가 가장 작은 포트폴리오를 200크기의 x로 표시

plt.title('Portfolio Optimization')
plt.xlabel('Risk')
plt.ylabel('Expected Returns')
plt.show()