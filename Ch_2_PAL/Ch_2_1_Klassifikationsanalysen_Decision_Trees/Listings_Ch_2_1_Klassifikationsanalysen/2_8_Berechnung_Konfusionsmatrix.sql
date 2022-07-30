-- Listing Abfrage der Prognoseergebnisse

-- im anonymen Block aus Listing 2.2. hinter dem Code von Listing 2.7 einfügen

lt_input_confusion = SELECT CHURN.CUSTOMERID,
    CONCAT('',CHURN.EXITED) AS original_label,
    t_predicted.SCORE AS predicted_label
    FROM CHURN
    JOIN :lt_pal_result AS t_predicted 
    ON CHURN.CUSTOMERID = t_predicted.CUSTOMERID;

lt_parameter_table = SELECT * FROM #pal_parameter_tbl
    WHERE NULL IS NOT NULL;

_SYS_AFL.PAL_CONFUSION_MATRIX(:lt_input_confusion,
    :lt_parameter_table,
    lt_confusion_matrix,
    lt_classification_report);

SELECT * FROM :lt_confusion_matrix;
