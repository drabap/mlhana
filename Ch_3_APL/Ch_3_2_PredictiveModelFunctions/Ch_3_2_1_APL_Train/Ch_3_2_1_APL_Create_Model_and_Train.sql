/* CHURN Prediction mit APL
	Verwendung des Algorithmus binary classification
	

	Funktionen: CREATE_MODEL_AND_TRAIN
	Modus: Balanced Set => 50% Kündiger, 50% nicht-Kündiger
           Imbalanced => 2000 als Stichtprobe ziehen 

    Erzeugt: CHURN_TRAIN, CHURN_TEST
    Ausgabetabellen: MODEL_TRAIN_BIN, TRAIN_LOG, SUMMARY, INDICATORS_TRAIN

*/

SET SCHEMA ML_APL;

/*
 * Ab zweiter Ausführung: Tabellen vorher löschen
*/

-- Steuertabellen für Training des Modells
DROP TABLE FUNC_HEADER;
DROP TABLE TRAIN_CONFIG;
DROP TABLE VARIABLE_DESC;
DROP TABLE VARIABLE_ROLES;

-- Ergebnistabellen
DROP TABLE MODEL_TRAIN_BIN;
DROP TABLE TRAIN_LOG;
DROP TABLE SUMMARY;
DROP TABLE INDICATORS_TRAIN;

-- Eingabedaten für Training und Test
DROP TABLE CHURN_TRAIN;
DROP TABLE CHURN_TEST;

/*
* Aufbau FUNC_HEADER
*/

CREATE TABLE FUNC_HEADER LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.FUNCTION_HEADER";
INSERT INTO FUNC_HEADER VALUES ('Oid', '#CHURN_42');
INSERT INTO FUNC_HEADER VALUES ('LogLevel', '8');
INSERT INTO FUNC_HEADER VALUES ('ModelFormat', 'bin');
-- Testausgabe FUNC_HEADER
SELECT * FROM FUNC_HEADER;

/*
* Aufbau TRAIN_CONFIG (= Eingabeparameter OPERATION_CONFIG)
*/
CREATE TABLE TRAIN_CONFIG LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.OPERATION_CONFIG_EXTENDED";
INSERT INTO TRAIN_CONFIG VALUES ('APL/ModelType', 'binary classification',null);
INSERT INTO TRAIN_CONFIG VALUES ('APL/IndicatorDataset', 'Validation',null);
-- Testausgabe TRAIN_CONFIG
SELECT * FROM TRAIN_CONFIG;

/*
* Aufbau VARIABLE_DESC 
*/
CREATE TABLE VARIABLE_DESC LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.VARIABLE_DESC_OID";

INSERT INTO VARIABLE_DESC VALUES('0','CUSTOMERID', 'integer','nominal',1,0,'','','Unique identifier of customer',null);
INSERT INTO VARIABLE_DESC VALUES('1','CREDITSCORE', 'integer','continuous',0,0,'','','Credit score',null);
INSERT INTO VARIABLE_DESC VALUES('2','GEOGRAPHY', 'string','nominal',0,0,'','','Geography',null);
INSERT INTO VARIABLE_DESC VALUES('3','GENDER', 'string','nominal',0,0,'','','Gender',null);
INSERT INTO VARIABLE_DESC VALUES('4','AGE', 'integer','continuous',0,0,'','','Age',null);
INSERT INTO VARIABLE_DESC VALUES('5','TENURE', 'integer','ordinal',0,0,'','','Tenure',null);
INSERT INTO VARIABLE_DESC VALUES('6','BALANCE', 'number','continuous',0,0,'','','Balance',null);
INSERT INTO VARIABLE_DESC VALUES('7','NUMOFPRODUCTS', 'integer','ordinal',0,0,'','','Number of products',null);
INSERT INTO VARIABLE_DESC VALUES('8','HASCRCARD', 'integer','nominal',0,0,'','','Has credit card',null);
INSERT INTO VARIABLE_DESC VALUES('9','ISACTIVEMEMBER', 'integer','nominal',0,0,'','','Active member',null);
INSERT INTO VARIABLE_DESC VALUES('10','ESTIMATEDSALARY', 'number','continuous',0,0,'','','Estimated salary',null);
INSERT INTO VARIABLE_DESC VALUES('11','EXITED', 'integer','nominal',0,0,'','','Customer has exited',null);
-- Testausgabe VARIABLE_DESC
SELECT * FROM VARIABLE_DESC;


/*
* Aufbau VARIABLE_ROLES 
*/
CREATE TABLE VARIABLE_ROLES LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.VARIABLE_ROLES_WITH_COMPOSITES_OID";
INSERT INTO variable_roles VALUES('EXITED', 'target',null,null,null);
-- Testausgabe VARIABLE_ROLES
SELECT * FROM VARIABLE_ROLES;

DO BEGIN

-- Modus: Zufallswahl
lt_id_train = SELECT TOP 2000 customerid  FROM ML_DATA.CHURN order by rand();

-- Alternativer Modus: Ausgeglichene Klassenverteilung
-- lt_id_train = (SELECT TOP 1200 customerid  FROM ML_DATA.CHURN WHERE exited = 0 order by rand() )
--			   UNION (SELECT TOP 800 customerid FROM ML_DATA.CHURN WHERE exited = 1 order by rand() );

CREATE TABLE CHURN_TRAIN AS (SELECT * 
							 FROM ML_DATA.CHURN 
							 WHERE EXISTS (SELECT CUSTOMERID FROM :lt_id_train WHERE CUSTOMERID = CHURN.CUSTOMERID));


CREATE TABLE CHURN_TEST AS (SELECT *
				            FROM ML_DATA.CHURN 
							WHERE NOT EXISTS (SELECT CUSTOMERID FROM :lt_id_train WHERE CUSTOMERID = CHURN.CUSTOMERID));

END;

DO BEGIN

lt_func_header = SELECT * FROM FUNC_HEADER;
lt_train_config = SELECT * FROM TRAIN_CONFIG;
lt_variable_desc = SELECT * FROM VARIABLE_DESC;
lt_variable_roles = SELECT * FROM VARIABLE_ROLES;

CALL "SAP_PA_APL"."sap.pa.apl.base::CREATE_MODEL_AND_TRAIN"(:lt_func_header, 
                                                            :lt_train_config, 
															:lt_variable_desc, 
															:lt_variable_roles, 
															'ML_APL',
															'CHURN_TRAIN', 
															lt_model_train_bin, 
															lt_train_log, 
															lt_train_summary, 
															lt_train_indicators);

SELECT * FROM :lt_model_train_bin;
SELECT * FROM :lt_train_log;
SELECT * FROM :lt_train_summary;
SELECT * FROM :lt_train_indicators;
-- Zusatz: Filtern der Indikatoren auf die Gütekennzahlen des Modells
SELECT * FROM :lt_train_indicators WHERE KEY IN ('PredictivePower','PredictionConfidence', 'KS','GINI','AUC','LogLoss');


CREATE TABLE MODEL_TRAIN_BIN LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.MODEL_BIN_OID";
INSERT INTO MODEL_TRAIN_BIN (SELECT * FROM :lt_model_train_bin);

CREATE TABLE TRAIN_LOG LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.OPERATION_LOG";
INSERT INTO TRAIN_LOG (SELECT * FROM :lt_train_log);

CREATE TABLE SUMMARY LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.SUMMARY";
INSERT INTO SUMMARY (SELECT * FROM :lt_train_summary);

CREATE TABLE INDICATORS_TRAIN LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.INDICATORS";
INSERT INTO INDICATORS_TRAIN (SELECT * FROM :lt_train_indicators);

END;
