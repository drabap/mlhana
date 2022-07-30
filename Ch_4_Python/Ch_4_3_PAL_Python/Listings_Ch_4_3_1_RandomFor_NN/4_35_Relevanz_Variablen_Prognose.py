# Relevanz der Variablen für die Prognose ausgeben
df_feature_importance = rfc.feature_importances_.sort(
   'IMPORTANCE', desc=True)

df_feature_importance.collect()
