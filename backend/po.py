import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model

df = pd.read_csv("pred.csv")

x=np.asarray(df['NO']).reshape(-1,1)
y = df['C']

regr = linear_model.LinearRegression()
regr.fit(x,y)
y_pred = regr.predict(x)

plt.scatter(x, y, color="black" )
plt.plot(x, y_pred, color="blue", linewidth=3)

plt.ylim(0,1)
#plt.show()

print(regr.predict([[30]]))