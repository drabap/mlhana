#!/usr/bin/env python
# coding: utf-8

# # 4.3 Random Forests und neuronale Netze trainieren

# - Random Forest trainieren
# -- Aufteilen der Grunddaten in Trainings- und Testdaten
# -- Trainieren eines Random Forest
# -- Evaluieren des Modells auf der Testmenge
# - Neuronales Netz trainieren
# -- Aufteilen der Grunddaten in Trainings- und Testdaten
# -- Trainieren und Evaluieren des neuronalen Netzes
# -- Hyperparameter optimieren
# 

# In[1]:


# Verbindung zur HANA
from hana_ml import dataframe

connection = dataframe.ConnectionContext( KEY = 'DEV' )

# CHURN laden
g_df_churn = connection.table('CHURN',
                                   schema = 'ML_DATA')

g_df_churn.head(20).collect()


# # Random Forest trainieren

# ## Aufteilen in Grund- und Testdaten

# In[2]:


#  Daten partitionieren
from hana_ml.algorithms.pal import partition

g_df_train, g_df_test, g_df_valid = partition.train_test_val_split( 
                                                    data = g_df_churn,
                                                    id_column = 'CUSTOMERID', 
                                                    partition_method = 'stratified',
                                                    training_percentage = 0.6, 
                                                    validation_percentage = 0.0,
                                                    testing_percentage = 0.4,
                                                    stratified_column = 'EXITED' 
   )

# Anteil Kündigungen je nach Referenzmenge zählen
# Gesamtmenge
g_df_churn.agg([('count','CUSTOMERID','count_customer')] ,
               group_by = ['EXITED']).collect()

# Trainingsdaten
# g_df_train.agg([('count','CUSTOMERID','count_customer')], 
#          group_by = ['EXITED']).collect()

# Testdaten
# g_df_test.agg([('count','CUSTOMERID','count_customer')] , group_by = ['EXITED']).collect()


# ## Trainieren des Random Forest

# In[3]:


# Trainieren des Random Forest
from hana_ml.algorithms.pal.trees import *
rfc = RDTClassifier( 
                             n_estimators = 10,
                             max_features = 10, random_state = 2,
                            split_threshold = 0.00001,
                            categorical_variable = ['EXITED'], 
                            strata = [(0,0.5),(1,0.5)], 
                            thread_ratio = 1.0 
                    )

l_features = ['CREDITSCORE','GEOGRAPHY','GENDER','AGE',
              'TENURE','BALANCE','NUMOFPRODUCTS',
              'HASCRCARD','ISACTIVEMEMBER','ESTIMATEDSALARY']

rfc.fit(data = g_df_train,
        key = 'CUSTOMERID',
        features = l_features, 
        label = 'EXITED')

# rfc.model_.collect()


# In[4]:


# Zusatz: Instanzattribute nach Training
# rfc.model_.collect()

# rfc.feature_importances_.collect()

# rfc.oob_error_.collect()

rfc.confusion_matrix_.collect()


# ## Modell anwenden auf Testmenge und Konfusionsmatrix berechnen

# In[5]:


# Predict anwenden auf Testmenge
l_features = ['CREDITSCORE','GEOGRAPHY','GENDER','AGE',
                  'TENURE','BALANCE','NUMOFPRODUCTS',
                  'HASCRCARD','ISACTIVEMEMBER','ESTIMATEDSALARY']

g_df_predict_test = rfc.predict( data = g_df_test,
                                 key = 'CUSTOMERID',
                                 features = l_features )

g_df_predict_test.collect()


# In[6]:


# Korrektklassifikationsrate berechnen (engl.: Accuracy Score)
rfc.score( data = g_df_test,
           key = 'CUSTOMERID',
           features = l_features)


# In[7]:


# Verknüpfen von Prognoseergebnis und Testmenge
col_select = [('P.CUSTOMERID','CUSTOMERID'), 
              ('P.SCORE','SCORE'), 
              ('A.EXITED','EXITED')]

