# Listing: Verbindung zu HANA von Python
from hana_ml import dataframe

connection = dataframe.ConnectionContext( address = '<HOST>',
                                          port = '<PORT>',
                                          user = '<USER>')