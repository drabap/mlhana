# Trainingsmenge mit ausgewogener Klassenverteilung
l_df_train_0 = g_df_churn.filter("EXITED = 0").head(1000)
l_df_train_1 = g_df_churn.filter("EXITED = 1").head(1000)

l_df_id_train = l_df_train_0.union(
    l_df_train_1).select([('CUSTOMERID','ID')])

l_df_id_train_mark = l_df_id_train.select(
    '*',('1','MARKER_TRAIN'))

# Left outer JOIN auf Grundgesamtheit
l_df_id_split = g_df_churn.alias("T").join(
    other = l_df_id_train_mark.alias('A'),
    condition = 'T.CUSTOMERID = A.ID',
    how = 'outer')

# Berechnete Spalte mit coalesce (MARKER_TRAIN, 0) 
# => nur 1 bei Kunden in Trainingsmenge
l_df_churn_split = l_df_id_split.select('*',
    ('COALESCE(MARKER_TRAIN,0)','TRAIN_SET')
    )

g_df_train_nn = l_df_churn_split.filter(
    "TRAIN_SET = 1")

g_df_test_nn = l_df_churn_split.filter(
    "TRAIN_SET = 0")

# Zählen der Kündigenden in Training- und Test
g_df_train_nn.agg([('count','EXITED','COUNT')],
    group_by = ['EXITED']).collect()
