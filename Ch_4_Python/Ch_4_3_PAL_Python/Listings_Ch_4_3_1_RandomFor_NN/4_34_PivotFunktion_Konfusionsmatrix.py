# Pivot-Funktionen für die Konfusionsmatrix
df_confusion_matrix.pivot_table(index = 'EXITED',
    columns = 'PREDICTED',
    values = 'COUNT').collect()

