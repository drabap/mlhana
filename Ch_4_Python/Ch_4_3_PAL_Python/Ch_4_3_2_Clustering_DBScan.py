#!/usr/bin/env python
# coding: utf-8

# # Clustering-Analysen

# - DBScan (PAL) auf Mall Data anwenden
# -- Vorbereitung: Selektieren und Visualisieren von Mall Data (Tabelle MALL_CUSTOMERS)
# -- Anwendung von DBSCAN
# -- Auswertung mit Streudiagramm und Box-Plot
# - Verwendung von KMeans
# -- Ergänzung: Variable Clusterzahl bei KMeans und Visualisierung von KMeans-Ergebnis
# -- Zusatz: Cluster-Modelle speichern zur späteren Verwendung
# 
# 

# ## Vorbereitung

# In[12]:


# MALL_CUSTOMERS selektieren
from hana_ml import dataframe

conn = dataframe.ConnectionContext(KEY = 'DEV')

g_df_mall_cust = conn.table(table = 'MALL_CUSTOMERS',
                            schema = 'ML_DATA')

# df_mall_cust.describe().collect()
# df_mall_cust.head(20).collect()


# In[13]:


# Scatter Plot Age vs. SpendingScore
from hana_ml.visualizers.eda import EDAVisualizer
import matplotlib.pyplot as plt

fig_scatter = plt.figure(figsize=(18,6))

ax1 = fig_scatter.add_subplot(121)
eda = EDAVisualizer(ax1)

# Color maps:
# Greys: Graustufen
# Reds, Blues

ax1, scatter_data = eda.scatter_plot(
                                  data = g_df_mall_cust, 
                                  x = 'AGE', 
                                  y = 'SPENDINGSCORE', 
                                  x_bins = 10, 
                                  y_bins = 10,
                                  debrief = True, 
                                  cmap = 'Blues')

# Kompression bei Scatter Plot: 10 bins in X und Y = 100 Datenpunkte. Bei 10000 Kunden bereits Faktor 100


# ## Clustering mit DBScan

# In[14]:


# Aufruf von DBScan und Ausgabe der Cluster
from hana_ml.algorithms.pal.clustering import DBSCAN

dbscan = DBSCAN(minpts = 5,
                eps = 10,
                metric = 'euclidean')

# Ergebnis des Clustering
g_df_cluster_assignment = dbscan.fit_predict(
                                        data = g_df_mall_cust,
                                        key = 'CUSTOMERID')
# Cluster anzeigen:
# Anzahl Sätze pro Cluster
l_df_cluster_agg = g_df_cluster_assignment.agg([
                       ('count','CUSTOMERID','COUNT_CUSTOMER')
                       ],
                       group_by = ['CLUSTER_ID'])

l_df_cluster_agg.sort(['CLUSTER_ID']).collect()


# In[15]:


# Join zwischen Cluster-Zuweisung und Kundendaten
l_df_cluster_1 = g_df_cluster_assignment.rename_columns({'CUSTOMERID' : 'CL_CUSTID'})

l_df_cust_w_cluster = g_df_mall_cust.alias('CUST').join(
                                          other = l_df_cluster_1.alias('CLST'),
                                          condition = 'CUSTOMERID = CL_CUSTID')

# Entferne überflüssige Spalte CL_CUSTID
g_df_cust_w_cluster = l_df_cust_w_cluster.drop('CL_CUSTID')

g_df_cust_w_cluster.head(20).collect()


# ### Visualisieren der Ergebnisse

# In[16]:


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
                 


# In[17]:


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


# ## Clustering mit KMeans

# In[18]:


# Clustering mit K-Means 
from hana_ml.algorithms.pal.clustering import KMeans

kmeans = KMeans(n_clusters = 4,
                init = 'first_k',
                max_iter = 100,
                distance_level = 'Euclidean',
                accelerated = True,
                category_weights = 0.5)

g_df_kmeans_assignment = kmeans.fit_predict(
                                          data = g_df_mall_cust,
                                          key = 'CUSTOMERID' )
# Cluster.Zuweisung ausgeben
g_df_kmeans_assignment.collect()


# In[19]:


# Zentrumspunkte der Cluster
kmeans.cluster_centers_.collect()


# ## Predict: Clusterzuweisung für neue Daten

# In[20]:


# Mit Predict das Cluster-Modell auf neue Daten anwenden 
# Beispiel für DBScan 
l_df_subset = g_df_mall_cust.head(10)

l_df_subset_cluster = dbscan.predict(data = l_df_subset,
                                     key = 'CUSTOMERID')
l_df_subset_cluster.collect()


# In[21]:


# Ergänzung: Predict mit K-Means
l_df_subset = g_df_mall_cust.head(10)

