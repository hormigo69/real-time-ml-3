
# Status

Me he saltado la parte de entrenamiento del modelo (ver runpod.md) y voy a intentar retomar desde la exportación del modelo en local.
Luego ya veré si lo hago en la máquina de Runpod o sigo desde este punto


## Exporting the fine tune model
Esta parte corre también en el ordenador remoto. Lo dejo pendiente



## Backfill pipeline for news - Part 1 - Creating data source for historical news

- creamos una rama nueva en got en local para el backfill (git checkout -b "backfill-news-signals")
- Pau no se emte en bajar el fichero de manera programática desde el repositorio de CryptoNewsDataset, pero yo ya lo tengo hecho en historical_data_source.py.
    - lo descargo en temp/download/cryptopanic_news.csv
    - guardo el path en path_to_csv_file

28/12/24 18:30  - de momento lo dejo aquí, lo subo a github
