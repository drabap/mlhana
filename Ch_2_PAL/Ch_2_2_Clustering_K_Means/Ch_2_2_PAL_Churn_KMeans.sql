SET SCHEMA ML_DATA;

-- Vor erneutem Durchlauf: Tabellen löschen
-- Diesen Quelltext einkommentieren ab zweitem Durchlauf
-- DROP TABLE #PAL_PARAMETER_TBL;
-- DROP TABLE CLUST_RES_CHURN;
-- Falls Modell gespeichert wird => auch diese Tabelle löschen
-- DROP TABLE ML_DATA.PAL_KMEANS_MODEL;

DO BEGIN

-- Clustering mit PAL

/*
 * Aufbau der Parametertabelle
 * Nicht im Buch aufgeführt
*/


-- Parametertabelle aufbauen
CREATE LOCAL TEMPORARY COLUMN TABLE #PAL_PARAMETER_TBL(
	PARAM_NAME NVARCHAR(256), 
	INT_VALUE INTEGER, 
	DOUBLE_VALUE DOUBLE, 
	STRING_VALUE NVARCHAR(1000)
);


INSERT INTO #PAL_PARAMETER_TBL VALUES ('GROUP_NUMBER', 4, NULL, NULL);
INSERT INTO #PAL_PARAMETER_TBL VALUES ('INIT_TYPE', 3, NULL, NULL);
INSERT INTO #PAL_PARAMETER_TBL VALUES ('DISTANCE_LEVEL',2, NULL, NULL);
INSERT INTO #PAL_PARAMETER_TBL VALUES ('THREAD_RATIO', NULL, 0.5, NULL);


-- Weitere Parameter zum Experimentieren
--INSERT INTO #PAL_PARAMETER_TBL VALUES ('GROUP_NUMBER_MIN', 4, NULL, NULL);
--INSERT INTO #PAL_PARAMETER_TBL VALUES ('GROUP_NUMBER_MAX', 10, NULL, NULL);
--INSERT INTO #PAL_PARAMETER_TBL VALUES ('CATEGORY_WEIGHTS', NULL, 0.5, NULL);
--INSERT INTO #PAL_PARAMETER_TBL VALUES ('MAX_ITERATION', 100, NULL, NULL);
--INSERT INTO #PAL_PARAMETER_TBL VALUES ('EXIT_THRESHOLD', NULL, 1.0E-6, NULL);

lt_parameter = SELECT * FROM #PAL_PARAMETER_TBL;

SELECT * FROM :lt_parameter;

/*
 * Listing: Aufruf von K-Means
 *
*/

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

-- Optional: Ausgabe von Zuweisung (LT_RESULT) und Zentrumspunkten (LT_CENTERS)
--SELECT * FROM :lt_result;

--SELECT * FROM :lt_centers;

/*
 * Listing: Clusterzentren ausgeben und Zuweisungen zählen
*/

lt_cen_count = SELECT CLUSTER_ID,
    count(*) AS COUNT_MEM FROM :lt_result 
    GROUP BY CLUSTER_ID;

lt_cen_res = SELECT cen.CLUSTER_ID,
    COUNT_MEM,
    cen.AGE,
    cen.BALANCE,
    cen.ESTIMATEDSALARY
    FROM :lt_centers AS cen 
    JOIN :lt_cen_count AS cen_count 
    ON cen.CLUSTER_ID = cen_count.CLUSTER_ID;

SELECT * FROM :lt_cen_res ORDER BY COUNT_MEM;


/*
 * Listing: Clusterzuordnung mit Quelldaten verknüpfen und speichern
*/

lt_churn_w_clust = SELECT clust_assign.CLUSTER_ID,
                          clust_assign.DISTANCE,
                          churn.* 
                               FROM :lt_result AS clust_assign
                               JOIN :lt_churn AS churn 
                               ON clust_assign.CUSTOMERID = churn.CUSTOMERID;

-- Zuordnung Datensatz zu Cluster ausgeben
SELECT * FROM :lt_churn_w_clust;

-- Speichern der Clusterzuweisung in Tabelle
CREATE TABLE CLUST_RES_CHURN AS (
    SELECT * FROM :lt_churn_w_clust );


-- Ausgabe der Statistiken
SELECT * FROM :lt_statistics;


-- Zusatz: Modellausgabe
-- SELECT * FROM :lt_model;

-- Speichern des Modells für spätere Verwendung
CREATE TABLE ML_DATA.PAL_KMEANS_MODEL AS (SELECT * FROM :lt_model);

END;