l_df_compare = g_df_predict_test.alias('P').join(
                                          other = g_df_test.alias('A'),
                                          condition = 'P.CUSTOMERID = A.CUSTOMERID',
                                          select = col_select)

l_df_compare = l_df_compare.cast('SCORE', 
                             'INT').rename_columns({'SCORE': 'PREDICTED'})

l_df_compare.head(20).collect()


# In[8]:


# Einschub: Aggregieren auf Spalte EXITED, SCORE => gleiches Ergebnis wie Konfusionsmatrix
l_df_agg = l_df_compare.agg([('count','CUSTOMERID','COUNT')], group_by = ['EXITED','PREDICTED'])

l_df_agg.collect()


# In[9]:


# Berechnung der Konfusionsmatrix und Erfolgskennzahlen
from hana_ml.algorithms.pal.metrics import confusion_matrix

(df_confusion_matrix, df_class_report) = confusion_matrix(
                                       data = l_df_compare, 
                                       key = 'CUSTOMERID',
                                       label_true = 'EXITED',
                                       label_pred = 'PREDICTED')

df_confusion_matrix.collect()


# In[10]:


# Zusatz: Gütekriterien ermittelt mit der Testmenge
df_class_report.collect()


# In[11]:


# Pivot-Funktion für die Konfusionsmatrix
# Zeile: Korrekte Klasse (actual class)
# Spalte: Vorhergesagte Klasse (predicted class), wie in Geron p. 91
# index = EXITED => bleibt in Zeile => Zeile entspricht tatsächlichem Wert
# columns = PREDICTED => wird zu Spalte => Spalte entspricht Vorhersage aus Spalte PREDICTED
df_confusion_matrix.pivot_table(index = 'EXITED',
                             columns = 'PREDICTED',
                             values = 'COUNT').collect()


# ## Einfluss der Features untersuchen

# In[12]:


# Relevanz der Variablen für die Prognose ausgeben
df_feature_importance = rfc.feature_importances_.sort(
    'IMPORTANCE',desc = True)

df_feature_importance.collect()


# In[13]:


# Plotten der Variablenwichtigkeit
from hana_ml.visualizers.eda import EDAVisualizer
import matplotlib.pyplot as plt

fig_barplot = plt.figure(figsize = (18,6))
ax1 = fig_barplot.add_subplot(121)
eda = EDAVisualizer(ax1)

ax1, bar_data = eda.bar_plot(
    data = df_feature_importance,
    column = 'VARIABLE_NAME',
    aggregation = {'IMPORTANCE':'avg'})


# # Neuronale Netze trainieren

# ## Trainingsmenge mit ausgewogener Klassenverteilung erstellen

# In[14]:


# Trainingsmenge mit ausgewogener Klassenverteilung

l_df_train_0 = g_df_churn.filter('EXITED = 0').head(1000)
l_df_train_1 = g_df_churn.filter('EXITED = 1').head(1000)

l_df_id_train = l_df_train_0.union(
    l_df_train_1).select([('CUSTOMERID','ID')])

l_df_id_train_mark = l_df_id_train.select(
    '*',('1','MARKER_TRAIN'))

# Left outer JOIN auf Grundgesamtheit
l_df_id_split = g_df_churn.alias('CH').join(
                                             other = l_df_id_train_mark.alias('TM'),
                                             condition = 'CH.CUSTOMERID = TM.ID',
                                             how = 'outer' )

# Berechnete Spalte mit coalesce (MARKER_TRAIN, 0): 
#   => Flag 1 bei Sätzen, die in Trainingsmenge l_df_id_train_mark sind
#   => Flag 0 bei Sätzen ohne JOIN-Partner, also alle, die nicht in l_df_id_train_mark sind
l_df_churn_split = l_df_id_split.select('*',
                                        ('COALESCE(MARKER_TRAIN,0)','TRAIN_SET')
                                        )