l_df_subset_cluster = kmeans.predict(data = l_df_subset,
                                     key = 'CUSTOMERID')
l_df_subset_cluster.collect()


# ## Ergänzung: Variable Clusterzahl bei KMeans und Visualisierung der KMeans-Cluster
# - Aufruf von KMeans mit einem Intervall der erlaubten Clusterzahl
# - Erzeugen von Streudiagramm und Box-Plot für KMeans-Ergebnis (analog zu Vorgehen im Buch bei DBSCAN)

# In[22]:


# Ergänzung: KMeans mit variabler Clusterzahl
kmeans_var = KMeans(n_clusters_min = 2,
                    n_clusters_max = 10,   
                    init = 'first_k',
                    max_iter = 100,
                    distance_level = 'Euclidean',
                    accelerated = True,
                    category_weights = 0.5)

g_df_kmeans_assignment_var = kmeans_var.fit_predict(
                                            data = g_df_mall_cust,
                                            key = 'CUSTOMERID')
# Cluster.Zuweisung ausgeben
kmeans_var.cluster_centers_.collect()


# In[23]:


# Ergänzung K-Means
# JOIN zwischen Clusterzuweisung und df_mall_cust
# Verwendung der Zuweisung aus Durchlauf mit variabler Clusterzahl
l_df_kmeans_assignment_1 = g_df_kmeans_assignment_var.rename_columns({'CUSTOMERID': 'CUSTOMERID_CLST'})


l_df_cust_w_cluster = g_df_mall_cust.alias('CUST').join(other = l_df_kmeans_assignment_1.alias('CLST'),
                                          condition = 'CUSTOMERID = CUSTOMERID_CLST' )

# Remove redundant column CUSTOMERID_CLST
g_df_cust_w_kmeans = l_df_cust_w_cluster.drop('CUSTOMERID_CLST')

g_df_cust_w_kmeans.head(20).collect()


# In[24]:


# Ergänzung K-Means
# Scatter Plot mit Pandas
l_pd_frame = g_df_cust_w_kmeans.collect()

l_pd_frame["CLUSTER_ID"] = l_pd_frame["CLUSTER_ID"].astype('category')
l_pd_frame["CLUSTER_ID"] = l_pd_frame["CLUSTER_ID"].cat.codes

# Scatter Plot
l_pd_frame.plot( kind = "scatter", x = "AGE", y = "SPENDINGSCORE",
                                   c = "CLUSTER_ID", cmap = 'Dark2' )


# In[25]:


# Ergänzung K-Means
# Verteilung Boxplot je nach Cluster

# Boxplot für die Variable AGE

f = plt.figure(figsize=(18,6))

ax1 = f.add_subplot(121)
eda = EDAVisualizer(ax1)

l_df_cust_w_kmeans = g_df_cust_w_kmeans.cast('CLUSTER_ID','NVARCHAR(2)')

ax, bar_data = eda.box_plot(data = l_df_cust_w_kmeans,
                            column = 'SPENDINGSCORE',
                            groupby = 'CLUSTER_ID',
                            outliers = True)


# ## Zusatz: Speichern der Cluster-Modelle
# - Dieser Code basiert auf dem Vorgehen, das in Abschnitt 4.3.3 "Modelle speichern und wiederverwenden" dargestellt wird.
# - Lesen Sie zunächst die Schritte im Buch durch.

# In[37]:


from hana_ml.model_storage import ModelStorage, ModelStorageError
MODEL_SCHEMA = 'ML_MODEL' # HANA-Schema in dem die erzeugten Modelle gespeichert werden

model_storage = ModelStorage(connection_context = conn, schema = MODEL_SCHEMA)

# Voraussetzung: Das Clustering mit DBSCAN (weiter oben) wurde ausgeführt
dbscan.name = 'DBScan Mall 1'
model_storage.save_model(model = dbscan, if_exists = 'upgrade')


# In[38]:


# Ausgabe der gespeicherten Modelle
model_storage.list_models()


# In[40]:


# Laden des Modells und Ausführen der Clusterzuweisung mit predict
# Laden von bestimmter Version
dbscan_loaded = model_storage.load_model(name = 'DBScan Mall 1', version = 4)
# Alternativ: Immer die neueste Version nehmen:
# dbscan_loaded = model_storage.load_model( name = 'DBScan Mall 1' )

print(dbscan_loaded)

# Predict anwenden (=> führt die Clusterzuweisung durch)
l_df_subset = g_df_mall_cust.head(30)

l_df_subset_cluster = dbscan_loaded.predict(data = l_df_subset,
                                           key = 'CUSTOMERID')

l_df_subset_cluster.collect()


# In[ ]:




