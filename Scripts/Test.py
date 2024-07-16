import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
    

data = {"Value": 3*np.sin(np.arange(48)*2*np.pi/(12)) + np.random.rand(48)}
dates = pd.date_range(start='2020-01-01', periods=len(data["Value"]), freq='ME')
df = pd.DataFrame(data, index=dates)
df.index = pd.to_datetime(df.index)

monthly_avg = df["Value"].groupby(df.index.month).mean()
#monthly_avg = df.groupby(df.index.month).mean()
monthly_avg.index.name = "Month"
df["Monthly Avg"] = df.index.month.map(monthly_avg)