g_df_train_nn = l_df_churn_split.filter("TRAIN_SET = 1")

g_df_test_nn = l_df_churn_split.filter("TRAIN_SET = 0")

# Zählen der Kündigenden in Training- und Testmenge
g_df_train_nn.agg([('count','EXITED','COUNT')],
                  group_by = ['EXITED']).collect()
#test_nn.agg([('count','EXITED','COUNT')],group_by = ['EXITED']).collect()


# ## Training des neuronalen Netzes

# In[15]:


# Das neuronale Netz trainieren
from hana_ml.algorithms.pal.neural_network import *

mlp_c = MLPClassifier( hidden_layer_size = (30,15,10,5),
                      activation = 'sigmoid_symmetric', 
                      output_activation = 'sigmoid_symmetric',
                      training_style = 'batch',
                      max_iter = 1000,
                      normalization = 'z-transform',
                      weight_init = 'normal',
                      thread_ratio = 0.3, 
                      categorical_variable = ['EXITED',
                                            'HASCRCARD',
                                            'ISACTIVEMEMBER']
                     )

l_features = ['CREDITSCORE','GEOGRAPHY','GENDER','AGE',
                  'TENURE','BALANCE','NUMOFPRODUCTS',
                  'HASCRCARD','ISACTIVEMEMBER','ESTIMATEDSALARY']



mlp_c.fit(data = g_df_train_nn,
         key = 'CUSTOMERID',
         features = l_features,
         label = 'EXITED' )        


# In[16]:


# Einschub: Das fertige Modell
mlp_c.model_.collect()


# ## Anwenden des Modells auf die Testdaten und Berechnung der Konfusionsmatrix

# In[17]:


# Anwenden des neuronalen Netzes auf die Testdaten
g_df_mlp_prediction, test_stat = mlp_c.predict(
                                          data = g_df_test_nn,
                                          key = 'CUSTOMERID',
                                          features = l_features 
                                         )

g_df_mlp_prediction.collect()
# mlp_prediction.agg([('count','CUSTOMERID','count_customer')] , group_by = ['TARGET']).collect()


# In[18]:


# Konfusionsmatrix für das neuronale Netz
# Verknüpfen von Prognoseergebnis und Testmenge
col_select = [('P.CUSTOMERID','CUSTOMERID'), 
              ('P.TARGET','TARGET'),
              ('A.EXITED','EXITED')]

l_df_compare_mlp = g_df_mlp_prediction.alias('P').join(
                                          other = g_df_test_nn.alias('A'),
                                          condition = 'P.CUSTOMERID = A.CUSTOMERID',
                                          select = col_select)

l_df_compare_mlp = l_df_compare_mlp.cast('TARGET', 'INT')
l_df_compare_mlp = l_df_compare_mlp.rename_columns(
    {'TARGET': 'PREDICTED'})

# Berechnung der Konfusionsmatrix und Erfolgskennzahlen
from hana_ml.algorithms.pal.metrics import confusion_matrix

(df_conf_matrix_nn, df_class_rep_nn)  = confusion_matrix( 
                                       data = l_df_compare_mlp, 
                                       key = 'CUSTOMERID',
                                       label_true = 'EXITED',
                                       label_pred = 'PREDICTED')

df_conf_matrix_nn.collect()


# In[19]:


df_class_rep_nn.collect()


# ## Hyperparameter optimieren bei neuronalen Netzen

# In[20]:


# Voraussetzung: Verbindung zur HANA steht
# Splitting in Trainingsmenge und Testmenge wurde durchgeführt
# Variable g_df_train_nn und g_df_test_nn sind gefüllt
g_df_train_nn.collect()


# ### Trainieren mit Optimierung der Hyperparameter

# In[21]:


# Training mit Optimierung der Hyperparameter
from hana_ml.algorithms.pal.neural_network import *

