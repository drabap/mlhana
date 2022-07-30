-- Aufruf der Trainingsprozedur

-- Einfügen in Quellcode aus Listing 2.2 vor END

_SYS_AFL.PAL_DECISION_TREE (
    :lt_input_train,
    :lt_parameter_tbl,
    lt_model,
    lt_decision_rules,
    lt_confusion_matrix_train,
    lt_statistics,
    lt_cross_validation);

-- Optional: Ausgabe der Entscheidungsregeln und der Konfusionsmatrix
SELECT * FROM :lt_decision_rules;
SELECT * FROM :lt_confusion_matrix_train;

