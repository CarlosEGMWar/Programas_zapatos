"""
Generador de catalogo PDF para zapatos EN PROCESO — version revendedor/cliente final.

Publico objetivo: clientes finales o revendedores que consultan modelos en proceso,
sin acceso a informacion de contacto interno ni enlaces a redes sociales.

Diferencias clave respecto a catalogo_sin_inventario.py (version con botones):
- Sin botones de WhatsApp, Instagram, Facebook ni Ver Tienda.
- En lugar de la barra de botones, muestra solo el texto "Consultar stock de tallas"
  en dorado sobre fondo gris suave (funcion dibujar_barra_consulta).
- Precios ajustados para reventa mediante la funcion transformar_precio():
    * Bebés (todas las tallas):  precio base -> $16.990
    * Precio base $10.000        -> $19.990
    * Precio base $15.000        -> $24.990
    * Precio base $20.000        -> $29.990
- La barra de consulta es mas pequena (BTN_BAR_H = 8 mm vs 16 mm) al no tener botones.

Caracteristicas compartidas con catalogo_sin_inventario.py:
- No usa ningun CSV de inventario.
- Detecta carpetas 'En Proceso' automaticamente en ROOT_DIR.
- Maximo 2 modelos por pagina; nueva pagina al cambiar de categoria.
- Fotos + SKU + categoria + precio en cada bloque.
- Indice por categoria con links internos al PDF.

Archivo de salida: catalogo_en_proceso_cliente.pdf (en la misma carpeta que este script)
"""

import io
import os
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

# ── Rutas ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent.parent       # .../Zapatos
OUTPUT_PDF = SCRIPT_DIR / "catalogo_en_proceso_cliente.pdf"

# ── Correcciones de nombre de categoria ───────────────────────────────────────
_CORR = {
    "ninos":   "Niños",
    "ninas":   "Niñas",
    "nino":    "Niño",
    "nina":    "Niña",
    "bebes":   "Bebés",
    "bebe":    "Bebé",
    "zapatillas ninos": "Zapatillas Niños",
    "botines ninas":    "Botines Niñas",
}

def corregir_nombre(s: str) -> str:
    """
    Corrige tildes y caracteres especiales en nombres de categoria.

    Los nombres de carpeta en el sistema de archivos suelen carecer de tildes
    (por compatibilidad), por ejemplo "Ninos" en lugar de "Niños". Esta funcion
    consulta el diccionario _CORR para aplicar las correcciones conocidas y,
    si el nombre no esta en el diccionario, aplica title() para capitalizar.

    Parametros:
        s (str): Nombre de la carpeta tal como aparece en el sistema de archivos.

    Devuelve:
        str: Nombre corregido con tildes y caracteres especiales (ej: 'Niños', 'Bebés').
    """
    key = s.strip().lower()
    if key in _CORR:
        return _CORR[key]
    return s.strip().title()

# ── Tablas de precios base (iguales al catalogo original) ─────────────────────

PRECIOS_BALLERINAS: dict = {
    19:10000,
    22:10000,
    40:10000,
}

PRECIOS_BEBES: dict = {
}

PRECIOS_BOTINES: dict = {
}

PRECIOS_BOTINES_NINAS: dict = {
    180:15000,
    186:10000,
    187:15000,
    188:15000,
    194:15000,
}

PRECIOS_ZAPATILLAS_NINOS: dict = {
}

_PRECIO_DEFAULT: dict = {
    "Ballerinas":       15000,
    "Bebés":            10000,
    "Botines":          15000,
    "Botines Niñas":    20000,
    "Zapatillas Niños": 15000,
}

_PRECIO_TABLA: dict = {
    "Ballerinas":       PRECIOS_BALLERINAS,
    "Bebés":            PRECIOS_BEBES,
    "Botines":          PRECIOS_BOTINES,
    "Botines Niñas":    PRECIOS_BOTINES_NINAS,
    "Zapatillas Niños": PRECIOS_ZAPATILLAS_NINOS,
}

_PRECIO_REVENTA: dict = {
    10000: 19990,
    15000: 24990,
    20000: 29990,
}


