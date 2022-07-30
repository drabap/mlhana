# Initialisieren und Konfigurieren des Gradient Boosting
from hana_ml.algorithms.apl.gradient_boosting_classification import GradientBoostingBinaryClassifier

g_gradboost_c = GradientBoostingBinaryClassifier()

# Konfigurieren mit optionalen Parametern
g_gradboost_c.set_params(
    eval_metric = 'LogLoss',
    max_depth = 4,
    learningrate = 0.05
)
