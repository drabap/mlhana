# Statistische Kennzahlen für Box-Plot ermitteln
list_cols_proj = ['column','median',
    'min','max',
    '25_percent_cont',
    '75_percent_cont']

df_bal = g_df_churn.filter("BALANCE > 0")
df_bal = df_bal.select("BALANCE")

df_bal.describe().select(list_cols_proj).collect()
