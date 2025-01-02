
# Status

Me he saltado la parte de entrenamiento del modelo (ver runpod.md) y voy a intentar retomar desde la exportación del modelo en local.
Luego ya veré si lo hago en la máquina de Runpod o sigo desde este punto


## Exporting the fine tune model
Esta parte corre también en el ordenador remoto. Lo dejo pendiente

Backfill pipeline for news - Part 6 - Reimplement historical news data source to match same format as live data
1/1/25
 - en este vídeo intentaremso debuguear la fucnión de otra manera.

Backfill pipeline for news - Part 5 - Reimplement historical news data source to match same format as live data
1/1/25 17:00
 - intentamos debuguear la fucnión HistoricalNewsDataSource en el fichero historical_data_source.py, pero el
 breakpoint da un problema.


Backfill pipeline for news - Part 4 - Updating the news-signal service
1/1/25 16:00
- creamos settings para live e historical data source

## Backfill pipeline for news - Part 3 - Adjust news-signal service
31/12/24 10:00

 - ojo, no estoy trayendo timestamp_ms de news, lo calculo en la línea 13 de run.py. No sé si esto me va a dar problemas (9:38 del vídeo)


## Backfill pipeline for news - Part 2- Creating data source for historical news
30/12/24 09:45
- He creado ya el data source para el historial de noticias. Lee de noticias live de CryptoPanic y de un fichero CSV para el backfill.
- Código por mi cuenta para bajar el rar, descomprimirlo, extraer el csv y meterlo en el directorio sources/data
- Subido a la rama de git >backfill-news-signals


## Backfill pipeline for news - Part 1 - Creating data source for historical news
28/12/24 18:30
- creamos una rama nueva en git en local para el backfill (git checkout -b "backfill-news-signals")
- Pau no se emte en bajar el fichero de manera programática desde el repositorio de CryptoNewsDataset, pero yo ya lo tengo hecho en historical_data_source.py.
    - lo descargo en temp/download/cryptopanic_news.csv
    - guardo el path en path_to_csv_file

  -  lo subo a github
