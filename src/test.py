from nplot import Figure
import pandas as pd
import numpy as np
#import seaborn as sns
import matplotlib.pyplot as plt
import Tkinter


# Uniformly sample points in [0,1]

N = 100
x = np.sort(np.random.rand(N))
y = 2*x + np.random.normal(0, 0.5, N)

df= pd.DataFrame({'x':x, 'y':y})


F = Figure()
F.scatter(df.x, df.y, regression=True)
#tips = sns.load_dataset("tips")
#sns.lmplot("total_bill", "tip", tips)
F.window.tk.mainloop()
