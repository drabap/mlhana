/* Kapitel 3, 3.2.1 Modell trainieren 
	Extrahiert Informationen aus einem trainierten Modell
	

    Voraussetzung: Skript Ch_3_2_1_APL_CREATE_MODEL_AND_TRAIN.sql wurde ausgeführt
    Input: Tabelle MODEL_TRAIN_BIN
    Ausgabe: Variablenbeschreibung (lt_variable_desc), 
             Variablenrollen (lt_variable_roles),
             Zusammenfassung (lt_summary),
             Indikatoren (lt_indicators)

*/

SET SCHEMA ML_APL;


-- Ab zweiter Ausführung: Tabellen löschen
DROP TABLE APPLY_FUNC_HEADER;
DROP TABLE MODEL_INFO_CONFIG;

DO BEGIN



CREATE TABLE APPLY_FUNC_HEADER LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.FUNCTION_HEADER";

INSERT INTO APPLY_FUNC_HEADER VALUES ('Oid', '#CHURN_42');
INSERT INTO APPLY_FUNC_HEADER VALUES ('LogLevel', '8');
INSERT INTO APPLY_FUNC_HEADER VALUES ('ModelFormat', 'bin');


CREATE TABLE MODEL_INFO_CONFIG LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.OPERATION_CONFIG_EXTENDED";


lt_func_header = SELECT * FROM FUNC_HEADER;
lt_model = SELECT * FROM MODEL_TRAIN_BIN;
lt_model_config = SELECT * FROM MODEL_INFO_CONFIG;


-- Beispiel: Variablenbeschreibung extrahieren
"SAP_PA_APL"."sap.pa.apl.base::EXPORT_VARIABLEDESCRIPTIONS"(:lt_func_header, 
															:lt_model,
															lt_variable_desc);
SELECT * FROM :lt_variable_desc;



-- Beispiel: Indikatoren und Zusammenfassung extrahieren
"SAP_PA_APL"."sap.pa.apl.base::GET_MODEL_INFO"(:lt_func_header, 
                                               :lt_model, 
                                               :lt_model_config, 
                                               lt_summary, 
                                               lt_variable_roles,
                                               lt_variable_desc,
                                               lt_indicators,
                                               lt_profitcurves ); 

SELECT * FROM :lt_variable_roles;
SELECT * FROM :lt_summary;
SELECT * FROM :lt_indicators;

END;