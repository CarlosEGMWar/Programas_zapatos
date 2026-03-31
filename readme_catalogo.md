# Generador de Catálogos PDF — KLIN

## Descripción general

Este proyecto contiene **4 scripts Python** que generan catálogos PDF de calzado en formato A4, con diseño profesional (colores oscuros y dorado), usando la librería ReportLab. Cada script genera un tipo distinto de catálogo según el público destino:

| Script | PDF generado | Público |
|---|---|---|
| `crear_catalogo.py` | `catalogo.pdf` | Vendedores y revendedores internos |
| `crear_catalogo_revendedor_cliente.py` | `catalogo_revendedor.pdf` | Clientes finales (desde inventario CSV) |
| `catalogo_sin_inventario.py` | `catalogo_en_proceso.pdf` | Modelos en proceso (público general) |
| `catalogo_sin_inventario_revend_cliente.py` | `catalogo_en_proceso_cliente.pdf` | Clientes finales (modelos en proceso) |

---

## Requisitos previos

- **Python 3.8 o superior**
- Librerías necesarias: `reportlab` y `Pillow`

Para instalarlas, abrir una terminal y ejecutar:

```
pip install reportlab Pillow
```

---

## Estructura de carpetas que DEBEN existir

Los scripts esperan encontrar una estructura de carpetas específica. La carpeta raíz es `Zapatos/`, que debe estar **dos niveles arriba** de la carpeta donde están los scripts:

```
Zapatos/                                          ← carpeta raíz (ROOT_DIR)
│
├── Inventario/
│   ├── Inventario_web_precios_al_vendedor.csv    ← usado por crear_catalogo.py
│   └── Inventario_web_precios_cliente.csv        ← usado por crear_catalogo_revendedor_cliente.py
│
├── Ballerinas/                                   ← ejemplo de categoría
│   └── En Proceso/                               ← carpeta especial (scripts sin inventario)
│       ├── 19/                                   ← número SKU del modelo
│       │   └── HD/
│       │       ├── foto1.jpg
│       │       └── foto2.jpg
│       └── 40/
│           └── HD/
│               └── foto1.jpg
│
├── Botines Niñas/
│   └── En Proceso/
│       └── 180/
│           └── HD/
│               ├── foto1.jpg
│               └── foto2.jpg
│
├── [Cualquier otra categoría]/
│   ├── 123/                                      ← carpeta del modelo (SKU directa)
│   │   └── HD/
│   │       └── foto1.jpg
│   └── En Proceso/
│       └── 55/
│           └── HD/
│               └── foto1.jpg
│
└── Softwares/
    └── Crear_catalogo/                           ← carpeta donde están los scripts
        ├── crear_catalogo.py
        ├── crear_catalogo_revendedor_cliente.py
        ├── catalogo_sin_inventario.py
        └── catalogo_sin_inventario_revend_cliente.py
```

> **Importante:** Los nombres de las carpetas de categoría (por ejemplo, `Ballerinas`, `Botines Niñas`) deben coincidir exactamente con los valores en el CSV o con los nombres que los scripts corrigen automáticamente.

---

## Formato del CSV de inventario

*(Solo aplica a `crear_catalogo.py` y `crear_catalogo_revendedor_cliente.py`)*

El archivo CSV debe tener **encabezados en la primera fila** y las siguientes columnas obligatorias:

| Columna | Descripción |
|---|---|
| `ref_modelo` | Identificador del modelo. Puede ser `"123"` (un color) o `"123-456"` (dos colores). |
| `producto` | Nombre del producto para mostrar en el catálogo. |
| `precio_con_iva` | Precio a mostrar en el PDF. |
| `categoria_completa` | Categoría jerárquica, ej: `"Ballerinas > Niñas"`. |
| `color` | Color del modelo (ej: `"Negro"`, `"Rosado"`). |
| `talla` | Talla disponible (ej: `"22"`, `"25 - (32)"`). |
| `ref_combinacion` | Referencia numérica de la combinación color-talla (para ordenar los colores). |
| `url_producto` | URL de la tienda online (solo se usa en `crear_catalogo.py`). |
| `empeine` | Material del empeine (ficha técnica). |
| `forro_interior` | Material del forro interior (ficha técnica). |
| `suela` | Material de la suela (ficha técnica). |
| `fabricacion` | País o método de fabricación (ficha técnica). |
| `anatomico` | Si tiene soporte anatómico: `"Sí"` / `"No"`. |
| `antideslizante` | Si la suela es antideslizante: `"Sí"` / `"No"`. |
| `cierre` | Tipo de cierre (ej: `"Velcro"`, `"Elástico"`). |
| `composicion` | Composición de materiales. |
| `frecuencia_uso` | Frecuencia de uso recomendada. |
| `luces_leds` | Si tiene luces LED: `"Sí"` / `"No"`. |
| `alto_botin` | Alto del botín en cm (si aplica). |
| `alto_botas` | Alto de las botas en cm (si aplica). |

