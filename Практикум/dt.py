import pandas as pd
import matplotlib.pyplot as plt

value = [1000,1200,900,123,5000]
time = ['17.00', '19.00', '20.00', '21.00', '20.23']
energyEffect = pd.Series(index = time , data = value)

print(energyEffect)

energyEffect = energyEffect.cumsum()

plt.figure()

energyEffect.plot()
plt.show()