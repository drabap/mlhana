# Clustering mit KMeans
from hana_ml.algorithms.pal.clustering import KMeans

kmeans = KMeans( n_clusters = 4,
    init = 'first_k',
    max_iter = 100,
    distance_level = 'Euclidean',
    category_weights = 0.5 )

g_df_kmeans_assignment = kmeans.fit_predict(
    data = g_df_mall_cust,
    key = 'CUSTOMERID' )

# Clusterzuweisung ausgeben
g_df_kmeans_assignment.collect()
