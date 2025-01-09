
# Status

Me he saltado la parte de entrenamiento del modelo (ver runpod.md) y voy a intentar retomar desde la exportación del modelo en local.
Luego ya veré si lo hago en la máquina de Runpod o sigo desde este punto


## Exporting the fine tune model
Esta parte corre también en el ordenador remoto. Lo dejo pendiente

Backfill pipeline for news - Part 8 - Making Ollama accessible to the Dockerized news signal service
- hay que conectar el docker de news-signal con ollama, pero en mac no se puede dockerizar, hay iun hack paa llamar a ollama desde el container de news-signal a través de localhost.
https://github.com/ollama/ollama/blob/main/docs/faq.md#how-do-i-configure-ollama-server
básicamente, consigues poder llamar a ollama desde la ip local.
launchctl setenv OLLAMA_HOST "0.0.0.0"
y reiniciar ollama después. Se prueba llamando desde el navegador a
ip_local:11434






Backfill pipeline for news - Part 9 - Docker compose file with the 3 services
6/1/25 20:15
- Funcionando el dockerizado de los tres servicios.
- Hopsworks recibe correctamente los datos de las señales de noticias.
- Haco el commit como



Backfill pipeline for news - Part 7 - Docker compose file with the 3 services
6/1/25 1:00
Vuelvo a intenatr el dockerizado de los tres servicios 12:45
Vamos a generar un docker que corra los tres servicios:
- leer las noticias de CryptoPanic, procesarlas y meterlas en Kafka
- Procesar las noticias usando ollama para extraer las señales y meterlas en Kafka
- leer las señales de Kafka y meterlas en un feature store




6/1/25 12:00
## Tengo un error que no soy capaz de solucionar. Vuelvo a la sesión 6 para asegurar el código
commit c3cd96ef76eabed3e8d2d95685ff1ee74e40ae73 (HEAD -> backfill-news-signals, origin/backfill-news-signals)
Author: Hormigo <hormigo@gmail.com>
Date:   Thu Jan 2 14:27:58 2025 +0100

    Fix output of historical data source

    We use the same News class as for live data fource.

Se corresponde con el vídeo Question -> How will we merge tech-indicators and news signals features? 1:32

Voy a crear una rama nueva con mi estado actual antes de volver al commit estable
  # 1. Crear una rama nueva con todo lo que tienes ahora
  git branch cambios-para-consultar

  # 2. Volver al commit estable
  git reset --hard c3cd96ef76eabed3e8d2d95685ff1ee74e40ae73

Después podré:
- Trabajar normalmente en mi rama actual (que estará en el commit estable)
- Consultar los cambios que hice usando:
    # Ver la otra rama
    git checkout cambios-para-consultar

    # Volver a tu rama principal
    git checkout backfill-news-signals

También puedo ver las diferencias entre ramas sin cambiar de rama:
  # Ver diferencias entre ramas
  git diff backfill-news-signals..cambios-para-consultar



OJO error y vuelvo a la versión estable
Backfill pipeline for news - Part 7 - Docker compose file with the 3 services
1/1/25 1:00
- Dockerizado pero con un error porque no ve ollama desde dentro del container.
- Yo teniá un error en el volumes, pero creo que lo he arrgaldo, aunque diferente de como lo hizo Pau.


Backfill pipeline for news - Part 6 - Reimplement historical news data source to match same format as live data
1/1/25 14:00
 - en este vídeo intentaremos debuguear la función de otra manera.
 - en principio funciona, pero al parar el servicio desde teclado me da un fallo. No le voy a dar importancia ahora porque
 se suben los datos a Kafka, pero ojo con esto.

Backfill pipeline for news - Part 5 - Reimplement historical news data source to match same format as live data
1/1/25 17:00
 - intentamos debuguear la función HistoricalNewsDataSource en el fichero historical_data_source.py, pero el
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