**Cada fila del CSV representa una combinación única de modelo + color + talla.**

Por ejemplo, un modelo con 2 colores y 5 tallas cada uno tendrá 10 filas en el CSV con el mismo `ref_modelo`.

El script detecta automáticamente si el archivo usa coma (`,`) o punto y coma (`;`) como separador, y prueba los encodings `utf-8-sig`, `utf-8` y `cp1252`.

---

## Los 4 scripts: cuándo usar cada uno

### 1. `crear_catalogo.py` → `catalogo.pdf`
**Para: vendedores y revendedores internos**

- Lee el CSV: `Inventario_web_precios_al_vendedor.csv` (precios al por mayor).
- Muestra: fotos por color, tallas disponibles como botones, ficha técnica completa, botón "Ver en tienda".
- **Chips de talla DORADOS** = hay stock en la tienda online → son links clickeables que van directo a comprar.
- **Chips de talla BLANCOS/GRISES** = sin stock en tienda online (no son clickeables).
- Botones de WhatsApp (con SKU en el mensaje), Instagram y Facebook.
- Índice jerárquico por categoría con links internos al PDF.

---

### 2. `crear_catalogo_revendedor_cliente.py` → `catalogo_revendedor.pdf`
**Para: clientes finales o revendedores sin acceso a la tienda online**

- Lee el CSV: `Inventario_web_precios_cliente.csv` (precios para cliente final).
- Muestra: fotos por color, tallas disponibles como chips, ficha técnica completa.
- **Todos los chips de talla son DORADOS** pero **sin links clickeables** (el cliente ve las tallas disponibles pero no puede comprar directamente desde el PDF).
- **Sin** botón "Ver en tienda".
- **Sin** botones de WhatsApp, Instagram ni Facebook.
- Índice jerárquico por categoría con links internos al PDF.

---

### 3. `catalogo_sin_inventario.py` → `catalogo_en_proceso.pdf`
**Para: modelos que aún no están en el inventario CSV ("En Proceso")**

- **No lee ningún CSV.** Detecta automáticamente las carpetas `En Proceso` en el árbol de directorios.
- Muestra: fotos del modelo, SKU (número de carpeta), categoría y precio.
- **Sin tallas** (los modelos aún no tienen stock definido).
- Botones clickeables: **WhatsApp** (consulta por tallas con SKU en el mensaje), **Instagram**, **Facebook**, **Ver Tienda**.
- Los precios se configuran manualmente en las tablas de precios al inicio del script.
- Índice por categoría con links internos.

---

### 4. `catalogo_sin_inventario_revend_cliente.py` → `catalogo_en_proceso_cliente.pdf`
**Para: clientes finales que consultan modelos en proceso, sin información de contacto**

- Igual al anterior pero **sin ningún botón ni link** de contacto o redes sociales.
- Muestra solo el texto **"Consultar stock de tallas"** como información.
- **Precios de reventa** (diferentes a los del catálogo público):

| Precio base | Precio de reventa |
|---|---|
| Bebés (cualquier precio) | $16.990 |
| $10.000 | $19.990 |
| $15.000 | $24.990 |
| $20.000 | $29.990 |

---

## Cómo configurar precios en los catálogos sin inventario

Al inicio de `catalogo_sin_inventario.py` y `catalogo_sin_inventario_revend_cliente.py` hay tablas de precios que se pueden editar:

