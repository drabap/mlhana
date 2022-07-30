/* Kapitel 2.1 - Klassifikationsanalysen mit Entscheidungsbäumen
*   Abschnitt 2.1.1 (Trainieren eines Entscheidungsbaums) und 2.1.2 (Testen des trainierten Modells)
*   Erstellen einer ausgewogenen Trainingsdatenmenge
*	Trainieren eines Modells mit den Trainingsdaten
*   Anwenden des Modells auf Testdaten und Vergleich Prognose/Ist
*   Performance-Evaluierung mit Konfusionsmatrix und Kennzahlen
*
*
*/ 

SET SCHEMA ML_DATA;

DO
BEGIN

/* Listing: Erstellen einer ausgewogenen Trainingsdatenmenge

*/

lt_input = SELECT CUSTOMERID,
    CREDITSCORE,
    GEOGRAPHY,
    GENDER,
    AGE,
    TENURE,
    BALANCE,
    NUMOFPRODUCTS,
    HASCRCARD,
    ISACTIVEMEMBER,
    ESTIMATEDSALARY,
    EXITED FROM CHURN;

-- Ausgewogene Trainingsmenge erstellen
lt_id_train = SELECT TOP 1000 CUSTOMERID FROM :lt_input
    WHERE EXITED = 1
    UNION SELECT TOP 1000 CUSTOMERID FROM :lt_input 
    WHERE EXITED = 0;

lt_input_train = SELECT * FROM :lt_input AS a 
    WHERE EXISTS (SELECT CUSTOMERID FROM :lt_id_train AS b
        WHERE b.CUSTOMERID = a.CUSTOMERID);

lt_input_test = SELECT * FROM :lt_input AS a
    WHERE NOT EXISTS (
        SELECT CUSTOMERID FROM :lt_id_train AS b
        WHERE b.CUSTOMERID = a.CUSTOMERID);


-- Optional: Ausgabe der Trainingsdatenmenge:
-- SELECT * FROM :lt_input_train;


/* Listing: Vorbereiten der Parameter-Tabelle
*/

CREATE LOCAL TEMPORARY COLUMN TABLE
    #PAL_PARAMETER_TBL(
        NAME VARCHAR (50),
        INT_VALUE INTEGER,
        DOUBLE_VALUE DOUBLE,
        STRING_VALUE VARCHAR (100));

INSERT INTO #PAL_PARAMETER_TBL VALUES
    ('ALGORITHM', 1, NULL, NULL); 
INSERT INTO #PAL_PARAMETER_TBL VALUES
    ('HAS_ID', 1, NULL, NULL);

INSERT INTO #PAL_PARAMETER_TBL VALUES
    ('CATEGORICAL_VARIABLE', NULL, NULL, 'EXITED');
INSERT INTO #PAL_PARAMETER_TBL VALUES
    ('CATEGORICAL_VARIABLE', NULL, NULL, 'HASCRCARD');
INSERT INTO #PAL_PARAMETER_TBL VALUES
    ('CATEGORICAL_VARIABLE', NULL, NULL, 'ISACTIVEMEMBER');

lt_parameter_tbl = SELECT * FROM #PAL_PARAMETER_TBL;

-- Optional: Ausgabe der Parameter-Tabelle
 SELECT * FROM :lt_parameter_tbl;


/* Listing: Aufruf der Trainingsprozedur
*/

_SYS_AFL.PAL_DECISION_TREE (    :lt_input_train,
							    :lt_parameter_tbl,
								lt_model,
								lt_decision_rules,
								lt_confusion_matrix_train,
								lt_statistics,
								lt_cross_validation);
-- Optional: Ausgabe der Entscheidungsregeln und der Konfusionsmatrix
SELECT * FROM :lt_decision_rules;
SELECT * FROM :lt_confusion_matrix_train;

/* Beginn Abschnitt 2.2.2 - Testen des trainierten Modells
*/

/* Listing 2.5: Vorbereitung der Eingabedaten für die Prognosebildung
*/

lt_input_prediction = SELECT CUSTOMERID,
    CREDITSCORE,
    GEOGRAPHY,
    GENDER,
    AGE,
    TENURE,
    BALANCE,
    NUMOFPRODUCTS,
    HASCRCARD,
    ISACTIVEMEMBER,
    ESTIMATEDSALARY FROM :lt_input_test;


/* Listing 2.6: Anwenden des trainierten Modells auf Testdaten
*/
lt_parameters_predict = SELECT * FROM #PAL_PARAMETER_TBL WHERE NULL IS NOT NULL;

CALL _SYS_AFL.PAL_DECISION_TREE_PREDICT(:lt_input_prediction, 
										:lt_model, 
										:lt_parameters_predict,
										 lt_pal_result);

/* Listing 2.7: Abfrage der Prognoseergebnisse
*/ 
SELECT TOP 20 * FROM :lt_pal_result;

/* Listing 2.8: Berechnung der Konfusionsmatrix
*/ 
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


/* Listing 2.9: Abfrage des Klassifikationsreport
*/
SELECT * FROM :lt_classification_report;

DROP TABLE #PAL_PARAMETER_TBL;

END;
