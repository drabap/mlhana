# Model Storage initialisieren und Modell speichern
from hana_ml.model_storage import ModelStorage, ModelStorageError

model_storage = ModelStorage(
    connection_context = connection,
    schema = 'ML_MODEL')

g_model_name_rfc = 'RandomForest CHURN'

rfc.name = g_model_name_rfc

model_storage.save_model(model = rfc,
    if_exists = 'upgrade')
