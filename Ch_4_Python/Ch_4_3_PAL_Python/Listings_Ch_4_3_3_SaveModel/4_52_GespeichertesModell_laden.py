# Ein gespeichertes Modell laden
g_rfc_loaded = model_storage.load_model(
    name = g_model_name_rfc )

# Optionaler Parameter: version 
#    Default: Letzte Version nehmen

# Bestimmte Version laden:
g_rfc_loaded = model_storage.load_model(
    name = g_model_name_rfc, version = 2)
