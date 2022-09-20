#!/usr/bin/env python
# coding: utf-8

# Kapitel 4, Abschnitt 4.2.1 - Datenvisualisierung im Jupyter Notebook
# - Verwendung des EDA-Visualisiers
# 
# Klasse hana_ml.visualizer.eda.EDAVisualizer
# 
# Diagramm-Arten:
# - Distribution/ Histogramm => Histogramm einer numerischen Variable
# - Pie Plot: Kuchendiagramm für kategoriale Verteilung
# - Bar Plot: Balkendiagramm einer Spalte
# 
# - Scatter Plot: Gemeinsame Verteilung zweier Variablen
# - Correlation Plot: Korrelation zwischen numerischen Variablen
# - Box plot: Mittelwert und Quantile einer Variable beschreiben
# 
# - DataserReportBuilder: Übersicht über verschiedene Informationen und Diagramme zu den Variablen
# 
# 
# 

# In[1]:


# Initialisierung zu Beginn des Jupyer-Notebooks

# Python-Bibliotheken importieren und zu HANA verbinden
from hana_ml import dataframe
from hana_ml.visualizers.eda import EDAVisualizer
import matplotlib.pyplot as plt

connection = dataframe.ConnectionContext(KEY = 'DEV')

# CHURN laden
g_df_churn = connection.table('CHURN', schema = 'ML_DATA')
# IRIS laden
g_df_iris = connection.table('IRIS', schema = 'ML_DATA')


# In[2]:


# Histogramm für die Variable AGE

fig = plt.figure(figsize = (18,6))

ax1 = fig.add_subplot(121)
eda = EDAVisualizer(ax1)

ax1, dist_data = eda.distribution_plot(
                                       data = g_df_churn, 
                                       column = 'AGE',
                                       bins = 10,
                                       title = 'Verteilung des Alters aller Kunden')


# In[3]:


# Zusatz: Histogramm für Balance

fig = plt.figure(figsize = (18,6))

ax1 = fig.add_subplot(121)
eda = EDAVisualizer(ax1)

ax1, dist_data = eda.distribution_plot(data = g_df_churn, 
                                       column = 'BALANCE',
                                       bins = 10,
                                       title = 'Verteilung des Kontosaldo aller Kunden')

# Beobachtung: Viele mit 0 => in der Praxis müsste man nun untersuchen,
# ob diese Wert korrekt sind oder in den Rohdaten der Wert fehlt 


# In[4]:


# Bar Plot: Kunden nach Produkt
fig_barplot = plt.figure(figsize = (18,6))


ax1 = fig_barplot.add_subplot(121)
eda = EDAVisualizer(ax1)

ax1, bar_data = eda.bar_plot(data = g_df_churn, 
                             column = 'NUMOFPRODUCTS',
                             aggregation = {'CUSTOMERID':'count'})


# In[5]:


# Zusatz: Bar Plot: Durchschnittliche BALANCE nach Produkt
fig_barplot = plt.figure(figsize = (18,6))


ax1 = fig_barplot.add_subplot(121)
eda = EDAVisualizer(ax1)

ax1, bar_data = eda.bar_plot(data = g_df_churn, 
                             column = 'NUMOFPRODUCTS',
                             aggregation = {'BALANCE':'avg'})


# In[6]:


# Anteil der Kunden nach Land

fig_pieplot = plt.figure(figsize = (18,6))

ax1 = fig_pieplot.add_subplot(121)
eda = EDAVisualizer(ax1)

ax1, pie_data = eda.pie_plot(data = g_df_churn, 
                             explode = 0.03,
                             column = 'GEOGRAPHY')


# In[7]:


# Kreisdiagramm: Anteil Kündigungen in zwei Altersgruppen

df_age_below_50 = g_df_churn.filter('AGE <= 50')
df_age_above_50 = g_df_churn.filter('AGE > 50')

fig_churn_by_age = plt.figure(figsize = (18,6))
ax1 = fig_churn_by_age.add_subplot(121)
eda = EDAVisualizer(ax1)

ax1, pie_data = eda.pie_plot(data = df_age_below_50, 
                             column = 'EXITED', 
                             title = "Churn for Age <= 50")

ax2 = fig_churn_by_age.add_subplot(122)
eda2 = EDAVisualizer(ax2)
ax2, pie_data2 = eda2.pie_plot(data = df_age_above_50, 
                               column = 'EXITED',
                               title = "Churn for Age > 50")


# In[8]:


# Streudiagramm mit Iris-Daten
# Plottet SEPAL_WIDTH vs. SEPAL_LENGTH

fig_scatter_iris = plt.figure(figsize=(18,6))

ax1 = fig_scatter_iris.add_subplot(121)
eda = EDAVisualizer(ax1)

# Color maps:
# Greys: Graustufen
# Reds, Blues

ax1, scatter_data = eda.scatter_plot(data = g_df_iris, 
                                  x = 'SEPAL_WIDTH', 
                                  y = 'SEPAL_LENGTH', 
                                  x_bins = 4, y_bins = 4,
                                  debrief = True, 
                                  cmap = 'Blues')


# In[3]:


