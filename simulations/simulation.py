
import numpy as np
import matplotlib.pyplot as plt

E = np.linspace(0.5,5,100)
delta = 0.05

E_true = E*(1+delta)
sigma_obs = E**2
sigma_true = E_true**2

plt.plot(E, sigma_true/sigma_obs)
plt.show()
