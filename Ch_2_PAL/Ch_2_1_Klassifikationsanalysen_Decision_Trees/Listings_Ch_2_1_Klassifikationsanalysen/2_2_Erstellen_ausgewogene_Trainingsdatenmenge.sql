-- Erstellen einer ausgewogenen Trainingsdatenmenge
-- Code dient zugleich als Grundgerüst für die Aufnahme der weiteren Listings
SET SCHEMA ML_DATA;

DO
BEGIN

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

-- Hier Code der unten folgenden Listings einfügen
-- Listing 2.3 Vorbereiten der Parameter-Tabelle
-- Listing 2.4 Aufruf Trainingsprozedur
-- Listings aus Abschnitt 2.1.2 (Testen des trainierten Modells) ebenso anfügen: Listing 2.5, 2.6, 2.7, 2.8, 2.9, 
END;

