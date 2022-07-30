SELECT exited, gb_decision_exited,
    COUNT(*) as count FROM CHURN_APPLY
    GROUP BY exited, gb_decision_exited
    ORDER BY exited, gb_decision_exited;
