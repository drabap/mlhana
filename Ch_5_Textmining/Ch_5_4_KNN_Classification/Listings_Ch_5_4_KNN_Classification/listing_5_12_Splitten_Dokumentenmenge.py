# Splitten der Dokumentenmenge

# Referenzdokumente => die ersten 1000 Dokumente
df_reference = df_input_knn.filter('ID <= 1000')
# l_df_train.describe().collect()

# Testdokumente => Zufällig 250 mit ID > 1000
df_test = df_input_knn.filter('ID > 1000').head(250)

# Zielvariable CATEGORY entfernen
df_input_test = df_test.drop('CATEGORY')
df_input_test.collect()