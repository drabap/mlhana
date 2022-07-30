# Aufruf von DBScan und Ausgabe der Cluster
from hana_ml.algorithms.pal.clustering import DBSCAN

dbscan = DBSCAN( minpts = 5,
    eps = 10,
    metric = 'euclidean' )

# Ergebnis des Clustering
g_df_cluster_assignment = dbscan.fit_predict(
    data = g_df_mall_cust,
    key = 'CUSTOMERID' )

l_df_cluster_agg = g_df_cluster_assignment.agg( [
    ('count','CUSTOMERID','COUNT_CUSTOMER')
    ],
    group_by = ['CLUSTER_ID'] )
l_df_cluster_agg.sort(['CLUSTER_ID']).collect()
