#!/usr/bin/env python
# coding: utf-8

# # Speichern von Modellen
# * Vorbereitung: Random Forest trainieren
# * Modell speichern
#  * Ergänzung Metriken zum Modell speichern
# * Modell laden und zur Prognose verwenden
# * Aufräumarbeiten

# ## Vorbereitung: Random Forest trainieren

# In[ ]:


# Wiederholung: RandomForest trainieren (Übernahme aus Ch4_Python_Sub_3_Section1_PAL_RandomFor_NN)
# Übernahme Listings: 4.27 Verbindung zur HANA, 4.28 Daten partitionieren, 4.29 Trainieren des RandomForest
from hana_ml import dataframe

connection = dataframe.ConnectionContext( KEY = 'DEV')

# CHURN laden
g_df_churn = connection.table('CHURN', schema = 'ML_DATA')

g_df_churn.head(20).collect()

#  Daten partitionieren
from hana_ml.algorithms.pal import partition

g_df_train, g_df_test, g_df_valid = partition.train_test_val_split(
                                                    g_df_churn,
                                                    partition_method = 'stratified',
                                                    training_percentage = 0.6, validation_percentage = 0.0,
                                                    testing_percentage = 0.4,
                                                    stratified_column = 'EXITED' )

# Anzahl Kündigungen in Trainingsmenge
# train.agg([('count','CUSTOMERID','count_customer')] , group_by = ['EXITED']).collect()
# test.agg([('count','CUSTOMERID','count_customer')] , group_by = ['EXITED']).collect()

# Trainieren des Random Forest
from hana_ml.algorithms.pal.trees import *
rfc = RandomForestClassifier( n_estimators = 10,
                             max_features = 10, random_state = 2,
                            split_threshold = 0.00001,
                            categorical_variable = ['EXITED'], 
                            strata = [(0,0.5),(1,0.5)], 
                            thread_ratio = 1.0 )

g_features = ['CREDITSCORE','GEOGRAPHY','GENDER','AGE','TENURE','BALANCE','NUMOFPRODUCTS','HASCRCARD','ISACTIVEMEMBER','ESTIMATEDSALARY']

rfc.fit(data = g_df_train,
        key = 'CUSTOMERID',
        features = g_features, 
        label = 'EXITED')

rfc.model_.collect()


# ### Zusatz: Berechnen der Metriken auf Basis der Testmenge

# * Berechnet die Metriken des Modells, um diese ebenso zu speichern

# In[ ]:


# Prognosebildung mit oben trainiertem Modell rfc und Classification Report berechnen mit Testmenge

# Prognose durchführen und Verknüpfen mit IST
# Übernommen aus Ch_4_3_1_PAL_RandomFor_NN
l_df_predict_test = rfc.predict(data = g_df_test,
                                  features = g_features,
                                  key = 'CUSTOMERID')

# Verknüpfen von Prognoseergebnis und Testmenge
l_col_select = [('P.CUSTOMERID','CUSTOMERID'), ('P.SCORE','SCORE'), ('A.EXITED','EXITED')]

l_df_compare = l_df_predict_test.alias('P').join( other = g_df_test.alias('A'),
                                                  condition = 'P.CUSTOMERID = A.CUSTOMERID',
                                                  select = l_col_select)

l_df_compare = l_df_compare.cast('SCORE', 'INT').rename_columns({'SCORE': 'PREDICTED'})

# Berechnung der Konfusionsmatrix und Erfolgskennzahlen
from hana_ml.algorithms.pal.metrics import confusion_matrix

(l_df_confusion_matrix, l_df_classification_report)  = confusion_matrix( 
                                                         data = l_df_compare, 
                                                         key = 'CUSTOMERID',
                                                         label_true = 'EXITED',
                                                         label_pred = 'PREDICTED')

# Ende Übernommen aus Ch_4_3_1_PAL_RandomFor_NN


# In[ ]:


# Testausgabe der Konfusionsmatrix
l_df_confusion_matrix.collect()


# ## Speichern der Modelle

# In[ ]:


# Model Storage initialisieren und Modell speichern
from hana_ml.model_storage import ModelStorage, ModelStorageError

MODEL_SCHEMA = 'ML_MODEL' # HANA-Schema in dem die erzeugten Modelle gespeichert werden

model_storage = ModelStorage( 
    connection_context = connection,
    schema = MODEL_SCHEMA )

g_model_name_rfc = 'RandomForest CHURN'

rfc.name = g_model_name_rfc

model_storage.save_model( model = rfc, 
                         if_exists = 'upgrade' )                       

# Werte für if_exists: 
# replace: Letzte Version wird ersetzt; 
# upgrade: Neue Version wird geschrieben


# In[ ]:


# Ausgabe der gespeicherten Modelle 
model_storage.list_models()


# In[ ]:


# Einschub: Alle Tabellen im Schema ML_MODEL
connection.table('M_TABLES', schema = 'SYS').filter("SCHEMA_NAME = 'ML_MODEL'").collect()


# ### Ergänzung: Speichern der Metriken zum Modell

# Vorgehen:
# - Abrufen der neuesten Versionsnummer und Zeitstempel des letzten gespeicherten Modells (aus Tabelle HANAML_MODEL_STORAGE)
# - Anreichern des Klassifikationsreports mit den Informationen Versionsnummer und Zeitstempel.
# - Alles zusammen in der Tabelle MODEL_METRIC im Schema ML_MODEL

