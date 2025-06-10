# Sistema de Recomendación de Libros con Clusterización (K-Means)

Este proyecto implementa una librería modular en Python para recomendar libros usando clustering jerárquico (K-Means dentro de K-Means). Ideal para plataformas de e-commerce de libros como "Relatos de Papel".

## Estructura de módulos
- `preprocessing`: limpieza y transformación de datos
- `clustering`: agrupamiento jerárquico de usuarios
- `api_enricher`: integración de metadatos externos
- `recommender`: generación de recomendaciones
- `utils`: reportes y validaciones

## Configuración del entorno virtual

1. Abre una terminal en la raíz del proyecto.
2. Crea el entorno virtual con:
   ```bash
   python3 -m venv .venv
   ```
3. Activa el entorno virtual:
   ```bash
   source .venv/bin/activate
   ```
4. Instala las dependencias necesarias (si tienes un archivo `requirements_clean.txt`):
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución del archivo principal

Para ejecutar el archivo principal `AIL_Library/main.py`, usa uno de los siguientes comandos desde la raíz del proyecto:

```bash
python -m AIL_Library.main
```
o

```bash
python AIL_Library/main.py
```

