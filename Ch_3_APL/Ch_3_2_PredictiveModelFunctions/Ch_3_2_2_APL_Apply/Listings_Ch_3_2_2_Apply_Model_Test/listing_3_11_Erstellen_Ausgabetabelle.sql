-- Ausgabe der Prognose
-- Je nach Parameterwert APL/ApplyExtraMode
-- Vor zweiter Ausführung: Tabelle löschen
-- DROP TABLE CHURN_APPLY;
CREATE COLUMN TABLE CHURN_APPLY(
    CUSTOMERID INTEGER,
    EXITED INTEGER,
    -- ApplyExtraMode Decision
    GB_DECISION_EXITED BIGINT
    -- ApplyExtraMode Score
    -- GB_SCORE_EXITED double
    -- ApplyExtraMode Probability
    -- GB_PROBA_EXITED double
);