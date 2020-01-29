import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

df = pd.read_csv("TSLAdaily.csv", sep=',', decimal='.', index_col="Date",
                 parse_dates=True, usecols=["Date", "Close", "Volume"], na_values="nan")

df1 = pd.read_csv("TSLAdaily.csv", sep=',', decimal='.', index_col="Date",
                  parse_dates=True, usecols=["Date", "High", "Low"], na_values="nan")

df2 = pd.read_csv("AAPL.csv", sep=',', decimal='.', index_col="Date",
                  parse_dates=True, usecols=["Date", "High", "Low"], na_values="nan")

df3 = pd.read_csv("TSLAdaily.csv", sep=',', decimal='.', index_col="Date",
                 parse_dates=True, usecols=["Date", "Volume"], na_values="nan")

#Volumen in Millionen
df3['Volume'] = np.round((df3['Volume']/100000).rolling(window=7).mean(), 2)

#42 Tage Trend
df['S42d'] = np.round(df['Close'].rolling(window=42).mean(), 2)

#252 Tage Trend
df['S252d'] = np.round(df['Close'].rolling(window=252).mean(), 2)

#Differenz 42-Tage-Trend und 252-Tage-Trend
df['TSLADiff'] = df['S42d']-df['S252d']

#Wenn Differenz Positiv, dann Kaufempfehlung
df['TSLABuy'] = np.where(df['TSLADiff'] > 10, 50, 0)

fig, ax1 = plt.subplots()
ax1.plot(df)
ax1.set_xlabel('Date')
ax1.set_ylim(-60, 400)
ax1.set_ylabel('Shareprice in $')
ax1.tick_params('y')
ax1.legend(('Closing Value', 'Volume', '42d Trend', '252d Trend', 'Trend-Diff', 'Buy'), loc='upper center', bbox_to_anchor=(0.5, -0.24), shadow=True, ncol=3)

ax2 = ax1.twinx()
ax2.plot(df3, '#FF7F11')
ax2.set_ylim(-60, 400)
ax2.set_ylabel('Volume in 100k', color='#FF7F11')
ax2.tick_params('y', colors='#FF7F11')

fig.tight_layout()
plt.title("TSLA Share Visualization for Rating")

plt.savefig("close.png", bbox_inches="tight", dpi=300)

#Differenz zwischen Tages Hoch und Tief TSLA
df1['DailyDiff TSLA'] = np.round((df1['High'] - df1['Low']).rolling(window=7).mean(), 2)

#Differenz zwischen Tages Hoch und Tief AAPL als Vergleich
df1['DailyDiff AAPL'] = np.round((df2['High'] - df2['Low']).rolling(window=7).mean(), 2)

#Löschen nicht genutzter Spalten
df1 = df1.drop(columns="High")
df1 = df1.drop(columns="Low")

result2 = df1.plot(title="Weekly Difference between High and Low Price per Share")
result2.set_ylabel("Difference High/Low in $")
plt.savefig("dailyDiff.png", bbox_inches="tight", dpi=300)