def transformar_precio(categoria: str, precio_base: int) -> int:
    """
    Convierte un precio base al precio de reventa correspondiente para el cliente final.

    Aplica la tabla de conversion _PRECIO_REVENTA segun las siguientes reglas:
    - Si la categoria es 'Bebes': devuelve siempre $16.990, sin importar el precio base.
    - Para las demas categorias, usa el diccionario _PRECIO_REVENTA:
        * $10.000 base -> $19.990
        * $15.000 base -> $24.990
        * $20.000 base -> $29.990
    - Si el precio base no esta en el diccionario, lo devuelve sin cambios.

    Esta funcion es exclusiva de esta version revendedor/cliente y no existe
    en catalogo_sin_inventario.py (version publica).

    Parametros:
        categoria (str): Nombre de la categoria corregido (ej: 'Bebés', 'Botines Niñas').
        precio_base (int): Precio original en CLP antes de la transformacion de reventa.

    Devuelve:
        int: Precio de reventa en CLP para mostrar al cliente final.
    """
    if categoria == "Bebés":
        return 16990
    return _PRECIO_REVENTA.get(precio_base, precio_base)


def obtener_precio(categoria: str, sku: str) -> int:
    """
    Devuelve el precio de reventa en pesos chilenos (CLP) para un producto.

    A diferencia de catalogo_sin_inventario.py, esta funcion aplica un paso
    adicional de transformacion: tras obtener el precio base de las tablas
    PRECIOS_*, llama a transformar_precio() para convertirlo al precio de
    reventa antes de devolverlo.

    Flujo:
    1. Busca el SKU (como entero) en la tabla especifica de la categoria.
    2. Si no esta, usa el precio por defecto de _PRECIO_DEFAULT para esa categoria.
    3. Pasa el precio base a transformar_precio() para obtener el precio de reventa.

    Parametros:
        categoria (str): Nombre de la categoria ya corregido (ej: 'Botines Niñas').
        sku (str): Numero de carpeta del modelo (ej: '180').

    Devuelve:
        int: Precio de reventa en CLP listo para mostrar en el catalogo.
             Devuelve 0 si no se puede determinar el precio base.
    """
    tabla = _PRECIO_TABLA.get(categoria, {})
    try:
        precio_base = tabla.get(int(sku), _PRECIO_DEFAULT.get(categoria, 0))
    except (ValueError, TypeError):
        precio_base = _PRECIO_DEFAULT.get(categoria, 0)
    return transformar_precio(categoria, precio_base)

# ── Paleta ────────────────────────────────────────────────────────────────────
C_DARK   = colors.HexColor("#1B2A3B")
C_ACCENT = colors.HexColor("#C9A050")
C_MID    = colors.HexColor("#4A5568")
C_LIGHT  = colors.HexColor("#EDF2F7")
C_WHITE  = colors.white
C_LINE   = colors.HexColor("#CBD5E0")

# ── Layout ────────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN  = 10 * mm
HDR_H   = 14 * mm
GAP_BLK = 5  * mm

N_FOTO     = 3
FOTO_GAP   = 0.5 * mm
GRP_GAP    = 1.0 * mm
PHOTO_W    = (PAGE_W - 2 * MARGIN - (N_FOTO - 1) * FOTO_GAP) / N_FOTO
BTN_BAR_H  = 8 * mm                              # barra reducida solo con texto
BLK_PAD    = HDR_H + BTN_BAR_H + 5 * mm

MAX_BLK_H     = (PAGE_H - 2 * MARGIN - GAP_BLK) / 2
MAX_CONTENT_H = MAX_BLK_H - BLK_PAD

# ─────────────────────────────────────────────────────────────────────────────
# BUSQUEDA DE PRODUCTOS
# ─────────────────────────────────────────────────────────────────────────────

