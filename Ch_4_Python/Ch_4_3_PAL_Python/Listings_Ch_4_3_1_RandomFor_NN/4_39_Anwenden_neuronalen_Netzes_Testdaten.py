# Anwenden des neuronalen Netzes auf die Testdaten
g_df_mlp_prediction, test_stat = mlp_c.predict(
    data = g_df_test_nn,
    key = 'CUSTOMERID',
    features = l_features
    )

g_df_mlp_prediction.collect()

