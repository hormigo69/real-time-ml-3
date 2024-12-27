Tengo un error en run.py de news-signal

    # Process the incoming news into a news signal
    sdf = sdf.apply(
        lambda value: {
            "news": value["title"],
            # "timestamp_ms": value["timestamp_ms"],  # added to fix the error 26/12 13:53
            **llm.get_signal(value["title"]),
            "model_name": llm.model_name,
        }
    )
si descomento esa línea me da un error al dockerizar el servicio.


2024-12-26 18:38:47 [2024-12-26 17:38:47,115] [ERROR] [quixstreams] : Failed to process a Row: partition="news[0]" offset="1162"
2024-12-26 18:38:47 Traceback (most recent call last):
2024-12-26 18:38:47   File "/app/.venv/lib/python3.10/site-packages/quixstreams/app.py", line 860, in _process_message
2024-12-26 18:38:47     context.run(
2024-12-26 18:38:47   File "/app/.venv/lib/python3.10/site-packages/quixstreams/core/stream/functions/apply.py", line 46, in wrapper
2024-12-26 18:38:47     child_executor(result, key, timestamp, headers)
2024-12-26 18:38:47   File "/app/.venv/lib/python3.10/site-packages/quixstreams/core/stream/functions/apply.py", line 45, in wrapper
2024-12-26 18:38:47     result = func(value)
2024-12-26 18:38:47   File "/app/run.py", line 38, in <lambda>
2024-12-26 18:38:47     "timestamp_ms": value["timestamp_ms"],  # added to fix the error 26/12 13:53
2024-12-26 18:38:47 KeyError: 'timestamp_ms'
2024-12-26 18:38:47 [2024-12-26 17:38:47,116] [WARNING] [quixstreams] : Application is stopping due to failure, latest checkpoint will not be committed.
2024-12-26 18:38:47 Traceback (most recent call last):
2024-12-26 18:38:47   File "/app/run.py", line 58, in <module>
2024-12-26 18:38:47     main(
2024-12-26 18:38:47   File "/app/run.py", line 48, in main
2024-12-26 18:38:47     app.run()
2024-12-26 18:38:47   File "/app/.venv/lib/python3.10/site-packages/quixstreams/app.py", line 731, in run
2024-12-26 18:38:47     self._run()
2024-12-26 18:38:47   File "/app/.venv/lib/python3.10/site-packages/quixstreams/app.py", line 770, in _run
2024-12-26 18:38:47     self._run_dataframe()
2024-12-26 18:38:47   File "/app/.venv/lib/python3.10/site-packages/quixstreams/app.py", line 794, in _run_dataframe
2024-12-26 18:38:47     self._process_message(dataframes_composed)
2024-12-26 18:38:47   File "/app/.venv/lib/python3.10/site-packages/quixstreams/app.py", line 860, in _process_message
2024-12-26 18:38:47     context.run(
2024-12-26 18:38:47   File "/app/.venv/lib/python3.10/site-packages/quixstreams/core/stream/functions/apply.py", line 46, in wrapper
2024-12-26 18:38:47     child_executor(result, key, timestamp, headers)
2024-12-26 18:38:47   File "/app/.venv/lib/python3.10/site-packages/quixstreams/core/stream/functions/apply.py", line 45, in wrapper
2024-12-26 18:38:47     result = func(value)
2024-12-26 18:38:47   File "/app/run.py", line 38, in <lambda>
2024-12-26 18:38:47     "timestamp_ms": value["timestamp_ms"],  # added to fix the error 26/12 13:53
2024-12-26 18:38:47 KeyError: 'timestamp_ms'

Solucionado calculando el timestamp_ms en el momento del procesamiento en services/news-signal/run.py:
Esta solución:

No depende de que el campo timestamp_ms exista en el mensaje
Calcula el timestamp de la misma manera que lo hace to_dict() en la clase News
Resuelve el error actual
(no lo he borrado de news porque no sé si va a funcionar)

    #This is the original code that is not working
    # At the end of session 6, Pau detect this error but decide to fix it later.
    # The code above calculates the timestamp_ms in the same way that the news data source does,
    # but I let it commented until to see wath Pau do with it.
    sdf = sdf.apply(
        lambda value: {
            "news": value["title"],
            **llm.get_signal(value["title"]),
            "model_name": llm.model_name,
            "timestamp_ms": value["timestamp_ms"],
        }
    )



________________________________________________________
