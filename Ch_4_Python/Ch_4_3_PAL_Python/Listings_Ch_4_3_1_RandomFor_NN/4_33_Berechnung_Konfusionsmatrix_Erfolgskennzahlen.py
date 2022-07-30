# Berechnung der Konfusionsmatrix und Erfolgskennzahlen
from hana_ml.algorithms.pal.metrics import confusion_matrix

(df_confusion_matrix, df_class_report) = confusion_matrix(
    data = l_df_compare,
    key = 'CUSTOMERID',
    label_true = 'EXITED',
    label_pred = 'PREDICTED')

df_confusion_matrix.collect()
