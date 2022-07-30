# Histogramm für die Variable AGE
fig = plt.figure(figsize = (18,6))

ax1 = fig.add_subplot(121)
eda = EDAVisualizer(ax1)

ax1, dist_data = eda.distribution_plot(
    data = g_df_churn,
    column = 'AGE',
    bins = 10,
    title = 'Verteilung des Alters aller Kunden')
