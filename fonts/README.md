# Fuentes de la marca

Tipografía común de los productos de Lion Systems, alojada en el propio sitio
porque la CSP solo permite `font-src 'self'`.

| Archivo | Familia | Pesos | Subconjunto |
| --- | --- | --- | --- |
| `inter-latin.woff2` | Inter (variable) | 100–900 | latino (U+0000–00FF y signos comunes) |
| `plus-jakarta-sans-latin.woff2` | Plus Jakarta Sans (variable) | 600–800 | latino |

El subconjunto latino cubre el español completo (á, é, ñ, ü, ¿, ¡) y el inglés.

## Licencia

Ambas familias se distribuyen bajo la **SIL Open Font License 1.1**
(<https://openfontlicense.org>), que permite usarlas, incrustarlas y
redistribuirlas, siempre que no se vendan por separado.

- Inter — Copyright 2016 The Inter Project Authors (<https://github.com/rsms/inter>).
- Plus Jakarta Sans — Copyright 2020 The Plus Jakarta Sans Project Authors
  (<https://github.com/tokotype/PlusJakartaSans>).

Los archivos son los subconjuntos que sirve Google Fonts, sin modificar.

## Si se agrega una fuente

El despliegue copia archivo por archivo (`.github/workflows/deploy.yml`, en
las rutas de GitHub Pages y de GCP). `tests/test_recursos_referenciados.py`
falla si el CSS pide una fuente que no existe aquí o que el workflow no copia.
