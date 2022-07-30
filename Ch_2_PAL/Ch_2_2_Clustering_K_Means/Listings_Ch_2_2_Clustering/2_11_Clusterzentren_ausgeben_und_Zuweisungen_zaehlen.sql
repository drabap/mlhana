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

