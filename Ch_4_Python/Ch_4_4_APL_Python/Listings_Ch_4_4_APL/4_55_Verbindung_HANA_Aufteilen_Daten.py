# Verbindung zur HANA und Aufteilen der Daten
from hana_ml import dataframe
from hana_ml.algorithms.pal import partition

connection = dataframe.ConnectionContext(KEY = 'DEV')

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
