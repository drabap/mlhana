-- Anwenden des trainierten Modells auf Testdaten

-- im anonymen Block aus Listing 2.2. hinter dem Code von Listing 2.5 einfügen

-- Leere Parametertabelle erzeugen
lt_parameters_predict = SELECT * FROM #PAL_PARAMETER_TBL
    WHERE NULL IS NOT NULL;

_SYS_AFL.PAL_DECISION_TREE_PREDICT(:lt_input_prediction,
    :lt_model,
    :lt_parameters_predict,
    lt_pal_result);
