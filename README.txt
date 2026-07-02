Para que funcione spacy:
> spacy download es_core_news_lg
Pesa alrededor de 700MB
    Sino, se pueden descargar modelos más pequeños cambiando las últimas 2 letras: es_core_news_md (medio), 
                                                                                   es_core_news_sm (chico).

RAW/ contiene el agente sin UI, es la lógica que creamos.
    Los "datos de usuario" no se influyen en el trabajo que realiza el modelo.
En UI/ usamos IA para que nos genere un HTML basándose en RAW/:
    En TEMPLATES/ esta el HTML.
    En server.py esta toda la lógica del agente.
    "respuestas.json" es el diccionario de sugerencias que devuelve el agente.

El trabajo consiste en crear una especie de mesa de ayuda. 
Con Leonel Encina elegimos el rubro de la salud.
El agente tiene que recibir una consulta y tiene que DEFINIR qué parte de la organización se encarga de esa consulta,
también tiene que ASIGNAR un nivel de prioridad a la consulta, y por último tiene que SUGERIR qué hacer.

Al final hay que guardar el proceso entero en un .json que debe contener por lo menos: consulta, área encargada, prioridad, y respuesta del agente; como un historial de tickets.