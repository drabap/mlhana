#!/usr/bin/env python
# coding: utf-8

# # Kapitel 4, Abschnitt 4.2.2 - Visualisieren mit Python-Bibliotheken

# - Pandas Dataframe => Scatter Plot von IRIS
# - Plotly => Multivariate Diagramme und Facet Plot bei CHURN
# 
# - HANA-Tabellen:
# -- IRIS
# -- CHURN

# # Matplotlib - Streudiagramm

# In[1]:


# Initialisierung zu Beginn des Jupyter-Notebooks (Wiederholung Listing 4.12)

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


# Streudiagramm von IRIS mit Pandas
# X,Y : Länge/Breite
# Farbe: Kategorie (Spalte SPECIES)

# HANA Dataframe nach Pandas dataframe
pd_iris = g_df_iris.collect()

# Kategoriale Kodierung von SPECIES => Zur Färbung der Punkte nehmen
# Quelle: https://pbpython.com/categorical-encoding.html

pd_iris['SPECIES'] = pd_iris['SPECIES'].astype('category')
pd_iris['SPECIES_CAT'] = pd_iris['SPECIES'].cat.codes

# Scatter Plot
pd_iris.plot(kind = 'scatter',  
             x = 'SEPAL_LENGTH',
             y = 'PETAL_WIDTH',
             c = 'SPECIES_CAT',
             cmap = 'coolwarm')


# # Plotly - Facet plot

# In[3]:


# Vorbereitung der Visualisierung: Aggregation in der HANA

# Aggregation: Anzahl der Kündigenden nach Anzahl Produkte
group_by_col = ['NUMOFPRODUCTS','EXITED']

l_df_agg = g_df_churn.agg(
                               [('count',
                                 'CUSTOMERID',
                                 'COUNT_CUSTOMER')
                               ],
                               group_by = group_by_col)

l_exp_label = """CASE EXITED WHEN 1 THEN 'EXITED'
 ELSE 'NOT EXITED' END"""

l_df_w_text = l_df_agg.select('*',
                              (l_exp_label, 'EXIT_LABEL')
                             )

# Umwandeln in Pandas Dataframe
l_pd_df = l_df_w_text.sort(group_by_col).collect()
# Zum Testen: Ausgeben des Pandas Dataframe
print(l_pd_df)


# ## Stacked Barchart mit einer Dimension

# In[4]:


# Balkendiagramm mit Dimension Anzahl Produkte

import plotly.express as px

fig = px.bar(data_frame = l_pd_df,
             x = 'NUMOFPRODUCTS', 
             y = 'COUNT_CUSTOMER', 
             color = 'EXIT_LABEL', 
             color_discrete_sequence = px.colors.qualitative.D3
             )



fig.show()

# Für JupyterLab muss eine Erweiterung installiert werden:
# In Kommandozeile der Python-Umgebung:
# jupyter labextension install jupyterlab-plotly

# Workaround JupyterLab: Export als iframe:
#fig.show( renderer = 'iframe' )



# ## Facet Plot mit zwei Dimensionen

# In[6]:


# Plotly: Barchart mit zwei Dimensionen
# Anteil der Kündigenden nach Land und Anzahl Produkte

import plotly.express as px

group_by_col_ext = ['GEOGRAPHY','NUMOFPRODUCTS','EXITED']

l_df_agg_ext = g_df_churn.agg([('count',
                                'CUSTOMERID',
                                'COUNT_CUSTOMER')
                              ],
                              group_by = group_by_col_ext)


l_exp_label = """CASE EXITED WHEN 1 THEN 'EXITED'
 ELSE 'NOT EXITED' END"""

l_df_text_ext = l_df_agg_ext.select('*',
                                    (l_exp_label, 'EXIT_LABEL')
                                   )

# Umwandeln in Pandas Dataframe
l_pd_df_ext = l_df_text_ext.sort(group_by_col_ext).collect()

# Zum Testen: Ausgeben des Pandas Dataframe
#print(l_pd_df_ext)

# Zeichnen

fig = px.bar(l_pd_df_ext, 
             x = 'NUMOFPRODUCTS', 
             y = 'COUNT_CUSTOMER', 
             color = 'EXIT_LABEL', 
             facet_row = 'GEOGRAPHY',
             #barmode = 'group', # Klassen nebeneinander anzeigen
             facet_row_spacing = 0.07,
             labels = {'COUNT_CUSTOMER' : 'Kunden', 
                       'EXIT_LABEL' : 'Kündigung'},
             color_discrete_sequence = px.colors.qualitative.D3)

# Optional: "Compare data on hover" aktivieren
# fig.update_layout(hovermode = 'x')

fig.show( )


# In[6]:


# Verbindung schließen
connection.close()


# ## Zusatz

# In[7]:


# Beispiele für mögliche Farbschemata in Plotly
import plotly.express as px
px.colors.qualitative.swatches()


# In[7]:


# Zusatz: Andere Plot-Typen mit Pandas
# KDE-Plot von IRIS mit Pandas
# Y : Spalte, deren Dichte geschätzt werden soll


# HANA Dataframe nach Pandas dataframe
l_pd_frame = g_df_iris.collect()

# Testausgabe bei Bedarf
# print(l_pd_frame)


# KDE plot

l_pd_frame.plot( kind = "kde", 
                # x = "SEPAL_LENGTH", Bei kind = kde nur eine Dimension angeben
                 y = "PETAL_LENGTH"
                 #c = "SPECIES_CAT", 
                 #cmap = 'coolwarm' 
               )


# In[6]:


# Zusatz: Andere Plot-Typen mit Pandas
# KDE-Plot von CHURN mit Pandas
# Y : Spalte, deren Dichte geschätzt werden soll


# HANA Dataframe nach Pandas-Dataframe
l_pd_frame = g_df_churn.filter('BALANCE > 0').collect()

# Bei Bedarf Testausgabe
# print(l_pd_frame)

# KDE plot

l_pd_frame.plot( kind = "kde", 
                 y = "BALANCE"
                 #cmap = 'coolwarm' 
               )


# ### Workaround Plotly bei Jupyterlab

# In[6]:


# In Jupyterlab werden interaktive Diagramme wie bei Plotly 
# nicht angezeigt.
# Als Workaround kann man beim Befehl fig.show das Argument renderer = "iframe" einfügen

# Test von Plotly gemäß 
# https://stackoverflow.com/questions/63449330/plotly-graphs-dont-render-on-jupyterlab-installed-with-zero-to-jupyterhub-gke
import plotly.graph_objects as go

fig = go.Figure(data=go.Bar(y=[2, 3, 1]))

fig.show(renderer = "iframe")


# In[ ]:




