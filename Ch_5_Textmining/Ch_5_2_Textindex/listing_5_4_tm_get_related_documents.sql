SELECT * FROM TM_GET_RELATED_DOCUMENTS(
DOCUMENT IN FULLTEXT INDEX WHERE KEY = 13
SEARCH TEXT FROM ML_TEXT.NEWSCORP
RETURN TOP 10 
KEY, CATEGORY, TEXT) AS T