def buscar_productos() -> list:
    """
    Recorre el arbol de directorios buscando carpetas 'En Proceso' con productos.

    Identica en logica a catalogo_sin_inventario.py, pero obtener_precio()
    ya aplica la transformacion de reventa, por lo que los precios devueltos
    son los precios finales para el cliente (no los precios base).

    Para cada carpeta llamada exactamente 'En Proceso' encontrada dentro de ROOT_DIR:
    - Determina la categoria a partir del nombre de la carpeta padre y la corrige
      aplicando corregir_nombre() para obtener tildes correctas.
    - Itera sobre las subcarpetas dentro de 'En Proceso' (cada una es un SKU).
    - Para cada subcarpeta que contenga una carpeta 'HD' con al menos una imagen
      valida, crea un dict de producto y lo agrega a la lista.

    La lista resultante se ordena por categoria y luego por SKU numerico.

    Devuelve:
        list[dict]: Lista de dicts de producto ordenada, cada uno con claves:
                    - 'sku' (str): Nombre de la subcarpeta (numero del modelo).
                    - 'categoria' (str): Nombre de categoria corregido.
                    - 'imgs' (list[Path]): Lista ordenada de rutas a las fotos.
                    - 'precio' (int): Precio de REVENTA en CLP (ya transformado).
    """
    productos = []
    for dirpath, dirnames, _ in os.walk(ROOT_DIR):
        dirnames.sort()
        if "En Proceso" in dirnames:
            en_proceso = Path(dirpath) / "En Proceso"
            categoria_raw = Path(dirpath).name
            categoria = corregir_nombre(categoria_raw)

            for entry in sorted(en_proceso.iterdir()):
                if not entry.is_dir():
                    continue
                sku = entry.name.strip()
                hd  = entry / "HD"
                if not hd.is_dir():
                    continue
                imgs = sorted(
                    p for p in hd.iterdir()
                    if p.suffix.lower() in (".png", ".jpg", ".jpeg")
                )
                if not imgs:
                    continue
                productos.append({
                    "sku":       sku,
                    "categoria": categoria,
                    "imgs":      imgs,
                    "precio":    obtener_precio(categoria, sku),
                })
                print(f"  OK  {categoria:<25}  SKU: {sku:<6}  {len(imgs)} fotos")

    def sort_key(p):
        """Clave de ordenamiento: (categoria, sku_numerico_o_texto)."""
        try:
            return (p["categoria"], int(p["sku"]))
        except ValueError:
            return (p["categoria"], p["sku"])

    return sorted(productos, key=sort_key)

# ─────────────────────────────────────────────────────────────────────────────
# PROCESAMIENTO DE IMAGENES
# ─────────────────────────────────────────────────────────────────────────────

_img_cache: dict = {}

def preparar_imagen(img_path: Path, max_px: int = 350):
    """
    Prepara una imagen para incrustarla en el PDF, con cache para evitar relecturas.

    Realiza tres operaciones en secuencia:
    1. Aplanar transparencia: PNG con canal alfa -> composicion sobre fondo blanco.
    2. Redimensionar: reduce a max_px en la dimension mayor con algoritmo LANCZOS.
    3. Convertir a JPEG: guarda en buffer con calidad 60 para reducir peso del PDF.

    Las imagenes procesadas se almacenan en _img_cache con la clave (ruta, max_px).

    Parametros:
        img_path (Path): Ruta al archivo de imagen original (.png, .jpg o .jpeg).
        max_px (int): Dimension maxima en pixeles tras redimensionar. Por defecto 350 px.

    Devuelve:
        tuple: (ImageReader, ancho_px, alto_px) listo para pasar a canvas.drawImage().
    """
    cache_key = (str(img_path), max_px)
    if cache_key in _img_cache:
        return _img_cache[cache_key]
    with PILImage.open(img_path) as im:
        if im.mode in ("RGBA", "LA"):
            bg = PILImage.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        elif im.mode == "P" and "transparency" in im.info:
            im = im.convert("RGBA")
            bg = PILImage.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
        im.thumbnail((max_px, max_px), PILImage.LANCZOS)
        w, h = im.size
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=60, optimize=True)
        buf.seek(0)
    result = (ImageReader(buf), w, h)
    _img_cache[cache_key] = result
    return result


