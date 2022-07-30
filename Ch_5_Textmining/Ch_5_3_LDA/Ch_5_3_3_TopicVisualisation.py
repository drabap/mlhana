#!/usr/bin/env python
# coding: utf-8

# # Themenverteilung visualisieren

# ## Themenscores abrufen und pivotisieren

# In[1]:


# HANA-Dataframe mit Ergebnis der Themenextraktion
# Vorausssetzung: LDA wurde HANA-seitig ausgeführt und Themenzuweisung ist in Tabelle ML_TEXT.PAL_LDA_DOCUMENT_TOPIC_DIST gespeichert

from hana_ml import dataframe

connection = dataframe.ConnectionContext( KEY = 'DEV')
df = connection.table('PAL_LDA_DOCUMENT_TOPIC_DIST',
                      schema = 'ML_TEXT')

# Beispielausgabe
df.sort(['KEY','TOPIC_ID']).head(20).collect()


# In[2]:


# Transponieren der Themenscores in Spalten
topics_pivot = df.pivot_table( columns = 'TOPIC_ID',
    values = 'PROBABILITY',
    index = 'KEY',
    aggfunc = 'AVG')

topics_pivot.collect()


# ## Projizieren der Daten mit t-SNE 

# In[3]:


# Anwenden des t-SNE-Algorithmus

from hana_ml.algorithms.pal.tsne import TSNE

tsne = TSNE(n_iter = 500,
            random_state = 1,
            n_components = 3,
            angle = 0.0,
            exaggeration = 20,
            learning_rate = 200,
            perplexity = 30,
            object_frequency = 50,
            thread_ratio = 0.5
           )

df_tsne_res, stats, obj = tsne.fit_predict(
                                   data = topics_pivot, 
                                   key = 'KEY' )

df_tsne_res.collect()


# In[4]:


# Scatter Plot vom t-SNE-Ergebnis
pd_res = df_tsne_res.collect()

pd_res.plot( kind = 'scatter',  
              x = 'x',
              y = 'y',
              c = 'z',
              cmap = 'coolwarm' )


# ## Zusatz: Clustern der projezierten Daten

# In[5]:


# Clustern der projizierten Daten
from hana_ml.algorithms.pal.clustering import DBSCAN

dbscan = DBSCAN( minpts = 50,
                 eps = 5,
                 metric = 'euclidean' )

# Clustering durchführen und Zuweisung zwischenspeichern
df_cluster_assignment = dbscan.fit_predict( 
                                        data = df_tsne_res,
                                        key = 'KEY' )


# Cluster anzeigen:
# Anzahl Sätze pro Cluster
cluster_agg = df_cluster_assignment.agg( [
                       ('count','KEY','COUNT_DOCS')
                       ],
                       group_by = ['CLUSTER_ID'] )

# Zählen der Dokumente pro Cluster
cluster_agg.sort(['CLUSTER_ID']).collect()

# Optional: Ausgabe der Zuweisung pro Dokument
#cluster_assignment.collect()


# In[6]:


# JOIN zwischen t-SNE und Clusterzuweisung => Für jedes Dokument werden die projizierten Koordinaten und deren Clusterzuweisung in einer Tabelle zusammengeführt
# Input: df_tsne_res, df_cluster_assignment

df_cluster_assignment_1 = df_cluster_assignment.rename_columns({'KEY' : 'CLST_KEY'})
df_tsne_with_cluster = df_tsne_res.alias('TSNE').join(other = df_cluster_assignment_1.alias('CLST'),
                                                      condition = 'KEY = CLST_KEY' ).drop('CLST_KEY')

df_tsne_with_cluster.collect()


# In[7]:


# Dokumente nach projizierten Features aus t-SNE mit Clusterzuweisung visualisieren
# Input: df_tsne_with_cluster=> Koordinaten in 3D mit Cluster-Zuweisung

pd_tsne_with_cluster = df_tsne_with_cluster.collect()

pd_tsne_with_cluster['CLUSTER_ID'] = pd_tsne_with_cluster['CLUSTER_ID'].astype('category')
pd_tsne_with_cluster['CLUSTER_ID'] = pd_tsne_with_cluster['CLUSTER_ID'].cat.codes

pd_tsne_with_cluster.plot( kind = 'scatter', x = 'x', y = 'y',
                                             c = 'CLUSTER_ID', cmap = 'tab20' )
# Alternative CMAPS: tab10, tab20, tab20c


# In[8]:


connection.close()


# In[ ]:




