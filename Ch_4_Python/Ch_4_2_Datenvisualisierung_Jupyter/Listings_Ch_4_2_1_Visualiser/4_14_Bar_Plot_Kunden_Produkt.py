# Bar-Plot: Kunden nach Produkt
fig_barplot = plt.figure(figsize = (18,6))
ax1 = fig_barplot.add_subplot(121)
eda = EDAVisualizer(ax1)

ax1, bar_data = eda.bar_plot(
    data = g_df_churn,
    column = 'NUMOFPRODUCTS',
    aggregation = {'CUSTOMERID' : 'count'}) 
