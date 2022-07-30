# Anwenden des geladenen Modells
l_df_new_cust_predict = g_rfc_loaded.predict(
    data = l_df_new_cust,
    key = 'CUSTOMERID')

l_df_new_cust_predict.collect()
