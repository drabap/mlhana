# Scatter Plot Age vs. Spending Score
from hana_ml.visualizers.eda import EDAVisualizer
import matplotlib.pyplot as plt

fig_scatter = plt.figure(figsize=(18,6))

ax1 = fig_scatter.add_subplot(121)
eda = EDAVisualizer(ax1)

ax1, scatter_data = eda.scatter_plot( 
    data = g_df_mall_cust,
    x = 'AGE',
    y = 'SPENDINGSCORE',
    x_bins = 10,
    y_bins = 10,
    debrief = True,
    cmap = 'Blues')
