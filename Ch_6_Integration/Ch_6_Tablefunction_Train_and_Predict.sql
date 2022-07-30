SET SCHEMA ML_MODEL;

CREATE OR REPLACE FUNCTION train_and_predict( i_max_depth int)
RETURNS TABLE (TYPE nvarchar(20), ROW_INDEX  int,
               MODEL_CONTENT nvarchar(5000),
               ACTUAL_CLASS int,
               PREDICTED_CLASS int,
               ROW_COUNT int,
               CUSTOMERID integer,
               SCORE nvarchar(1),
               CONFIDENCE double )
AS BEGIN
    
/* Variablendeklaration

*/
declare lt_parameter_tbl table(
        NAME VARCHAR (50),
        INT_VALUE INTEGER,
        DOUBLE_VALUE DOUBLE,
        STRING_VALUE VARCHAR (100));

declare lt_model table(row_index  int,
               model_content nvarchar(5000));
               
declare lt_rules table(row_index integer, rules_content nvarchar(5000));

declare lt_confusion_matrix table(actual_class nvarchar(1000), predicted_class nvarchar(1000), count int );



declare lt_statistics table(stat_name nvarchar(1000), stat_value nvarchar(1000));

declare lt_cross_validation table(
        param_NAME VARCHAR (50),
        INT_VALUE INTEGER,
        DOUBLE_VALUE DOUBLE,
        STRING_VALUE VARCHAR (100));
        
declare lt_pal_result table( customerid integer, score nvarchar(1), confidence double );

declare lt_confusion_matrix_test table(original_label nvarchar(100), predicted_label nvarchar(100), count int );

declare lt_classification_report table(class nvarchar(100), recall double, precision double, f_measure double, support int);

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
    EXITED FROM ML_DATA.CHURN;

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

/* Listing: Vorbereiten der Parameter-Tabelle
*/


INSERT INTO :lt_parameter_tbl VALUES
    ('ALGORITHM', 1, NULL, NULL); 
INSERT INTO :lt_parameter_tbl VALUES
    ('HAS_ID', 1, NULL, NULL);

INSERT INTO :lt_parameter_tbl VALUES
    ('CATEGORICAL_VARIABLE', NULL, NULL, 'EXITED');
INSERT INTO :lt_parameter_tbl VALUES
    ('CATEGORICAL_VARIABLE', NULL, NULL, 'HASCRCARD');
INSERT INTO :lt_parameter_tbl VALUES
    ('CATEGORICAL_VARIABLE', NULL, NULL, 'ISACTIVEMEMBER');

INSERT INTO :lt_parameter_tbl VALUES
    ('MAX_DEPTH', :i_max_depth, NULL, NULL);


/* Listing: Aufruf der Trainingsprozedur
*/

_SYS_AFL.PAL_DECISION_TREE (    :lt_input_train,
							    :lt_parameter_tbl,
								lt_model,
								lt_rules,
								lt_confusion_matrix,
								lt_statistics,
								lt_cross_validation);

/* Prognosebildung
*/


lt_parameters_predict = SELECT * FROM :lt_parameter_tbl WHERE NULL IS NOT NULL;

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


CALL _SYS_AFL.PAL_DECISION_TREE_PREDICT(:lt_input_prediction, 
										:lt_model, 
										:lt_parameters_predict,
										 lt_pal_result);


-- Konfusionsmatrix mit Testdaten berechnen
lt_input_confusion = SELECT CHURN.CUSTOMERID,
    CONCAT('',CHURN.EXITED) AS original_label,
    t_predicted.SCORE AS predicted_label
    FROM ML_DATA.CHURN
    JOIN :lt_pal_result AS t_predicted 
    ON CHURN.CUSTOMERID = t_predicted.CUSTOMERID;

lt_parameter_table = SELECT * FROM :lt_parameters_predict
    WHERE NULL IS NOT NULL;

_SYS_AFL.PAL_CONFUSION_MATRIX(:lt_input_confusion,
    :lt_parameter_table,
    lt_confusion_matrix_test,
    lt_classification_report);

--SELECT * FROM :lt_confusion_matrix;


RETURN SELECT 'MODEL' AS TYPE, ROW_INDEX, model_content, NULL as actual_class, NULL as predicted_class, NULL as row_count, NULL as customerid, NULL as score, NULL as confidence from :lt_model
UNION SELECT 'MATRIX_TRAIN' AS TYPE, NULL as ROW_INDEX, NULL as MODEL_CONTENT, actual_class, predicted_class, count as row_count, NULL as customerid, NULL as score, NULL as confidence from :lt_confusion_matrix
UNION SELECT 'MATRIX_TEST' AS TYPE, NULL as ROW_INDEX, NULL as MODEL_CONTENT, original_label as actual_class, predicted_label as predicted_class, count as row_count, NULL as customerid, NULL as score, NULL as confidence from :lt_confusion_matrix_test
UNION SELECT 'PREDICT' as TYPE, NULL as ROW_INDEX, NULL as MODEL_CONTENT, NULL as actual_class, NULL as predicted_class, NULL as row_count, customerid, score, confidence from :lt_pal_result;


END;