# In[ ]:


# Letzte Version abrufen von Modell => Timestamp und Versionsnummer übernehmen für das Speichern der Zusatzinformationen
l_df_all_model = connection.table(table = 'HANAML_MODEL_STORAGE', 
                                  schema = 'ML_MODEL').filter("NAME = 'RandomForest CHURN'")

l_df_last_model = l_df_all_model.sort('TIMESTAMP', desc = True).head(1)

l_df_last_model_info = l_df_last_model.select(['NAME','VERSION','TIMESTAMP'])
l_df_last_model_info.collect()


# In[ ]:


# Klassifikationsreport mit Informationen zu Modell verknüpfen
l_df_model_metric = l_df_last_model_info.join(l_df_classification_report, condition = '1=1')

l_df_model_metric.save( where = ('ML_MODEL','MODEL_METRIC'),
                        force = False,
                        append = True)

# Prüfen, das gespeichert wurde
connection.table('MODEL_METRIC', schema = 'ML_MODEL').collect()


# ## Laden des gespeicherten Modells

# In[ ]:


# Ein gespeichertes Modell laden
g_rfc_loaded = model_storage.load_model( name = g_model_name_rfc )
# Optionaler Parameter: version => Keine Angabe => Letzte Version nehmen
# Bestimmte Version laden: 
# rfc_loaded = model_storage.load_model(
#    name = 'RandomForest CHURN', version = 9 )


# In[ ]:


# Beispieldaten hochladen
import pandas as pd

# Pandas Dataframe mit neuen Kundendaten erstellen
l_pd_new_customer = pd.DataFrame( { 'CUSTOMERID' : [20000001,20000002],
                                  'CREDITSCORE' : [500,450], 
                                  'GEOGRAPHY' : ["Germany","France"], 
                                  'GENDER' : ["Male","Female"],
                                  'AGE' : [40,70], 
                                  'TENURE' : [8,4], 
                                  'BALANCE' : [84000.00, 72000.00],
                                  'NUMOFPRODUCTS' : [2,3], 
                                  'HASCRCARD' : [1,0],
                                  'ISACTIVEMEMBER' : [1,1], 
                                  'ESTIMATEDSALARY' : [90000.00,70000.00] 
                                }, index = [1,2] )

# In neue Tabelle NEW_CUSTOMER_PREDICT speichern für PREDICT
l_df_new_cust = dataframe.create_dataframe_from_pandas(connection_context = connection,
                                                     pandas_df = l_pd_new_customer,
                                                     table_name = 'NEW_CUSTOMER_PREDICT',
                                                     schema = 'ML_DATA',
                                                     primary_key = 'CUSTOMERID',
                                                     drop_exist_tab = True,
                                                     force = True
                                                    )
l_df_new_cust.collect()


# Einschub: Parameterkombinationen von drop_exist_tab, force:
# - force = False, drop_exist_tab = False => Anhängen an existierende Tabelle. Fehlermeldung, falls Primary Key Constraint verletzt ist
# - force = False, drop_exist_tab = True => Führt zu Fehlermeldung 'Cannot use duplicate table name'
# - force = True, drop_exist_tab = False => Leert die Tabelle mittles Drop, nur die neuen Daten bleiben erhalten
# - force = True, drop_exist_tab = True => Löscht die Tabelle mittels Truncate, nur die neuen Daten bleiben erhalten
# 
# Alternative zu create_dataframe_from_pandas: Temporäre Tabellen erstellen mit save und Eingabeparameter: table_type = LOCAL TEMPORARY COLUMN (siehe unten unter Aufräumarbeiten und Ergänzungen)

# In[ ]:


# Anwenden des geladenen Modells
l_df_new_cust_predict = g_rfc_loaded.predict( data = l_df_new_cust,
                                            key = 'CUSTOMERID')

l_df_new_cust_predict.collect()


# ## Aufräumarbeiten und Ergänzungen

# In[ ]:


# Modelle zu Random Forest löschen
# model_storage.delete_models(g_model_name_rfc)


# In[ ]:


# Datentypen auslesen
connection.table(table = 'NEW_CUSTOMER_PREDICT', schema = 'ML_DATA').dtypes()


# In[ ]:


# Tabellen NEW_CUSTOMER_PREDICT und MODEL_METRIC löschen
# connection.drop_table('NEW_CUSTOMER_PREDICT', schema = 'ML_DATA')
# connection.drop_table('MODEL_METRIC', schema = 'ML_MODEL')


# In[ ]:


# Zusatz: Leere Tabelle aus Vorlage CHURN anlegen - Typ LOCAL TEMPORARY COLUMN
# connection.table('CHURN', schema = 'ML_DATA').dtypes()
df_churn_hull = connection.table('CHURN', schema = 'ML_DATA').filter('1 <> 1')

df_churn_hull_2 = df_churn_hull.drop(['ROWNUMBER','SURNAME','EXITED'])

df_churn_hull_2.save(where = ('ML_DATA','NEW_CUSTOMER_PREDICT'),
                     table_type = 'LOCAL TEMPORARY COLUMN' )


# In[ ]:


df_churn_hull_2.dtypes()


# In[ ]:




