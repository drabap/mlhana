/* Ch. 3.2.3 - Profitcurve ROC (Receiver Operating Characteristic) für CHURN Prediction
	Prozedur EXPORT_PROFITCURVE anwenden.
	Kurventyp: ROC

	Voraussetzung: Skript Ch_3_2_2_APL_Apply_Model_and_Test.sql: 
	  				- Modell wurde auf Testdaten angewandt mit Methode APPLY_MODEL_AND_TEST und das aktualisierte Modell in Tabelle MODEL_TEST_BIN gespeichert


	Funktionen: EXPORT_PROFITCURVE
				- Input: ML_DATA.MODEL_TEST_BIN
				- Datengrundlage: CHURN_TEST (nur indirekt verwendet über MODEL_TEST_BIN)
				- Ergebnistabellen: EXPORT_ROC
                
    
	 
	
*/

SET SCHEMA ML_APL;

/*
 Clean up: Verwendet Tabellen löschen => bei erster Durchführung überspringen
*/
DROP TABLE FUNC_HEADER_CURVE;
DROP TABLE EXPORTCURVE_CONFIG;
DROP TABLE EXPORT_PROFITCURVE_ROC;

/*
 Eingabeparameter FUNC_HEADER aufbauen 
 Erstellt die Tabelle APPLY_FUNC_HEADER. Diese wird dann als Wert für FUNC_HEADER verwendet
*/
CREATE TABLE FUNC_HEADER_CURVE LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.FUNCTION_HEADER";
INSERT INTO FUNC_HEADER_CURVE VALUES ('Oid', '#CHURN_42');

/*
   Eingabeparameter OPERATION_CONFIG aufbauen
   Erstellt die Tabelle EXPORTCURVE_CONFIG. Diese wird dann als Wert für OPERATION_CONFIG verwendet 
*/
CREATE TABLE EXPORTCURVE_CONFIG LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.OPERATION_CONFIG_EXTENDED";
INSERT INTO EXPORTCURVE_CONFIG VALUES ('APL/ModelName', 'Churn Model',null);
INSERT INTO EXPORTCURVE_CONFIG VALUES ('APL/ModelComment', 'Published from APL',null);
INSERT INTO EXPORTCURVE_CONFIG VALUES ('APL/ModelSpaceName', '"MODELS"',null);
-- Angabe mehrerer Kurventypen getrennt durch Semikolon möglich: roc;detected;lift;sensitivity
INSERT INTO EXPORTCURVE_CONFIG VALUES ('APL/CurveType', 'roc',null);
INSERT INTO EXPORTCURVE_CONFIG VALUES ('APL/CurvePointCount', '10',null);


DO BEGIN     
    lt_header   = SELECT * FROM FUNC_HEADER_CURVE;       
    lt_model_in = SELECT * FROM MODEL_TEST_BIN;   
    lt_config   = SELECT * FROM EXPORTCURVE_CONFIG;          

   "SAP_PA_APL"."sap.pa.apl.base::EXPORT_PROFITCURVES"(:lt_header, :lt_model_in, :lt_config, lt_out_curves);
    
    -- Rohausgabe von Prozedur EXPORT_PROFITCURVES
    SELECT * FROM :lt_out_curves;
    
    -- Speichern des Ergebnis, Datentypen in Dezimalzahlen casten und aussagekräftige Namen vergeben
    CREATE TABLE EXPORT_PROFITCURVE_ROC AS (
    	SELECT 
    	type,-- Typ der Kurve (Hier nur: roc)
    	cast( "Frequency" as dec(10,7)) as false_positive_rate,
    	cast( "ApplyIn" as dec(10,7) ) as recall_apply,
    	cast( "Validation" as dec(10,7) ) as recall_validation,
    	cast( "Random" as dec(10,7) ) as recall_random,
    	cast( "Wizard" as dec(10,7) ) as recall_wizard
    	    	
    	FROM :lt_out_curves
    	
    	);
END;
