#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Listing: Verbindung zu HANA von Python
from hana_ml import dataframe

connection = dataframe.ConnectionContext( KEY = 'DEV' )


# In[2]:


# Listing: Tabelle CHURN abfragen und auf 100 Zeilen reduzieren

g_df_source = connection.table(table = 'CHURN',
                               schema = 'ML_DATA')

g_df_source.head(100).collect()


# In[3]:


# Listing: Entfernen von Spalten mit dem Deselect-Befehl
l_df_reduced = g_df_source.deselect(['ROWNUMBER','SURNAME'])
l_df_reduced.collect()


# In[4]:


# Selektion bestimmter Spalten
l_df_select = g_df_source.select(
    ['CUSTOMERID','CREDITSCORE','AGE','EXITED']
    )
l_df_select.collect()


# In[5]:


# Aufruf der Describe-Methode
g_df_source.describe(['CREDITSCORE','AGE',
                           'TENURE','NUMOFPRODUCTS',
                           'BALANCE']).collect()


# In[6]:


# Aggregation auf Ebene GEOGRAPHY und EXITED
l_df_exited_per_country = g_df_source.agg([
    ('count','CUSTOMERID','COUNT_CUSTOMER')],
    group_by = ['GEOGRAPHY','EXITED'])

l_df_exited_per_country.sort(
    ['GEOGRAPHY','EXITED']).collect()


# In[7]:


# Filterung von Kunden 
# Kunden in Frankreich mit einem Produkt oder Kunden in Deutschland mit 3 oder 4 Produkten
l_df_filter = g_df_source.filter("""
(Geography = 'France' AND NUMOFPRODUCTS = 1) 
OR 
(Geography = 'Germany' AND ( NUMOFPRODUCTS IN (3,4) ))""")
l_df_filter.collect()

# Validierung: 
#l_filter.distinct(['GEOGRAPHY',
#                      'NUMOFPRODUCTS']).collect()


# In[8]:


# UNION: Vereinigung zweier Kundengruppen
# Kunden in Frankreich mit einem Produkt und Kunden in Deutschland mit 3 oder 4 Produkten
l_df_france_1 = g_df_source.filter("""
Geography = 'France' AND NUMOFPRODUCTS = 1
""")
l_df_germany_3_4 = g_df_source.filter("""
Geography = 'Germany' 
AND  NUMOFPRODUCTS IN (3,4)""")

l_df_union = l_df_france_1.union(l_df_germany_3_4)
l_df_union.collect()
# Validierung:
#l_union.distinct(['GEOGRAPHY','NUMOFPRODUCTS']).collect()


# In[9]:


# Berechnete Spalten
l_df_calc = g_df_source.select(['CUSTOMERID','SURNAME',
                                     'BALANCE','EXITED'])
# Text für EXITED
l_df_w_text = l_df_calc.select('*',
                               ("""CASE EXITED WHEN 1 THEN 'EXITED' ELSE 'NOT EXITED' END""",
                                    'EXIT_LABEL')
                              )

# Balance > 0 ?
l_df_w_balance = l_df_w_text.select('*',
                                    ('CASE WHEN BALANCE > 0 THEN 1 ELSE 0 END',
                                     'HAS_BALANCE')
                                   )

l_df_w_balance.collect()


# In[10]:


# Binning der Spalte BALANCE
l_df = g_df_source.select(['CUSTOMERID','BALANCE'])
# Binning uniform number
l_df_bin = l_df.bin(col = 'BALANCE', 
                    strategy = 'uniform_number',
                    bins = 10, 
                    bin_column = 'BALANCE_BIN')

l_df_bin.collect()
# Optional: Ausgabe alle BINS
# l_df_bin.distinct('BALANCE_BIN').sort('BALANCE_BIN').collect()


# In[11]:


# Dataframe aus SQL
connection.sql("""SELECT * FROM SYS.M_TABLES 
WHERE SCHEMA_NAME = 'ML_DATA' """).collect()


# In[12]:


# Alternativ: Tabelle selektieren und Filter anwenden
connection.table('M_TABLES', schema = 'SYS').filter("SCHEMA_NAME = 'ML_DATA'").collect()


# In[13]:


# Neu ab 2.9: Alle Tabellen ausgeben
connection.get_tables(schema = 'ML_DATA')


# In[14]:


# Verbindung schließen
connection.close()


# In[ ]:




