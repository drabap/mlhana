# Verbindung zur HANA
from hana_ml import dataframe

connection = dataframe.ConnectionContext(KEY = 'DEV')

# CHURN laden
g_df_churn = connection.table('CHURN',
    schema = 'ML_DATA')

g_df_churn.head(20).collect()
