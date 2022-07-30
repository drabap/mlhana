/* Kapitel 2, Abschnitt 2.2 Clustering-Analysen mit K-Means, 
-- Zusatz: Cluster Assignment aufrufen mit gespeichertem Modell
-- Voraussetzung: In der Tabelle ML_DATA.PAL_KMEANS_MODEL ist das Clustering-Modell nach Ausführung vom Skript PAL_CHURN_KMEANS.sql gespeichert

-- Ablauf:
-- Aufbau der Parameter-Tabelle
-- Laden des zuvor erstellten Cluster-Modell
-- Es werden zufällig 20 Kunden aus ML_DATA.CHURN abgerufen.
-- Für diese Datensätze wird die Prozedur PAL_CLUSTER_ASSIGNMENT aufgerufen und die Clusterzuweisung ausgegeben.

*/
SET SCHEMA ML_DATA;


DO BEGIN


CREATE LOCAL TEMPORARY COLUMN TABLE #PAL_PARAMETER_ASSIGN(
	PARAM_NAME NVARCHAR(256), 
	INT_VALUE INTEGER, 
	DOUBLE_VALUE DOUBLE, 
	STRING_VALUE NVARCHAR(1000)
);


INSERT INTO #PAL_PARAMETER_ASSIGN VALUES ('DISTANCE_LEVEL',2, NULL, NULL);
INSERT INTO #PAL_PARAMETER_ASSIGN VALUES ('THREAD_RATIO', NULL, 0.5, NULL);

lt_parameter = SELECT * FROM #PAL_PARAMETER_ASSIGN;

SELECT * FROM :lt_parameter;

lt_model = SELECT * FROM PAL_KMEANS_MODEL;

lt_churn = SELECT TOP 20 CUSTOMERID,
				  GEOGRAPHY,
				  AGE,
				  TENURE,
				  BALANCE,
				  NUMOFPRODUCTS,
				  ESTIMATEDSALARY
				  FROM CHURN ORDER BY RAND();

SELECT * FROM :lt_churn;

CALL _SYS_AFL.PAL_CLUSTER_ASSIGNMENT(:lt_churn, 
                          :lt_model,
                          :lt_parameter, 
                          lt_assignment);
                          
SELECT * FROM :lt_assignment;                          

DROP TABLE #PAL_PARAMETER_ASSIGN;

END;