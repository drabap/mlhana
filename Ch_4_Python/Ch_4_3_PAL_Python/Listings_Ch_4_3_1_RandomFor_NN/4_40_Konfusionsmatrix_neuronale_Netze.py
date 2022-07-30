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

(df_conf_matrix_nn, df_class_rep_nn) = confusion_matrix(
    data = l_df_compare_mlp,
    key = 'CUSTOMERID',
    label_true = 'EXITED',
    label_pred = 'PREDICTED')

df_conf_matrix_nn.collect()

