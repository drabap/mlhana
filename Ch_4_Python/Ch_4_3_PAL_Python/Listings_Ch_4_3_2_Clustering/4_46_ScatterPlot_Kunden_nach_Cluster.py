# Streudiagramm der Kunden nach Cluster
# Filtern auf Punkte in Cluster, dann umwandeln in Pandas
l_pd_frame = g_df_cust_w_cluster.filter(
    "CLUSTER_ID >= 0").collect()

l_pd_frame["CLUSTER_ID"] = l_pd_frame["CLUSTER_ID"].astype('category')
l_pd_frame["CLUSTER_ID"] = l_pd_frame["CLUSTER_ID"].cat.codes

# Scatter Plot
l_pd_frame.plot(kind = "scatter",
    x = "AGE",
    y = "SPENDINGSCORE",
    c = "CLUSTER_ID",
    cmap = 'tab20c')