```python
PRECIOS_BALLERINAS: dict = {
    19: 10000,   # SKU 19 → $10.000
    22: 10000,   # SKU 22 → $10.000
    40: 10000,   # SKU 40 → $10.000
}

PRECIOS_BOTINES_NINAS: dict = {
    180: 15000,  # SKU 180 → $15.000
    186: 10000,  # SKU 186 → $10.000
}
```

- La **clave** es el número de la carpeta (SKU), como número entero.
- El **valor** es el precio en pesos chilenos (CLP), como número entero.
- Si un SKU **no aparece en la tabla**, se usa el precio por defecto (`_PRECIO_DEFAULT`) para esa categoría.

Los precios por defecto son:

| Categoría | Precio por defecto |
|---|---|
| Ballerinas | $15.000 |
| Bebés | $10.000 |
| Botines | $15.000 |
| Botines Niñas | $20.000 |
| Zapatillas Niños | $15.000 |

> **Nota:** En `catalogo_sin_inventario_revend_cliente.py`, estos precios base se transforman automáticamente a precios de reventa mediante la función `transformar_precio()`. No es necesario cambiar los precios base para ajustar los precios de reventa.

---

## Cómo ejecutar los scripts

Abrir una terminal, navegar a la carpeta de los scripts y ejecutar el que corresponda:

```bash
cd Zapatos/Softwares/Crear_catalogo/

python crear_catalogo.py                            # genera catalogo.pdf
python crear_catalogo_revendedor_cliente.py         # genera catalogo_revendedor.pdf
python catalogo_sin_inventario.py                   # genera catalogo_en_proceso.pdf
python catalogo_sin_inventario_revend_cliente.py    # genera catalogo_en_proceso_cliente.pdf
```

El PDF se guarda en la misma carpeta donde están los scripts. Si ya existe un PDF con ese nombre, se sobreescribe.

Durante la ejecución, el script imprime en la consola cada producto que encuentra y procesa, facilitando identificar si algún modelo no se incluyó (por ejemplo, porque no tiene carpeta HD).

---

## Cómo agregar nuevos modelos "En Proceso"

Seguir estos pasos para que un nuevo modelo aparezca en `catalogo_en_proceso.pdf` y `catalogo_en_proceso_cliente.pdf`:

1. **Crear la carpeta de categoría** dentro de `Zapatos/` si no existe, por ejemplo: `Zapatos/Ballerinas/`.

2. **Crear la subcarpeta `En Proceso`** dentro de la categoría (exactamente con ese nombre y mayúsculas):
   ```
   Zapatos/Ballerinas/En Proceso/
   ```

3. **Crear una carpeta con el número SKU** del nuevo modelo dentro de `En Proceso`:
   ```
   Zapatos/Ballerinas/En Proceso/55/
   ```

4. **Crear la carpeta `HD`** dentro del SKU y poner ahí las fotos (`.jpg`, `.png` o `.jpeg`):
   ```
   Zapatos/Ballerinas/En Proceso/55/HD/
       foto1.jpg
       foto2.jpg
   ```

5. **Agregar el precio en la tabla** correspondiente al inicio del script (si el precio es diferente al por defecto). Por ejemplo, en `catalogo_sin_inventario.py`, dentro de `PRECIOS_BALLERINAS`:
   ```python
   PRECIOS_BALLERINAS: dict = {
       19: 10000,
       55: 12000,   # ← nuevo modelo SKU 55 con precio $12.000
   }
   ```

6. **Ejecutar el script** para generar el PDF actualizado.

---

## Diseño visual

Todos los catálogos comparten la misma paleta de colores y estilo:

| Elemento | Color | Código hexadecimal |
|---|---|---|
| Fondo oscuro (header, portada) | Azul marino oscuro | `#1B2A3B` |
| Acento dorado (precios, botones, chips) | Dorado | `#C9A050` |
| Texto de etiquetas (ficha técnica) | Gris medio | `#4A5568` |
| Fondos suaves (badges de color) | Gris muy claro | `#EDF2F7` |
| Líneas separadoras | Gris claro | `#CBD5E0` |
| Fondo dorado suave (índice) | Crema dorado | `#FDF3DC` |

**Tamaño de página:** A4 (210 × 297 mm).
**Modelos por página:** máximo 2 (los scripts de inventario pueden colocar 1 si el modelo tiene muchos colores o fotos).
**Fotos por fila:** 3 (disposición en cuadrícula).
