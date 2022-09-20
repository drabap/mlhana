# Das neuronale Netz trainieren
from hana_ml.algorithms.pal.neural_network import *

mlp_c = MLPClassifier(hidden_layer_size = (30,15,10,5),
    activation = 'sigmoid_symmetric', 
    output_activation = 'sigmoid_symmetric',
    training_style = 'batch',
    max_iter = 1000,
    normalization = 'z-transform',
    weight_init ='normal',
    thread_ratio = 0.3,
    categorical_variable = ['EXITED',
        'HASCRCARD',
        'ISACTIVEMEMBER']
    )

l_features = ['CREDITSCORE','GEOGRAPHY','GENDER','AGE',
    'TENURE','BALANCE','NUMOFPRODUCTS',
    'HASCRCARD','ISACTIVEMEMBER','ESTIMATEDSALARY']

mlp_c.fit(data = g_df_train_nn,
    key = 'CUSTOMERID',
    features = l_features,
    label = 'EXITED')

