# Boxplot für SPENDINGSCORE je Cluster
f = plt.figure(figsize=(18,6))

ax1 = f.add_subplot(121)
eda = EDAVisualizer(ax1)

l_df_cust_2 = g_df_cust_w_cluster.cast('CLUSTER_ID',
    'NVARCHAR(2)')

ax, bar_data = eda.box_plot(data = l_df_cust_2,
    column = 'SPENDINGSCORE',
    groupby = 'CLUSTER_ID',
    outliers = True)

