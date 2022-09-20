# 4_17 Streudiagramm mit Iris-Daten
fig_scatter_iris = plt.figure(figsize=(18,6))

ax1 = fig_scatter_iris.add_subplot(121)
eda = EDAVisualizer(ax1)

# Color maps:
# Greys: Graustufen
#     Reds, Blues
ax1, scatter_data = eda.scatter_plot(
    data = g_df_iris,
    x = 'SEPAL_WIDTH',
    y = 'SEPAL_LENGTH',
    x_bins = 4, y_bins = 4,
    debrief = True,
    cmap = 'Blues')
