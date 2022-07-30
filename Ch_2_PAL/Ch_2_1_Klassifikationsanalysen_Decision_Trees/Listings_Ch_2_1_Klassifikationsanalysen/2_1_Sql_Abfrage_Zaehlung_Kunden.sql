-- SQL-Abfrage zur Zählung der Kunden nach EXITED
SELECT EXITED, count(*) FROM CHURN GROUP BY EXITED