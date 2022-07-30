# Dataframe aus SQL
connection.sql("""SELECT * FROM SYS.M_TABLES 
WHERE SCHEMA_NAME = 'ML_DATA' """).collect()
