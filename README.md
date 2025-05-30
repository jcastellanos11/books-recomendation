# README.md
# Sistema de Recomendación de Libros con Clusterización (K-Means)

Este proyecto implementa una librería modular en Python para recomendar libros usando clustering jerárquico (K-Means dentro de K-Means). Ideal para plataformas de e-commerce de libros como "Relatos de Papel".

## Estructura de módulos
- `preprocessing`: limpieza y transformación de datos
- `clustering`: agrupamiento jerárquico de usuarios
- `api_enricher`: integración de metadatos externos
- `recommender`: generación de recomendaciones
- `utils`: reportes y validaciones

## Cómo iniciar
```bash
python AIL_Library/main.py
```

project/
├── AIL_Library/
│   ├── __init__.py
│   ├── preprocessing.py  # Cargar datos y limpieza básica
│   ├── clustering.py     # KMeans jerárquico
│   ├── api_enricher.py   # Enriquecimiento con APIs
│   ├── recommender.py    # Sistema de recomendación
│   ├── utils.py          # Reportes, logs y validaciones
│   └── main.py           # Orquestador
├── data/
│   └── sample_users_books.json
├── notebooks/
│   └── exploration.ipynb
├── requirements.txt
└── README.md