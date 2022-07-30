from hana_ml.algorithms.pal.tsne import TSNE

tsne = TSNE( n_iter = 500,
    random_state = 1,
    n_components = 3,
    angle = 0.0,
    exaggeration = 20,
    learning_rate = 200,
    perplexity = 30,
    object_frequency = 50,
    thread_ratio = 0.5 )

df_tsne_res, stats, obj = tsne.fit_predict(
    data = topics_pivot,
    key = 'KEY' )

df_tsne_res.collect()