# Predict anwenden auf Testmenge
l_features = ['CREDITSCORE','GEOGRAPHY','GENDER','AGE',
    'TENURE','BALANCE','NUMOFPRODUCTS',
    'HASCRCARD','ISACTIVEMEMBER','ESTIMATEDSALARY']

g_df_predict_test = rfc.predict(data = g_df_test,
    key = 'CUSTOMERID',
    features = l_features)

g_df_predict_test.collect()

