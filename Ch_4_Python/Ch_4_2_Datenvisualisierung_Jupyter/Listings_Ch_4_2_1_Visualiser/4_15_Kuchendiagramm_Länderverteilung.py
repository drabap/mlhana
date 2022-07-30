# Kuchendiagramm Länderverteilung plotten
fig_pieplot = plt.figure(figsize = (18,6))
ax1 = fig_pieplot.add_subplot(121)
eda = EDAVisualizer(ax1)

ax1, pie_data = eda.pie_plot(
    data = g_df_churn,
    explode = 0.03,
    column = 'GEOGRAPHY')
