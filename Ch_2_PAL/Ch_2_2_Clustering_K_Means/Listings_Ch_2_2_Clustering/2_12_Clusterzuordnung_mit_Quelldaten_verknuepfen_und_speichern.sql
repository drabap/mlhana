lt_churn_w_clust = SELECT clust_assign.CLUSTER_ID,
    clust_assign.DISTANCE,
    churn.*
    FROM :lt_result AS clust_assign
    JOIN :lt_churn AS churn 
    ON clust_assign.CUSTOMERID = churn.CUSTOMERID;

-- Zuordnung Datensatz zu Cluster ausgeben
SELECT * FROM :lt_churn_w_clust;

-- Speichern in Tabelle
CREATE TABLE CLUST_RES_CHURN AS (
    SELECT * FROM :lt_churn_w_clust);

-- Ausgabe der Statistik (Slight Silhouette)
SELECT * FROM :lt_statistics;

-- Speichern des Modells in persistenter Tabelle
CREATE TABLE ML_DATA.PAL_KMEANS_MODEL AS (SELECT * FROM 
:lt_model);
