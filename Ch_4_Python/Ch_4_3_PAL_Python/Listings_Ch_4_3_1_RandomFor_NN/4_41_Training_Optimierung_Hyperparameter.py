# Training mit Optimierung der Hyperparameter
from hana_ml.algorithms.pal.neural_network import *

# Mögliche Werte für Netztopologie
hidden_layer_opt = [(30,20,10,5),(10,10,5,5),
    (30,20,10),(10,5)]


mlp_c_opt = MLPClassifier(
    # hidden_layer_size = (10,10,5,5),
    hidden_layer_size_options = hidden_layer_opt,
    activation = 'sigmoid_symmetric',
    output_activation = 'sigmoid_symmetric',
    training_style = 'batch',
    max_iter = 1000,
    normalization = 'z-transform',
    weight_init = 'normal',
    thread_ratio = 0.3,
    categorical_variable = ['EXITED',
        'HASCRCARD',
        'ISACTIVEMEMBER'],
    resampling_method = 'cv',
    fold_num = 4,
    evaluation_metric = 'f1_score',
    search_strategy = 'grid',
    progress_indicator_id = 'TEST'
    )

l_features = ['CREDITSCORE','GEOGRAPHY','GENDER','AGE',
    'TENURE','BALANCE','NUMOFPRODUCTS',
    'HASCRCARD','ISACTIVEMEMBER','ESTIMATEDSALARY']

mlp_c_opt.fit( data = g_df_train_nn,
    key = 'CUSTOMERID',
    features = l_features,
    label = 'EXITED' )
