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

# Kündigungen nach Partition zählen
g_df_train.agg([('count','CUSTOMERID','count_customer')],
    group_by = ['EXITED']).collect()
