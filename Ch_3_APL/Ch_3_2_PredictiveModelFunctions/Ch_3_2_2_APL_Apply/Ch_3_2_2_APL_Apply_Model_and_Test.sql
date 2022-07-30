/* CHURN Prediction mit APL
	Trainiertes Modell von Skript CREATE_MODEL_AND_TRAIN.sql anwenden

	Funktionen: APPLY_MODEL_AND_TEST
				- Daten: ML_APL.CHURN_TEST
				- Modell: ML_APL.MODEL_TRAIN_BIN
				- Ergebnistabellen: CHURN_APPLY, MODEL_TEST_BIN, APPLY_LOG, APPLY_TEST_INDICATORS 
    Voraussetzung: Modell trainiert und in Tabelle MODEL_TRAIN_BIN gespeichert 
	

*/

SET SCHEMA ML_APL;

/*
 Clean up: Verwendete Tabellen löschen => bei erster Durchführung überspringen
*/
DROP TABLE APPLY_FUNC_HEADER;
DROP TABLE APPLY_CONFIG;
DROP TABLE CHURN_APPLY;

DROP TABLE APPLY_TEST_INDICATOR;
DROP TABLE APPLY_LOG;-- nicht im Buch

DROP TABLE MODEL_TEST_BIN;-- wird bei Prognosebildung erstellt

/*
 Eingabeparameter FUNC_HEADER aufbauen 
 Erstellt die Tabelle APPLY_FUNC_HEADER. Diese wird dann als Wert für FUNC_HEADER verwendet
*/

CREATE TABLE APPLY_FUNC_HEADER LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.FUNCTION_HEADER";

INSERT INTO APPLY_FUNC_HEADER VALUES ('Oid', '#CHURN_42');
INSERT INTO APPLY_FUNC_HEADER VALUES ('LogLevel', '8');
INSERT INTO APPLY_FUNC_HEADER VALUES ('ModelFormat', 'bin');

/*
 Eingabeparameter OPERATION_CONFIG aufbauen
 Erstellt die Tabelle APPLY_CONFIG und füllt diese. Diese wird dann als Eingabeparameter OPERATION_CONFIG verwendet.
*/

CREATE TABLE APPLY_CONFIG LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.OPERATION_CONFIG_EXTENDED";

-- Ausgabe der Klassenzuordnung
INSERT INTO APPLY_CONFIG VALUES ('APL/ApplyExtraMode', 'Decision', null);
-- Ausgabe des Scores:
--INSERT INTO APPLY_CONFIG VALUES ('APL/ApplyExtraMode', 'Score', null);
-- Ausgabe der Wahrscheinlichkeit:
--INSERT INTO APPLY_CONFIG VALUES ('APL/ApplyExtraMode', 'Probability', null);
-- Entscheidungsschwelle: Beispiel in Buch 0.3
INSERT INTO APPLY_CONFIG VALUES ('APL/ApplyDecisionThreshold', '0.3', null);
-- Alternativ: Höherer Wert für Entscheidungsschwelle
--INSERT INTO APPLY_CONFIG VALUES ('APL/ApplyDecisionThreshold', '0.75', null);


-- Ausgabe der Prognose
-- Je nach Parameterwert APL/ApplyExtraMode
CREATE COLUMN TABLE CHURN_APPLY(
    CUSTOMERID INTEGER,
    EXITED INTEGER,
    -- ApplyExtraMode Decision
    GB_DECISION_EXITED BIGINT
    -- ApplyExtraMode Score
    -- GB_SCORE_EXITED DOUBLE
    -- ApplyExtraMode Probability
    -- GB_PROBA_EXITED DOUBLE
);



/*
 Aufbau der Ausgabeparameter
*/
CREATE COLUMN TABLE APPLY_TEST_INDICATOR LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.INDICATORS";
CREATE COLUMN TABLE APPLY_LOG LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.OPERATION_LOG";-- nicht im  Buch verwendet




DO BEGIN

lt_apply_func_header = SELECT * FROM APPLY_FUNC_HEADER;
lt_model_train = SELECT * FROM MODEL_TRAIN_BIN;
lt_apply_config = SELECT * FROM APPLY_CONFIG;


-- Optional: Vorschlag für Tabellentyp der Ausgabe ermitteln
CALL "SAP_PA_APL"."sap.pa.apl.base::GET_TABLE_TYPE_FOR_APPLY"( :lt_apply_func_header, 
                                                               :lt_model_train, 
                                                               :lt_apply_config, 
                                                               'ML_APL','CHURN_TEST', 
                                                               lt_output_table, 
                                                               lt_log );
                                                               
SELECT * FROM :lt_output_table;                                                               

DELETE FROM CHURN_APPLY;

CALL "SAP_PA_APL"."sap.pa.apl.base::APPLY_MODEL_AND_TEST"( :lt_apply_func_header, 
                                                           :lt_model_train, 
                                                           :lt_apply_config, 
                                                           'ML_APL','CHURN_TEST', 
                                                           'ML_APL','CHURN_APPLY', 
                                                           lt_model_out,
                                                           lt_apply_log,
                                                           lt_apply_test_indicator);


SELECT * FROM CHURN_APPLY;

INSERT INTO APPLY_TEST_INDICATOR ( SELECT * FROM :lt_apply_test_indicator );

CREATE TABLE MODEL_TEST_BIN AS ( SELECT * FROM :lt_model_out);

-- Optional: Speichern von Log
-- INSERT INTO APPLY_LOG ( SELECT * FROM :lt_apply_log );

END;

-- Zusatz: Aggregiere Nach EXITED und GB_DECISION_PREDICTED => Grundlage für Konfusionsmatrix

SELECT exited, gb_decision_exited,
    COUNT(*) as count FROM CHURN_APPLY
    GROUP BY exited, gb_decision_exited
    ORDER BY exited, gb_decision_exited;

