# Plotten der Variablenwichtigkeit
from hana_ml.visualizers.eda import EDAVisualizer
import matplotlib.pyplot as plt

fig_barplot = plt.figure(figsize = (18,6))
ax1 = fig_barplot.add_subplot(121)
eda = EDAVisualizer(ax1)

ax1, bar_data = eda.bar_plot(
    data = df_feature_importance,
    column = 'VARIABLE_NAME',
    aggregation = {'IMPORTANCE':'avg'})