# Einschub: Binning manuell machen und zählen
# Mismatch zu Scatter plot => Quellcode prüfen => anscheinend andere Strategie
l_df_iris_bin = g_df_iris.bin(col = 'SEPAL_WIDTH', 
                              strategy = 'uniform_number', 
                              bins = 4, bin_column = 'SEPAL_WIDTH_BIN')

l_df_iris_bin_2 = l_df_iris_bin.bin(col = 'SEPAL_LENGTH',
                                    strategy = 'uniform_number',
                                    bins = 4, bin_column = 'SEPAL_LENGTH_BIN')

l_list_agg = [('count','PLANTID','COUNT_PLANT'),
              ('min','SEPAL_WIDTH','SEPAL_WIDTH_MIN'),
              ('max','SEPAL_WIDTH','SEPAL_WIDTH_MAX')]

l_df_iris_agg = l_df_iris_bin_2.agg(l_list_agg,
                                    group_by = ['SEPAL_WIDTH_BIN','SEPAL_LENGTH_BIN'])
l_df_iris_agg.sort(['SEPAL_WIDTH_BIN','SEPAL_LENGTH_BIN']).collect()

#dataframe_iris.describe().collect()


# In[9]:


# Korrelation berechnen

fig_correlation_iris = plt.figure(figsize=(18,6))

ax1 = fig_correlation_iris.add_subplot(121)
eda = EDAVisualizer(ax1)

ax1, scatter_data = eda.correlation_plot(
                                  data = g_df_iris, 
                                  corr_cols = ['SEPAL_LENGTH','SEPAL_WIDTH',
                                               'PETAL_LENGTH','PETAL_WIDTH'],
                                  cmap = 'Reds')


# In[10]:


# Tipp: Direkte Berechnung Korrelation mit Dataframe
g_df_iris.corr('SEPAL_LENGTH','SEPAL_WIDTH').collect()


# In[11]:


# Boxplot für die Variable BALANCE
# Variation: Gruppieren nach Spalte, z.B. GEOGRAPHY

f = plt.figure(figsize=(18,6))

ax1 = f.add_subplot(121)
eda = EDAVisualizer(ax1)

l_df_bal = g_df_churn.filter("BALANCE > 0")
ax, bar_data = eda.box_plot(data = l_df_bal,
                            column = 'BALANCE',
                            #groupby = 'GEOGRAPHY',
                            outliers = True)
                                                 


# In[12]:


# Ergänzung:
# Boxplot: SEPAL_LENGTH nach Art (SPECIES)
# outliers = true => Ausreißer darstellen

f = plt.figure(figsize=(18,6))

ax1 = f.add_subplot(121)
eda = EDAVisualizer(ax1)

ax, bar_data = eda.box_plot(data = g_df_iris, column='SEPAL_LENGTH', 
                                                 groupby = 'SPECIES', outliers = True)


# In[13]:


# Ergänzung: Statistische Kennzahlen für Boxplot ermitteln
list_cols_proj = ['column','median',
                  'min','max',
                  '25_percent_cont',
                  '75_percent_cont']

l_df_bal = g_df_churn.filter("BALANCE > 0")
l_df_bal = l_df_bal.select("BALANCE")

l_df_bal.describe().select(list_cols_proj).collect()


# Bedeutung (gem. https://de.wikipedia.org/wiki/Box-Plot)

# Gestrichelte Linie: Median => 50% der Werte darunter, 50% darüber
# Blaue Box: Mittlere 50% der Werte => die kleinsten 25% sind links der Box, 75% der Werte sind links vom rechten Rand der Box
#  linker Rand der blauen Box = 25_percent_cont (unteres Quartil). Hier: 100.000
# rechter Rand der blauen Box = 75_percent_cont (oberes Quartil).  Hier: 140.000
# IQR: Inter-Quartils-Abstand ( 75_percent_cont - 25_percent_cont ): 40.000

# Whisker-Antenne: 
# Suspected Outlier fence: unteres Quartil - 1.5*IQR = 100.000 - 1.5 * 40.000 = 40.000
# Suspected Outlier fence: oberes Quartil + 1.5*IQR = 140.000 + 1.5*40.000 = 200.000
# Außerhalb Suspected aber innerhalb Outlier fence: milde Ausreißer
# Außerhalb von 3 Quartil (Outlier fence) => extreme Ausreißer


# In[14]:


# Dataset Report erstellen für Tabelle CHURN
from hana_ml.visualizers.dataset_report import DatasetReportBuilder

datasetReportBuilder = DatasetReportBuilder()
datasetReportBuilder.build( g_df_churn, key = 'CUSTOMERID')
datasetReportBuilder.generate_notebook_iframe_report()


# In[15]:


# Ergänzung: Dataset Report erstellen für Tabelle IRIS
from hana_ml.visualizers.dataset_report import DatasetReportBuilder

datasetReportBuilder = DatasetReportBuilder()
datasetReportBuilder.build(g_df_iris, key = 'PLANTID')
datasetReportBuilder.generate_notebook_iframe_report()


# In[4]:


# Verbindung schließen
connection.close()


# In[ ]:




