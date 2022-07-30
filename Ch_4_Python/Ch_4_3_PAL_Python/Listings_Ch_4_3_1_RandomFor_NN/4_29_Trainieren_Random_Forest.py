# Trainieren des Random Forest
from hana_ml.algorithms.pal.trees import *

rfc = RDTClassifier(
    n_estimators = 10,
    max_features = 10, random_state = 2,
    split_threshold = 0.00001,
    categorical_variable = ['EXITED'],
    strata = [(0,0.5),(1,0.5)],
    thread_ratio = 1.0
    )

l_features = ['CREDITSCORE','GEOGRAPHY','GENDER','AGE',
    'TENURE','BALANCE','NUMOFPRODUCTS',
    'HASCRCARD','ISACTIVEMEMBER','ESTIMATEDSALARY']

rfc.fit(data = g_df_train,
    key = 'CUSTOMERID',
    features = l_features, 
    label = 'EXITED')

# rfc.model_.collect()
