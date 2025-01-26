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
## Consideraciones
- El script está configurado para que se ejecute en Chrome.
- Se asume que todos los datos que irán en el csv serán correctos. *Por ejemplo, en los selectores solo tendremos opciones válidas*.
- No siempre se ocuparán todos los campos. *Por ejemplo si el tipo de instalación es "Suelo" no usaremos el campo de inclinación*. Es posible no ingresar datos en un campo si no se va a ocupar.
- Los datos se cargan desde el archivo `data/database.csv`. 

| name | email | phone | address | structureType | roofInclination | roofType | accountCost | reference | fileRoute |
|------|--------|-------|----------|--------------|-----------------|----------|-------------|-----------|-----------|
| Luis Hernandez | luis.hernandez@gmail.com | 912345678 | Avenida Chile España 105 Ñuñoa | Techo | Plano | Teja Asfáltica | 100000 | Google | luis.pdf |

* Si en roofType se especifica "Otro", se debe especificar el material seguido de un "-".

En fileRoute se debe especificar el nombre del archivo a subir, y colocarlo en la carpeta `data/uploadFiles`. Para efectos de llenado del formulario se asumirá que el archivo existe. Si no se llena este campo, se asumirá que no se subirá ningún archivo.
- Con respecto al slider, se ubicará en la posición más cercana al valor de accountCost.
