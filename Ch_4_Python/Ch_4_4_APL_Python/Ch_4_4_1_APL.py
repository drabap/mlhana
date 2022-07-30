#!/usr/bin/env python
# coding: utf-8

# # APL verwenden
# 
# - Modell trainieren
# 
# - Indikatoren und Kennzahlen auslesen
# 
# - Prognose mit Modell erstellen
# 
# 

# ## Modell trainieren
# 

# In[1]:


# Verbindung zur HANA und Aufteilen der Daten
from hana_ml import dataframe
from hana_ml.algorithms.pal import partition

connection = dataframe.ConnectionContext( KEY = 'DEV')

# CHURN laden
l_df_churn = connection.table('CHURN', schema = 'ML_DATA')

l_df_churn_red = l_df_churn.deselect(['ROWNUMBER','SURNAME'])

g_df_train, g_df_test, g_df_valid = partition.train_test_val_split( 
                                                    data = l_df_churn_red,
                                                    id_column = 'CUSTOMERID', 
                                                    partition_method = 'stratified',
                                                    training_percentage = 0.6, 
                                                    validation_percentage = 0.0,
                                                    testing_percentage = 0.4,
                                                    stratified_column = 'EXITED' 
   )


# In[2]:


# Initialisieren und Konfigurieren des Gradient-Boosting
from hana_ml.algorithms.apl.gradient_boosting_classification  import GradientBoostingBinaryClassifier

g_gradboost_c = GradientBoostingBinaryClassifier()

# Konfigurieren mit optionalen Parametern
g_gradboost_c.set_params(
 eval_metric = 'LogLoss',
 max_depth = 4,
 learningrate = 0.05   
)


# In[3]:


# Variablen konfigurieren
# Variablen werden automatisch mit Vorschlagswerten initialisiert. Die manuelle Zuweisung ist somit optional
g_gradboost_c.set_params(
   variable_value_types = {
       'AGE' : 'continuous'
   }
)


# In[4]:


# Modelltraining mit APL
g_gradboost_c.fit( g_df_train, 
                   label = 'EXITED', 
                   key = 'CUSTOMERID' )


# ## Indikatoren und Kennzahlen auslesen

# In[5]:


# Metriken des Modells ausgeben
g_gradboost_c.get_performance_metrics()


# In[7]:


# Einfluss der Eingabevariablen ausgeben
g_gradboost_c.get_feature_importances()


# In[8]:


## Prognosebildung mit APL

l_df_result = g_gradboost_c.predict( g_df_test )

l_df_result.collect()


# In[ ]:




