"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```

    """
    import os
    import zipfile
    import pandas as pd

    # 1) DESCOMPRIMIR el ZIP si aún no se ha extraído
    #    El ZIP ya contiene la carpeta "input/" adentro, así que extraemos
    #    a la RAÍZ del proyecto (no a "input") para que quede input/train/...
    zip_path = "files/input.zip"
    if not os.path.isdir("input/train/positive"):
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(".")

    # 2) Crear la carpeta de salida files/output/
    os.makedirs("files/output", exist_ok=True)

    # 3) Para cada split (train y test), recorrer las carpetas de sentiment
    #    y armar un DataFrame con (phrase, target)
    resultados = {}
    for split in ["train", "test"]:
        filas = []
        split_dir = os.path.join("input", split)

        # Recorremos las 3 carpetas de sentiment en un orden estable
        for sentiment in ["negative", "positive", "neutral"]:
            sentiment_dir = os.path.join(split_dir, sentiment)

            # Si la carpeta no existe (puede pasar si el ZIP tiene otra estructura), la saltamos
            if not os.path.isdir(sentiment_dir):
                continue

            # Listamos los archivos .txt ordenados alfabéticamente
            for filename in sorted(os.listdir(sentiment_dir)):
                if not filename.endswith(".txt"):
                    continue

                # Leemos el contenido del archivo y le quitamos espacios/saltos al borde
                filepath = os.path.join(sentiment_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    phrase = f.read().strip()

                filas.append({"phrase": phrase, "target": sentiment})

        # Construimos el DataFrame y lo guardamos como CSV
        df = pd.DataFrame(filas)
        output_path = os.path.join("files", "output", f"{split}_dataset.csv")
        df.to_csv(output_path, index=False)
        resultados[split] = df

    return resultados
