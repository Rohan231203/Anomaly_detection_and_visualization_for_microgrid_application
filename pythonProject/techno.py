import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 0.1, 0.001)   # start,stop,step
y1 = np.sin(2*np.pi*50*x)	# 50 Hz Sine

plt.plot(x, y1)
plt.show()