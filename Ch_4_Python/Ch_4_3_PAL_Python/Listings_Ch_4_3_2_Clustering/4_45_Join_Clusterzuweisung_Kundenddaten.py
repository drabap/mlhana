# Join zwischen Cluster-Zuweisung und Kundendaten
l_df_cluster_1 = g_df_cluster_assignment.rename_columns(
    {'CUSTOMERID' : 'CL_CUSTID'})

l_df_cust_w_cluster = g_df_mall_cust.alias('CUST').join(
    other = l_df_cluster_1.alias('CLST'),
    condition = 'CUSTOMERID = CL_CUSTID')

# Entferne überflüssige Spalte CL_CUSTID
g_df_cust_w_cluster = l_df_cust_w_cluster.drop('CL_CUSTID')
g_df_cust_w_cluster.head(20).collect()

