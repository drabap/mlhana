# Mit Predict das Cluster-Modell auf neue Daten anwenden
l_df_subset = g_df_mall_cust.head(10)

l_df_subset_cluster = dbscan.predict(data = l_df_subset,
    key = 'CUSTOMERID')

l_df_subset_cluster.collect()
