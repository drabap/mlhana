# Initialisierung zu Beginn des Jupyter Notebook
# Python-Bibliotheken importieren und zu HANA verbinden
from hana_ml import dataframe
from hana_ml.visualizers.eda import EDAVisualizer
import matplotlib.pyplot as plt

connection = dataframe.ConnectionContext( KEY = 'DEV')

# CHURN laden
g_df_churn = connection.table('CHURN', schema = 'ML_DATA')
# IRIS laden
g_df_iris = connection.table('IRIS', schema = 'ML_DATA')
