SET SCHEMA ML_DATA;

-- Vor erneutem Durchlauf: Tabellen löschen

-- Diesen Quelltext einkommentieren ab zweitem Durchlauf
-- DROP TABLE #PAL_PARAMETER_TBL;
-- DROP TABLE CLUST_RES_CHURN;
-- Falls Modell gespeichert wird => auch diese Tabelle
-- löschen
-- DROP TABLE ML_DATA.PAL_KMEANS_MODEL;

DO BEGIN

-- Aufbau der Parametertabelle
-- Auslassung, siehe Quellcodeverzeichnis

lt_churn = SELECT CUSTOMERID,
    GEOGRAPHY,
    AGE,
    TENURE,
    BALANCE,
    NUMOFPRODUCTS,
    ESTIMATEDSALARY
    FROM CHURN WHERE BALANCE > 0;

CALL _SYS_AFL.PAL_KMEANS(:lt_churn,
    :lt_parameter,
    lt_result,
    lt_centers,
    lt_model,
    lt_statistics,
    lt_placeholder);

-- Optional: Ausgabe von Zuweisung (LT_RESULT) und 
-- Zentrumspunkten (LT_CENTERS)
--SELECT * FROM :lt_result;
--SELECT * FROM :lt_centers;

-- Einfügen: Auswertung aus weiteren Listings unten
--    Abfrage lt_statistics, Modell speichern etc.
END;


