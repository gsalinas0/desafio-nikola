# Relleno de Formulario Nikola automático
Script para rellenar el formulario de Nikola de manera automática. El script está hecho en Python en un entorno virtual utilizando Selenium.

## Requisitos
- Python 3.10
- Tener una versión de Chrome instalada
- **Importante**: El script está pensado para ejecutarse en Windows.

## SetUp del proyecto

1. Crear el entorno virtual
```
python -m venv venv
```

2. Instalar las dependencias
```
pip install -r requirements.txt
```

3. Activar el entorno virtual
```
.\venv\Scripts\activate
```

4. Desactivar el entorno virtual
```
deactivate
```

## Ejecución
Para ejecutar el script, se debe correr el siguiente comando:
```
python3 main.py
```
## Tomar en cuenta
- El script está configurado para que se ejecute en Chrome.
- Podrían llegar a arrojarse excepciones si el formulario tarda mucho tiempo en cargar
- Los datos se cargan desde el archivo `data/database.csv`. Para la parte de subir el archivo, se debe escribir el nombre del archivo (o su ruta relativa) y guardarlo en la carpeta `data/uploadFiles`. *Por ejemplo, si el archivo se llama `luis.pdf` se debe escribir `luis.pdf` y guardarlo en la carpeta `data/uploadFiles`*. Se asume que los archivos siempre estarán en la carpeta

## Supuestos
- Se asume que todos los datos que irán en el csv serán correctos. *Por ejemplo, en los selectores solo se tendremos opciones válidas*, aunque no siempre se ocuparán todos los campos. *Por ejemplo si el tipo de instalación es "Suelo" no usaremos el campo de inclinación*.
