# NBAReference Stats Scraper

## Instalación
Los prerrequisitos y sus versiones vienen especificados en el fichero `requirements.txt` y se pueden instalar de manera conjunta mediante el comando
```bash
pip install -r requirements.txt
```

## Ejecución
Para ejecutar el programa se debe comprobar que existe una conexión activa a internet y usaremos el script `scraper.py`.
```bash
python scraper.py
```
Si la ejecución es correcta se mostrará en consola el mensaje `200 OK` y, de lo contrario, un mensaje de error especificando el [código de error HTTP](https://httpstatuses.com/) que ha recibido de la petición a la web.

## Fichero de salida
El resultado del proceso de web scraping se almacenará en un fichero de salida llamado `nba.csv`.

Para más información, puedes consultar la Wiki de este repositorio.