# Mögliche Werte für Netztopologie
hidden_layer_opt = [(30,20,10,5),(10,10,5,5),(30,20,10),(10,5)]

# act_opts = ['tanh', 'sigmoid_symmetric']
# act_out_opts = ['tanh', 'sigmoid_symmetric']


mlp_c_opt = MLPClassifier( 
                      # hidden_layer_size = (10,10,5,5),
                      hidden_layer_size_options = hidden_layer_opt,
                      activation = 'sigmoid_symmetric',
                      #activation_options = act_opts, 
                      output_activation = 'sigmoid_symmetric',
                      #output_activation_options = act_out_opts,
                      training_style = 'batch', # oder batch
                      max_iter = 1000,
                      normalization = 'z-transform',
                      weight_init = 'normal',
                      thread_ratio = 0.3, 
                      categorical_variable = ['EXITED',
                                            'HASCRCARD',
                                            'ISACTIVEMEMBER'],
                      resampling_method = 'cv', # oder stratified_cv, bootstrap, stratified_bootstrap
                      fold_num = 4,
                      evaluation_metric = 'f1_score', # oder accuracy, auc_onevsrest, auc_pairwise
                      search_strategy = 'grid',
                      progress_indicator_id = 'TEST'    
                     )

l_features = ['CREDITSCORE','GEOGRAPHY','GENDER','AGE',
                  'TENURE','BALANCE','NUMOFPRODUCTS',
                  'HASCRCARD','ISACTIVEMEMBER','ESTIMATEDSALARY']



mlp_c_opt.fit( data = g_df_train_nn,
         key = 'CUSTOMERID',
         features = l_features,
         label = 'EXITED' )        


# In[23]:


# Zusatz: Ausgabe der Statistiken zur Parameteroptimierung
mlp_c_opt.stats_.collect()


# In[25]:


# Beste Wahl der Hyperparameter ausgeben
mlp_c_opt.optim_param_.collect()


# In[24]:


# Zusatz: Log des Trainings ausgeben
mlp_c_opt.train_log_.collect()


# ### Zusatz: Anwenden des Modells mit optimierten Hyperparameter auf die Testdaten

# In[25]:


# Anwenden des neuronalen Netzes mit den optimierten Hyperparametern auf die Testdaten
g_mlp_opt_pred, test_stat = mlp_c_opt.predict(
                                          data = g_df_test_nn,
                                          key = 'CUSTOMERID',
                                          features = l_features 
                                         )


# mlp_prediction.agg([('count','CUSTOMERID','count_customer')] , group_by = ['TARGET']).collect()
# Konfusionsmatrix für das neuronale Netz
# Verknüpfen von Prognoseergebnis und Testmenge
col_select = [('P.CUSTOMERID','CUSTOMERID'), 
              ('P.TARGET','TARGET'),
              ('A.EXITED','EXITED')]

l_df_compare_mlp_opt = g_mlp_opt_pred.alias('P').join(
                                          other = g_df_test_nn.alias('A'),
                                          condition = 'P.CUSTOMERID = A.CUSTOMERID',
                                          select = col_select)

l_df_compare_mlp_opt = l_df_compare_mlp_opt.cast('TARGET', 'INT')
l_df_compare_mlp_opt = l_df_compare_mlp_opt.rename_columns(
    {'TARGET': 'PREDICTED'})

# Berechnung der Konfusionsmatrix und Erfolgskennzahlen
from hana_ml.algorithms.pal.metrics import confusion_matrix

(df_conf_matrix_mlp_opt, df_class_rep_mlp_opt)  = confusion_matrix( 
                                       data = l_df_compare_mlp_opt, 
                                       key = 'CUSTOMERID',
                                       label_true = 'EXITED',
                                       label_pred = 'PREDICTED')

df_conf_matrix_mlp_opt.collect()


# In[26]:


df_class_rep_mlp_opt.collect()


# In[27]:


connection.close()

