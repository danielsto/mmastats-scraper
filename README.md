# NBA Talent Scraper

## Instalación

Los prerrequisitos y sus versiones vienen especificados en el fichero `requirements.txt` y se pueden instalar de manera conjunta mediante el comando. Este script usa características de Python 3.5+, lo que hace necesaria la instalación de esta versión del lenguaje Python y no la 2.7, ya deprecada.

```bash
$ pip3 install -r requirements.txt
```

## Ejecución

Para ejecutar el programa se debe comprobar que existe una conexión activa a internet y usaremos el script `main.py`.

```bash
$ python3 main.py [-mode full | simple] [-league nba | aba | baa]
```

La ejecución completa del script para obtener el dataset más completo es la siguiente:

```bash
$ python3 main.py
```

> **Nota**: La ejecución completa puede llevar unos segundos. Se han introducido instrucciones `print` en el script para que se pueda ver el progreso de las temporadas (registros) extraídos. El intervalo es de 2019-20 a la 1947-48.

Para más información sobre los argumentos opcionales:

```bash
$ python3 main.py -h
```

Si la ejecución es correcta se mostrará en consola el mensaje `200 OK` y, de lo contrario, un mensaje de error especificando el [código de error HTTP](https://httpstatuses.com/) que ha recibido de la petición a la web.

## Tests

El directorio `tests` contiene dos ficheros de testing básicos. Para ejecutar los tests hay que ejecutar el siguiente comando:

```bash
$ pytest
```

## Fichero de salida

El resultado del proceso de web scraping se almacenará en un fichero de salida llamado `nba_talent.csv`.

Para más información y detalles de este proyecto, puedes consultar la [Wiki](https://github.com/danielsto/nba-reference-scraper/wiki) de este repositorio.

## Dataset

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4261333.svg)](https://doi.org/10.5281/zenodo.4261333)