def dibujar_imagen(c: canvas.Canvas, img_path: Path, x, y, w, h):
    """
    Dibuja una imagen centrada dentro de un rectangulo dado, respetando proporciones.

    Calcula la escala maxima que permite que la imagen quepa completamente dentro
    del rectangulo sin deformarla. La imagen se centra horizontal y verticalmente.

    Si ocurre cualquier error al cargar o dibujar la imagen, imprime una advertencia
    en consola y continua sin interrumpir la generacion del PDF.

    Parametros:
        c (canvas.Canvas): Lienzo PDF de ReportLab sobre el que dibujar.
        img_path (Path): Ruta al archivo de imagen a dibujar.
        x (float): Coordenada X de la esquina inferior izquierda del rectangulo (en puntos).
        y (float): Coordenada Y de la esquina inferior izquierda del rectangulo (en puntos).
        w (float): Ancho del rectangulo disponible (en puntos).
        h (float): Alto del rectangulo disponible (en puntos).
    """
    try:
        img_reader, iw, ih = preparar_imagen(img_path)
        ratio = min(w / iw, h / ih)
        dw, dh = iw * ratio, ih * ratio
        cx = x + (w - dw) / 2
        cy = y + (h - dh) / 2
        c.drawImage(img_reader, cx, cy, dw, dh)
    except Exception as e:
        print(f"  [WARN] {img_path.name}: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS DE DIBUJO
# ─────────────────────────────────────────────────────────────────────────────

def rounded_rect(c, x, y, w, h, r=2*mm, fill=None, stroke=None, lw=0.4):
    """
    Dibuja un rectangulo con esquinas redondeadas en el lienzo PDF.

    En esta version revendedor/cliente se usa principalmente para la barra
    de consulta (dibujar_barra_consulta) y otros elementos decorativos.
    No se usa para botones externos ya que esta version no tiene links.

    Parametros:
        c (canvas.Canvas): Lienzo PDF de ReportLab.
        x (float): Coordenada X de la esquina inferior izquierda (en puntos).
        y (float): Coordenada Y de la esquina inferior izquierda (en puntos).
        w (float): Ancho del rectangulo (en puntos).
        h (float): Alto del rectangulo (en puntos).
        r (float): Radio de curvatura de las esquinas. Por defecto 2 mm.
        fill: Color de relleno (objeto ReportLab Color). None para sin relleno.
        stroke: Color del borde. None para sin borde.
        lw (float): Grosor de la linea de borde en puntos. Por defecto 0.4.
    """
    if fill:
        c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    p = c.beginPath()
    p.roundRect(x, y, w, h, r)
    c.drawPath(p, fill=1 if fill else 0, stroke=1 if stroke else 0)

# ─────────────────────────────────────────────────────────────────────────────
# ALTURA DE BLOQUE
# ─────────────────────────────────────────────────────────────────────────────

def calcular_ph(n_imgs: int) -> float:
    """
    Calcula la altura optima de cada foto para que el bloque no supere MAX_BLK_H.

    Determina cuantas filas de fotos necesita el producto y calcula la altura
    maxima por foto tal que toda la cuadricula quepa dentro de MAX_CONTENT_H.
    Limita ademas la altura a PHOTO_W (tamano cuadrado de referencia).

    Nota: en esta version BTN_BAR_H = 8 mm (solo texto, sin botones), por lo que
    el area disponible para fotos es mayor que en catalogo_sin_inventario.py
    (donde BTN_BAR_H = 16 mm con 4 botones).

    Parametros:
        n_imgs (int): Numero total de imagenes del producto.

    Devuelve:
        float: Altura de foto en puntos, <= PHOTO_W.
    """
    n_rows = max(1, -(-n_imgs // N_FOTO))
    ph_max = (MAX_CONTENT_H - (n_rows - 1) * FOTO_GAP) / n_rows
    return min(PHOTO_W, ph_max)


def calcular_bloque_h(n_imgs: int) -> float:
    """
    Calcula la altura total del bloque de un producto, garantizando que cabe en media pagina.

    La altura total es BLK_PAD (header + barra de consulta + padding) mas el area
    de fotos (n_rows * ph + gaps entre filas). Siempre sera <= MAX_BLK_H.

    Parametros:
        n_imgs (int): Numero total de imagenes del producto.

    Devuelve:
        float: Altura total del bloque en puntos de ReportLab, <= MAX_BLK_H.
    """
    n_rows = max(1, -(-n_imgs // N_FOTO))
    ph = calcular_ph(n_imgs)
    content_h = n_rows * ph + (n_rows - 1) * FOTO_GAP
    return BLK_PAD + content_h

# ─────────────────────────────────────────────────────────────────────────────
# BARRA "CONSULTAR STOCK DE TALLAS"  (sin botones, sin links)
# ─────────────────────────────────────────────────────────────────────────────

def dibujar_barra_consulta(c: canvas.Canvas, zona_y: float, zona_h: float):
    """
    Dibuja la barra de consulta entre el header y las fotos del bloque.

    Reemplaza a dibujar_botones_canales de catalogo_sin_inventario.py.
    En lugar de botones clickeables (WhatsApp, Instagram, Facebook, Ver Tienda),
    muestra unicamente el texto "Consultar stock de tallas" centrado en la barra,
    en color dorado sobre fondo gris muy suave (#F7F8FA).

    No contiene ningun link, URL ni elemento interactivo. El objetivo es informar
    al cliente que puede consultar disponibilidad, sin revelar canales de contacto.

    La barra es mas pequena que en la version publica (BTN_BAR_H = 8 mm en lugar
    de 16 mm) al no necesitar espacio para los 4 botones.

    Parametros:
        c (canvas.Canvas): Lienzo PDF sobre el que dibujar.
        zona_y (float): Coordenada Y del borde inferior de la barra (en puntos).
        zona_h (float): Altura de la barra (= BTN_BAR_H = 8 mm).
    """
    c.setFillColor(colors.HexColor("#F7F8FA"))
    c.rect(0, zona_y, PAGE_W, zona_h, fill=1, stroke=0)

    c.setFillColor(C_ACCENT)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(
        PAGE_W / 2,
        zona_y + (zona_h / 2) - 1.2 * mm,
        "Consultar stock de tallas",
    )

    c.setStrokeColor(C_LINE)
    c.setLineWidth(0.3)
    c.line(MARGIN, zona_y, PAGE_W - MARGIN, zona_y)

# ─────────────────────────────────────────────────────────────────────────────
# DIBUJO DE BLOQUE
# ─────────────────────────────────────────────────────────────────────────────

def dibujar_bloque(c: canvas.Canvas, prod: dict,
                   bloque_x: float, bloque_y: float, bloque_h: float,
                   is_first_on_page: bool = False, precio: int = 0):
    """
    Dibuja el bloque completo de un producto en el lienzo PDF (version revendedor/cliente).

    Un bloque comprende (de arriba hacia abajo):
    1. Mini-header oscuro (ancho completo de pagina): categoria en dorado arriba,
       SKU en blanco a la izquierda, precio de reventa en dorado a la derecha.
    2. Barra de consulta (dibujar_barra_consulta): solo texto "Consultar stock de tallas",
       sin ningun boton ni link. Mas pequena (8 mm) que la version con botones.
    3. Cuadricula de fotos (ancho completo, N_FOTO = 3 por fila).
    4. Linea separadora en la parte inferior del bloque.

    Diferencias respecto a catalogo_sin_inventario.py:
    - Usa dibujar_barra_consulta() en lugar de dibujar_botones_canales().
    - El precio mostrado es el precio de reventa (ya transformado por obtener_precio).

    Parametros:
        c (canvas.Canvas): Lienzo PDF sobre el que dibujar.
        prod (dict): Diccionario del producto con claves 'sku', 'categoria', 'imgs', 'precio'.
        bloque_x (float): Coordenada X del borde izquierdo del bloque (= MARGIN).
        bloque_y (float): Coordenada Y del borde INFERIOR del bloque (en puntos).
        bloque_h (float): Altura total del bloque (en puntos).
        is_first_on_page (bool): Si True, el header se extiende hasta el borde superior.
        precio (int): Precio de reventa en CLP a mostrar. Si es 0 no se muestra.
    """
    bw = PAGE_W - 2 * MARGIN

    # ── Mini-header ───────────────────────────────────────────────────────
    hdr_y   = bloque_y + bloque_h - HDR_H
    hdr_top = PAGE_H if is_first_on_page else (hdr_y + HDR_H)
    c.setFillColor(C_DARK)
    c.rect(0, hdr_y, PAGE_W, hdr_top - hdr_y, fill=1, stroke=0)

    # Categoria pequeña arriba
    c.setFillColor(C_ACCENT)
    c.setFont("Helvetica-Oblique", 7)
    c.drawString(MARGIN, hdr_y + HDR_H - 3.5*mm, prod["categoria"].upper())

    # SKU grande
    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, hdr_y + 4.5*mm, f"SKU: {prod['sku']}")

    # Precio a la derecha
    if precio:
        precio_str = f"${precio:,}".replace(",", ".")
        c.setFillColor(C_ACCENT)
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(PAGE_W - MARGIN, hdr_y + 4.5*mm, precio_str)

    # ── Barra "Consultar stock de tallas" (justo bajo el header) ─────────
    btn_bar_y = hdr_y - BTN_BAR_H
    dibujar_barra_consulta(c, btn_bar_y, BTN_BAR_H)

    # ── Fotos (toda la anchura, N_FOTO por fila) ──────────────────────────
    content_top = btn_bar_y - 2 * mm
    imgs   = prod["imgs"]
    n_rows = max(1, -(-len(imgs) // N_FOTO))
    ph     = calcular_ph(len(imgs))
    y_band = content_top

    for row_i in range(n_rows):
        row_imgs  = imgs[row_i * N_FOTO : (row_i + 1) * N_FOTO]
        if not row_imgs:
            break
        y_row_bot = y_band - ph
        for j, img in enumerate(row_imgs):
            fx = MARGIN + j * (PHOTO_W + FOTO_GAP)
            dibujar_imagen(c, img, fx, y_row_bot, PHOTO_W, ph)
        gap = FOTO_GAP if row_i < n_rows - 1 else 0
        y_band = y_row_bot - gap

    # Linea separadora
    c.setStrokeColor(C_LINE)
    c.setLineWidth(0.4)
    c.line(bloque_x, bloque_y, bloque_x + bw, bloque_y)

# ─────────────────────────────────────────────────────────────────────────────
# AGRUPACION EN PAGINAS
# ─────────────────────────────────────────────────────────────────────────────

def agrupar_en_paginas(productos: list) -> list:
    """
    Agrupa los productos en paginas con un maximo de 2 modelos por pagina.

    Reglas de agrupacion:
    - Maximo 2 modelos por pagina (las alturas garantizan que siempre caben 2).
    - Nueva pagina al cambiar de categoria: si el siguiente producto pertenece
      a una categoria distinta, se cierra la pagina actual aunque no este llena.
    - Esto garantiza que el indice apunte siempre al primer producto de cada
      categoria en su propia pagina.

    Parametros:
        productos (list): Lista de dicts de producto, ordenada por categoria y SKU.

    Devuelve:
        list[list]: Lista de paginas, donde cada pagina es una lista de 1 o 2 productos.
    """
    if not productos:
        return []
    pages   = []
    current = []

    for prod in productos:
        cambio_cat = bool(current) and current[-1]["categoria"] != prod["categoria"]
        if cambio_cat or len(current) >= 2:
            if current:
                pages.append(current)
            current = [prod]
        else:
            current.append(prod)

    if current:
        pages.append(current)
    return pages

# ─────────────────────────────────────────────────────────────────────────────
# INDICE
# ─────────────────────────────────────────────────────────────────────────────

def dest_name(sku: str) -> str:
    """
    Genera un nombre de destino interno valido para los bookmarks y links del PDF.

    Convierte el SKU en un identificador seguro para PDF usando el prefijo 'ep_'
    (de 'En Proceso'), identico al de catalogo_sin_inventario.py para mantener
    consistencia entre ambas versiones.

    Parametros:
        sku (str): Numero del modelo (nombre de la subcarpeta dentro de 'En Proceso').

    Devuelve:
        str: Nombre de destino con prefijo 'ep_' (ej: 'ep_180', 'ep_40').
    """
    return "ep_" + sku.replace(" ", "_").replace("-", "_")


def dibujar_portada(cv: canvas.Canvas):
    """
    Dibuja la portada del catalogo en proceso para revendedor/cliente (primera pagina).

    Identica a catalogo_sin_inventario.py: fondo oscuro, franjas doradas,
    titulo "CATALOGO EN PROCESO", nombre "KLIN" y linea separadora.
    No incluye boton de enlace a la tienda ni ningun link externo.

    Al terminar llama a cv.showPage() para pasar a la siguiente pagina.

    Parametros:
        cv (canvas.Canvas): Lienzo PDF sobre el que dibujar.
    """
    W, H = A4
    cv.setFillColor(C_DARK)
    cv.rect(0, 0, W, H, fill=1, stroke=0)

    cv.setFillColor(C_ACCENT)
    cv.rect(0, H - 6*mm, W, 6*mm, fill=1, stroke=0)
    cv.rect(0, 0, W, 6*mm, fill=1, stroke=0)

    cv.setFillColor(C_WHITE)
    cv.setFont("Helvetica-Bold", 28)
    cv.drawCentredString(W / 2, H / 2 + 18*mm, "CATALOGO EN PROCESO")

    cv.setFillColor(C_ACCENT)
    cv.setFont("Helvetica-Bold", 42)
    cv.drawCentredString(W / 2, H / 2 - 8*mm, "KLIN")

    cv.setStrokeColor(C_ACCENT)
    cv.setLineWidth(1.5)
    cv.line(W/2 - 40*mm, H/2 + 8*mm, W/2 + 40*mm, H/2 + 8*mm)

    cv.showPage()


def dibujar_indice(cv: canvas.Canvas, productos: list):
    """
    Genera la(s) pagina(s) de indice por categoria al inicio del catalogo.

    Identica en estructura a catalogo_sin_inventario.py: indice plano donde
    cada fila es una categoria clickeable que lleva al primer producto de ese grupo.

    El subtitulo de la primera pagina es "Toca una categoria para ir al primer modelo".
    Cada fila tiene fondo dorado suave, nombre de categoria y flecha '>'.

    Parametros:
        cv (canvas.Canvas): Lienzo PDF sobre el que dibujar.
        productos (list): Lista de dicts de producto (resultado de buscar_productos()).
    """
    W, H = A4
    M    = 12 * mm

    cat_first: dict = {}
    for p in productos:
        cat = p["categoria"]
        if cat not in cat_first:
            cat_first[cat] = dest_name(p["sku"])

    LEAF_H  = 8 * mm
    cat_seen: set = set()

    def new_page(first=False):
        """
        Dibuja el encabezado de una pagina del indice (header oscuro con titulo).

        Parametros:
            first (bool): Si True muestra la instruccion de uso; si False '(continuacion)'.
        """
        cv.setFillColor(C_DARK)
        cv.rect(0, H - 20*mm, W, 20*mm, fill=1, stroke=0)
        cv.setFillColor(C_WHITE)
        cv.setFont("Helvetica-Bold", 15)
        cv.drawCentredString(W / 2, H - 12*mm, "CATALOGO EN PROCESO  —  INDICE")
        cv.setFillColor(C_ACCENT)
        cv.setFont("Helvetica-Oblique", 7.5)
        label = "Toca una categoria para ir al primer modelo" if first else "(continuacion)"
        cv.drawCentredString(W / 2, H - 18*mm, label)

    new_page(first=True)
    cy = H - 24*mm

    for cat, dest in cat_first.items():
        needed = LEAF_H + 2*mm
        if cy - needed < M:
            cv.showPage()
            new_page(first=False)
            cy = H - 24*mm

        row_y = cy - LEAF_H

        cv.setFillColor(colors.HexColor("#FDF3DC"))
        cv.rect(M, row_y + 0.5*mm, W - 2*M, LEAF_H - 1*mm, fill=1, stroke=0)
        cv.setFillColor(C_ACCENT)
        cv.rect(M, row_y + 0.5*mm, 1.5*mm, LEAF_H - 1*mm, fill=1, stroke=0)

        cv.setFillColor(C_DARK)
        cv.setFont("Helvetica-Bold", 10)
        cv.drawString(M + 4*mm, row_y + 2.5*mm, cat)

        cv.setFillColor(C_ACCENT)
        cv.setFont("Helvetica-Bold", 9)
        cv.drawRightString(W - M - 2*mm, row_y + 2.5*mm, ">")

        cv.setStrokeColor(C_LINE)
        cv.setLineWidth(0.3)
        cv.line(M, row_y, W - M, row_y)

        cv.linkAbsolute("", dest,
                        Rect=(M, row_y, W - M, row_y + LEAF_H),
                        thickness=0)

        if cat not in cat_seen:
            cv.bookmarkHorizontal(f"cat_{cat.replace(' ','_')}", 0, cy)
            cat_seen.add(cat)
        cv.addOutlineEntry(cat, dest, level=0, closed=True)

        cy -= LEAF_H

    cv.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# GENERACION
# ─────────────────────────────────────────────────────────────────────────────

def generar_catalogo(productos: list):
    """
    Orquesta la generacion completa del PDF del catalogo en proceso para revendedor/cliente.

    Secuencia de generacion:
    1. Portada sin links (dibujar_portada).
    2. Pagina(s) de indice por categoria (dibujar_indice).
    3. Paginas de productos: agrupa en paginas, calcula altura de bloques,
       registra bookmarks y llama a dibujar_bloque (con barra de consulta,
       sin botones de canales).

    El PDF se guarda en OUTPUT_PDF (catalogo_en_proceso_cliente.pdf) al finalizar.

    Parametros:
        productos (list): Lista de dicts de producto con claves 'sku', 'categoria',
                          'imgs' y 'precio' (precios ya transformados para reventa).
    """
    cv = canvas.Canvas(str(OUTPUT_PDF), pagesize=A4)
    cv.setTitle("Catalogo En Proceso - KLIN")
    cv.setAuthor("Catalogo Zapatos")

    dibujar_portada(cv)
    dibujar_indice(cv, productos)

    paginas = agrupar_en_paginas(productos)

    for pagina in paginas:
        cursor_y      = PAGE_H - MARGIN
        first_on_page = True

        for prod in pagina:
            bh = calcular_bloque_h(len(prod["imgs"]))
            dest = dest_name(prod["sku"])

            bloque_y = cursor_y - bh
            cv.bookmarkHorizontal(dest, 0, cursor_y)

            dibujar_bloque(cv, prod, MARGIN, bloque_y, bh,
                           is_first_on_page=first_on_page,
                           precio=prod["precio"])

            cursor_y      = bloque_y - GAP_BLK
            first_on_page = False

        cv.showPage()

    cv.save()

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    """
    Funcion principal: busca los productos en proceso y genera el catalogo para revendedor.

    Flujo de ejecucion:
    1. Busca todas las carpetas 'En Proceso' en ROOT_DIR mediante buscar_productos().
       Los precios ya vienen transformados para reventa desde buscar_productos().
    2. Si no se encontraron productos, informa y termina.
    3. Llama a generar_catalogo() con la lista de productos.
    4. El PDF se guarda en OUTPUT_PDF (catalogo_en_proceso_cliente.pdf).

    No recibe parametros ni devuelve valores. No requiere CSV de inventario.
    """
    print(f"Buscando carpetas 'En Proceso' en: {ROOT_DIR}\n")
    productos = buscar_productos()

    if not productos:
        print("No se encontraron productos.")
        return

    print(f"\nTotal: {len(productos)} modelos")
    print(f"Generando PDF: {OUTPUT_PDF}\n")
    generar_catalogo(productos)
    print("Listo.")


if __name__ == "__main__":
    main()
