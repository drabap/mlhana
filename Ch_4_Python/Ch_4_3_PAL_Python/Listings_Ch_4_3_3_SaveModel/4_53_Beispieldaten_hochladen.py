# Beispieldaten hochladen
import pandas as pd

# Pandas Dataframe mit neuen Kundendaten erstellen
l_pd_new_customer = pd.DataFrame(
    { 'CUSTOMERID' : [20000001,20000002],
        'CREDITSCORE' : [500,450],
        'GEOGRAPHY' : ["Germany","France"],
        'GENDER' : ["Male","Female"],
        'AGE' : [40,70],
        'TENURE' : [8,4],
        'BALANCE' : [84000.00, 72000.00],
        'NUMOFPRODUCTS' : [2,3],
        'HASCRCARD' : [1,0],
        'ISACTIVEMEMBER' : [1,1],
        'ESTIMATEDSALARY' : [90000.00,70000.00]
    }, index = [1,2])

# In neue Tabelle speichern für PREDICT
l_df_new_cust = dataframe.create_dataframe_from_pandas(
    connection_context = connection,
    pandas_df = l_pd_new_customer,
    table_name = 'NEW_CUSTOMER_PREDICT',
    schema = 'ML_DATA',
    primary_key = 'CUSTOMERID',
    drop_exist_tab = True,
    force = True )
