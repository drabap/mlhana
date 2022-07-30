/* Ch. 3.2.3 - Profitcurve Detected für CHURN Prediction
	Prozedur EXPORT_PROFITCURVE anwenden.
	Kurventyp: DETECTED
    Dieser Kurventyp zeigt, wieviel % der Instanzen der Zielkategorie gefunden werden,
        wenn man gemäß der Scoring-Prognose des Modells eine Teilmenge aus den Testdaten mit vorgegebener Größe zieht
        Bsp.: Man selektiert 20% der Testdaten sortiert nach dem Score des Klassifikationsmodell.
              Wieviel % der Kündiger findet man?

	Funktionen: EXPORT_PROFITCURVE
				- Modell: ML_DATA.MODEL_TEST_BIN
				- Datengrundlage: CHURN_TEST (nur indirekt verwendet über MODEL_TEST_BIN)
				- Ergebnistabellen: EXPORT_CURVE_DETECTED
                
    Voraussetzung: Modell wurde auf Testdaten angewandt mit Methode APPLY_MODEL_AND_TEST und das aktualisierte Modell in Tabelle MODEL_TEST_BIN gespeichert 
	
*/

SET SCHEMA ML_APL;

/*
 Clean up: Verwendet Tabellen löschen => bei erster Durchführung überspringen
*/
DROP TABLE ML_APL.FUNC_HEADER_CURVE;
DROP TABLE ML_APL.EXPORTCURVE_CONFIG;
DROP TABLE ML_APL.EXPORT_CURVE_DETECTED;

/*
 Eingabeparameter FUNC_HEADER aufbauen 
 Erstellt die Tabelle APPLY_FUNC_HEADER. Diese wird dann als Wert für FUNC_HEADER verwendet
*/
CREATE TABLE ML_APL.FUNC_HEADER_CURVE LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.FUNCTION_HEADER";
INSERT INTO ML_APL.FUNC_HEADER_CURVE VALUES ('Oid', '#CHURN_42');

/*
   Eingabeparameter OPERATION_CONFIG aufbauen
   Erstellt die Tabelle EXPORTCURVE_CONFIG. Diese wird dann als Wert für OPERATION_CONFIG verwendet 
*/
CREATE TABLE ML_APL.EXPORTCURVE_CONFIG LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.OPERATION_CONFIG_EXTENDED";
INSERT INTO ML_APL.EXPORTCURVE_CONFIG VALUES ('APL/ModelName', 'Churn Model',null);
INSERT INTO ML_APL.EXPORTCURVE_CONFIG VALUES ('APL/ModelComment', 'Published from APL',null);
INSERT INTO ML_APL.EXPORTCURVE_CONFIG VALUES ('APL/ModelSpaceName', '"MODELS"',null);
-- Angabe mehrere Kurventypen möglich mit Kommata getrennt: roc,detected,lift,sensitivity
INSERT INTO ML_APL.EXPORTCURVE_CONFIG VALUES ('APL/CurveType', 'detected',null);
INSERT INTO ML_APL.EXPORTCURVE_CONFIG VALUES ('APL/CurvePointCount', '100',null);


DO BEGIN     
    lt_header   = SELECT * FROM FUNC_HEADER_CURVE;       
    lt_model_in = SELECT * FROM MODEL_TEST_BIN;   
    lt_config   = SELECT * FROM EXPORTCURVE_CONFIG;          

   "SAP_PA_APL"."sap.pa.apl.base::EXPORT_PROFITCURVES"(:lt_header, :lt_model_in, :lt_config, lt_out_curves);
    
    -- Rohausgabe von Prozedur EXPORT_PROFITCURVES
    SELECT * FROM :lt_out_curves;
    
    -- Speichern des Ergebnis und Datentypen in Dezimalzahlen casten und aussagekräftige Namen vergeben
    CREATE TABLE EXPORT_CURVE_DETECTED AS (
    	SELECT 
    	type,-- Typ der Kurve (Hier nur: detected)
    	cast( "Frequency" as dec(10,7)) as part_population,
    	cast( "ApplyIn" as dec(10,7) ) as detected_apply,
    	cast( "Validation" as dec(10,7) ) as detected_validation,
    	cast( "Random" as dec(10,7) ) as detected_random,
    	cast( "Wizard" as dec(10,7) ) as detected_wizard
    	    	
    	FROM :lt_out_curves
    	
    	);
END;
