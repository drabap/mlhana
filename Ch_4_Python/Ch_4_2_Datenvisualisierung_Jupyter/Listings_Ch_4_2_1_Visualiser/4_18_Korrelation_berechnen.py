# Korrelation berechnen
fig_correlation_iris = plt.figure(figsize=(18,6))

ax1 = fig_correlation_iris.add_subplot(121)
eda = EDAVisualizer(ax1)

ax1, scatter_data = eda.correlation_plot(
    data = g_df_iris,
    corr_cols = ['SEPAL_LENGTH','SEPAL_WIDTH',
                 'PETAL_LENGTH','PETAL_WIDTH'],
    cmap = 'Reds')
