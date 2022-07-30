#!/usr/bin/env python
# coding: utf-8

# # Klassifikation von Dokumenten mit k-nearest Neighbours (k-NN)

# ## Daten vorbereiten

# In[2]:


# HANA-Dataframe für den Dokumentenkorpus 
# Quelltabelle: ML_TEXT.NEWSCORP

# Verbindung zur HANA
from hana_ml import dataframe

connection = dataframe.ConnectionContext( KEY = 'DEV')

df_newscorp = connection.table('NEWSCORP', 
                               schema = 'ML_TEXT')

# Umwandeln von CLOB nach NVARCHAR - Textmining-Paket unterstützt nur 5000 Zeichen
df_text = df_newscorp.cast('TEXT', 'NVARCHAR(5000)')

# Spalten umbenennen nach Vorgabe der Methode für Textklassifikation
df_input_knn = df_text.select(('KEY','ID'),
                                  ('TEXT','CONTENT'),
                                  'CATEGORY')
# Ausgabe der Daten zur Kontrolle
df_input_knn.collect()


# In[3]:


# Splitten der Dokumentenmenge

# Referenzdokumente => die ersten 1000 Dokumente
df_reference = df_input_knn.filter('ID <= 1000')
# l_df_train.describe().collect()

# Testdokumente => Zufällig 250 mit ID > 1000
df_test = df_input_knn.filter('ID > 1000').head(250)

# Zielvariable CATEGORY entfernen
df_input_test = df_test.drop('CATEGORY')
df_input_test.collect()


# ## Aufruf der Klassifikationsfunktion 

# In[4]:


# Aufruf der Textklassifikation
from hana_ml.text.tm import text_classification
res = text_classification( pred_data = df_input_test,
                          ref_data  = df_reference,
                          k_nearest_neighbours = 5,
                          thread_ratio = 0.5 )

res.select('ID','RANK','CATEGORY_VALUE','SCORE').collect()


# ### Vergleich der prognostizierten und tatsächlichen Kategorie

# In[5]:


# Vergleich von Prognose und Ist
# Prognose der Kategorie => Kategorie mit RANK = 1 selektieren
res_predicted = res.filter('RANK = 1').select('ID','CATEGORY_VALUE','SCORE')

compare = res_predicted.alias('RES').join( df_input_knn.alias('INP'),
                                           condition = 'RES.ID = INP.ID',
                                           how = 'inner',
                                           select = [('RES.ID','KEY'),
                                                     ('INP.CATEGORY','CAT_ACTUAL'),
                                                     ('RES.CATEGORY_VALUE','CAT_PREDICTED'),
                                                     ('RES.SCORE','SCORE')
                                                     ])

compare.sort(['KEY','CAT_ACTUAL']).collect()


# In[6]:


# Zählen der richtigen und falschen Klassifikationen
compare_agg = compare.agg( 
    agg_list = [('count','KEY','col_count')] ,
    group_by = ['CAT_ACTUAL','CAT_PREDICTED']).sort(['CAT_ACTUAL','CAT_PREDICTED'])

compare_agg.collect()


# In[7]:


# Ergänzung: die Confusion Matrix berechnen
compare_pivot = compare_agg.pivot_table( values = 'col_count', 
                         index = 'CAT_PREDICTED',
                         columns = 'CAT_ACTUAL',
                         aggfunc = 'SUM' )


compare_pivot.select('CAT_PREDICTED','business',
                     'entertainment',
                     'politics',
                     'sport',
                     'tech').collect()


# In[8]:


connection.close()


# In[ ]:




