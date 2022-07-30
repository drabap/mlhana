topics_pivot = df.pivot_table( columns = 'TOPIC_ID',
    values = 'PROBABILITY',
    index = 'KEY',
    aggfunc = 'AVG')

topics_pivot.collect()