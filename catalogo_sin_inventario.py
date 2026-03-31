"""
Generador de catalogo PDF para zapatos EN PROCESO — version publica con botones.

Publico objetivo: clientes y seguidores en redes sociales que consultan modelos
que aun no estan en el inventario CSV pero ya tienen fotos disponibles.

Este script NO utiliza ningun archivo CSV de inventario. En su lugar, detecta
automaticamente los productos buscando carpetas llamadas "En Proceso" dentro
del arbol de directorios ROOT_DIR.

Estructura de carpetas que debe existir:
    [Categoria]/
        En Proceso/
            [numero_sku]/
                HD/
                    foto1.jpg
                    foto2.jpg

Caracteristicas principales:
- Sin inventario, sin tallas: muestra solo fotos + SKU + categoria + precio.
- Los precios se configuran manualmente en las tablas PRECIOS_* al inicio del script.
- Maximo 2 modelos por pagina; nueva pagina al cambiar de categoria.
- Botones clickeables: WhatsApp (con SKU en el mensaje), Instagram, Facebook, Ver Tienda.
- Indice por categoria con links internos al PDF.

Archivo de salida: catalogo_en_proceso.pdf (en la misma carpeta que este script)
"""

import io
import os
from pathlib import Path
from urllib.parse import quote

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

# ── Rutas ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent.parent       # .../Zapatos
OUTPUT_PDF = SCRIPT_DIR / "catalogo_en_proceso.pdf"

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
    si el nombre no esta en el diccionario, aplica title() para capitalizar
    correctamente las palabras.

    Parametros:
        s (str): Nombre de la carpeta tal como aparece en el sistema de archivos.

    Devuelve:
        str: Nombre corregido con tildes y caracteres especiales, listo para
             mostrarse en el catalogo (ej: 'Ninos' -> 'Niños', 'Bebes' -> 'Bebés').
    """
    key = s.strip().lower()
    if key in _CORR:
        return _CORR[key]
    return s.strip().title()

# ── Tablas de precios por categoría ───────────────────────────────────────────
# Cada tabla mapea número de carpeta (int) → precio en CLP (int).
# Si una carpeta no aparece en la tabla, se usa el precio por defecto de abajo.

PRECIOS_BALLERINAS: dict = {
    # ejemplo: 1234: 18000,
    19:10000,
    22:10000,
    40:10000,
}

PRECIOS_BEBES: dict = {
    # ejemplo: 2001: 12000,
}

PRECIOS_BOTINES: dict = {
    # ejemplo: 3050: 17000,
}

PRECIOS_BOTINES_NINAS: dict = {
    # ejemplo: 4010: 16000,
    180:15000,
    186:10000,
    187:15000,
    188:15000,
    194:15000,
    
}

PRECIOS_ZAPATILLAS_NINOS: dict = {
    # ejemplo: 5005: 14000,
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


def obtener_precio(categoria: str, sku: str) -> int:
    """
    Devuelve el precio en pesos chilenos (CLP) para un producto segun su categoria y SKU.

    Busca el SKU (convertido a entero) en la tabla de precios especifica de la categoria.
    Si el SKU no esta en la tabla, usa el precio por defecto definido en _PRECIO_DEFAULT
    para esa categoria. Si la categoria no existe en ninguna de las dos tablas, devuelve 0.

    Tablas de precios disponibles (configurables al inicio del script):
    - PRECIOS_BALLERINAS: precios especificos para modelos de Ballerinas.
    - PRECIOS_BEBES: precios especificos para modelos de Bebés.
    - PRECIOS_BOTINES: precios especificos para Botines.
    - PRECIOS_BOTINES_NINAS: precios especificos para Botines Niñas.
    - PRECIOS_ZAPATILLAS_NINOS: precios especificos para Zapatillas Niños.

    Parametros:
        categoria (str): Nombre de la categoria ya corregido (ej: 'Botines Niñas').
        sku (str): Numero de carpeta del modelo (ej: '180').

    Devuelve:
        int: Precio en pesos chilenos (CLP). Devuelve 0 si no se puede determinar.
    """
    tabla = _PRECIO_TABLA.get(categoria, {})
    try:
        return tabla.get(int(sku), _PRECIO_DEFAULT.get(categoria, 0))
    except (ValueError, TypeError):
        return _PRECIO_DEFAULT.get(categoria, 0)

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
BTN_BAR_H  = 16 * mm                             # barra de canales/botones
BLK_PAD    = HDR_H + BTN_BAR_H + 5 * mm          # header + botones + (2mm gap fotos + 3mm bottom)

# Altura maxima por bloque para que 2 modelos quepan siempre en la pagina
MAX_BLK_H     = (PAGE_H - 2 * MARGIN - GAP_BLK) / 2
MAX_CONTENT_H = MAX_BLK_H - BLK_PAD

# ─────────────────────────────────────────────────────────────────────────────
# BUSQUEDA DE PRODUCTOS
# ─────────────────────────────────────────────────────────────────────────────

def buscar_productos() -> list:
    """
    Recorre el arbol de directorios buscando carpetas 'En Proceso' con productos.

    Para cada carpeta llamada exactamente 'En Proceso' encontrada dentro de ROOT_DIR:
    - Determina la categoria a partir del nombre de la carpeta padre y la corrige
      aplicando corregir_nombre() para obtener tildes correctas.
    - Itera sobre las subcarpetas dentro de 'En Proceso' (cada una es un SKU/modelo).
    - Para cada subcarpeta que contenga una carpeta 'HD' con al menos una imagen
      valida (.png, .jpg, .jpeg), crea un dict de producto y lo agrega a la lista.
    - Obtiene el precio del modelo llamando a obtener_precio(categoria, sku).

    La lista resultante se ordena por categoria (alfabetico) y luego por SKU
    numerico (si el nombre de la carpeta es un numero entero) o alfabetico.

    Imprime en consola cada producto encontrado para facilitar el seguimiento.

    Devuelve:
        list[dict]: Lista de dicts de producto ordenada, cada uno con claves:
                    - 'sku' (str): Nombre de la subcarpeta (numero del modelo).
                    - 'categoria' (str): Nombre de categoria corregido.
                    - 'imgs' (list[Path]): Lista ordenada de rutas a las fotos.
                    - 'precio' (int): Precio en CLP segun las tablas configuradas.
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

    # Ordenar por categoria luego SKU numerico si posible
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
    1. Aplanar transparencia: si la imagen tiene canal alfa (PNG con fondo transparente),
       compone la imagen sobre un fondo blanco solido para evitar fondos negros en el PDF.
    2. Redimensionar: reduce la imagen a max_px en su dimension mayor, manteniendo
       la proporcion original (usando el algoritmo LANCZOS de alta calidad).
    3. Convertir a JPEG: guarda en buffer en memoria con calidad 60 y optimizacion
       activada, reduciendo el peso final del PDF.

    Las imagenes procesadas se almacenan en _img_cache con la clave (ruta, max_px),
    evitando reprocesar la misma imagen si se llama mas de una vez.

    Parametros:
        img_path (Path): Ruta al archivo de imagen original (.png, .jpg o .jpeg).
        max_px (int): Dimension maxima en pixeles tras redimensionar. Por defecto 350 px,
                      ajustado para el tamano de foto en este catalogo.

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
    del rectangulo (x, y, w, h) sin deformarla ni recortarla. La imagen se centra
    tanto horizontal como verticalmente dentro del area disponible.

    Si ocurre cualquier error al cargar o dibujar la imagen (archivo corrupto,
    formato no soportado, etc.), imprime una advertencia y continua sin interrumpir
    la generacion del PDF.

    Nota: a diferencia de crear_catalogo.py, esta funcion no acepta el parametro
    max_px porque las fotos de este catalogo siempre se preparan con el default
    de 350 px definido en preparar_imagen().

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

    Se usa para los botones de canales (WhatsApp, Instagram, Facebook, Ver Tienda)
    en la barra de botones de cada bloque de producto.

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

    Determina cuantas filas de fotos necesita el producto (ceil de n_imgs / N_FOTO)
    y calcula la altura maxima por foto tal que toda la cuadricula de fotos quepa
    dentro del area de contenido maxima (MAX_CONTENT_H). Ademas limita la altura
    a PHOTO_W para que las fotos nunca superen el tamano cuadrado de referencia.

    Garantiza que 2 modelos siempre caben en una pagina A4 con los margenes
    configurados, independientemente del numero de fotos.

    Parametros:
        n_imgs (int): Numero total de imagenes del producto.

    Devuelve:
        float: Altura de foto en puntos, entre MIN_PH (implicito por MAX_CONTENT_H)
               y PHOTO_W.
    """
    n_rows = max(1, -(-n_imgs // N_FOTO))
    ph_max = (MAX_CONTENT_H - (n_rows - 1) * FOTO_GAP) / n_rows
    return min(PHOTO_W, ph_max)


def calcular_bloque_h(n_imgs: int) -> float:
    """
    Calcula la altura total del bloque de un producto, garantizando que cabe en media pagina.

    La altura total es:
    - BLK_PAD: overhead fijo (header oscuro + barra de botones de canales + padding vertical).
    - content_h: altura del area de fotos = n_rows * ph + gaps entre filas.

    Usa calcular_ph() para obtener el alto de foto optimo, lo que asegura que
    el bloque siempre cabe en MAX_BLK_H (la mitad de la pagina util).

    Parametros:
        n_imgs (int): Numero total de imagenes del producto.

    Devuelve:
        float: Altura total del bloque en puntos de ReportLab, <= MAX_BLK_H.
    """
    n_rows = max(1, -(-n_imgs // N_FOTO))   # ceil division
    ph = calcular_ph(n_imgs)
    content_h = n_rows * ph + (n_rows - 1) * FOTO_GAP
    return BLK_PAD + content_h

# ─────────────────────────────────────────────────────────────────────────────
# BARRA DE CANALES
# ─────────────────────────────────────────────────────────────────────────────

_C_WA   = colors.HexColor("#25D366")   # WhatsApp verde
_C_IG   = colors.HexColor("#C13584")   # Instagram morado
_C_FB   = colors.HexColor("#1877F2")   # Facebook azul


def dibujar_botones_canales(c: canvas.Canvas, sku: str,
                             zona_y: float, zona_h: float):
    """
    Dibuja la barra de botones de canales entre el header y las fotos del bloque.

    La barra tiene fondo gris muy suave (#F7F8FA) y contiene:
    - Texto invitacion: "Visitenos en nuestros canales para mas informacion".
    - 4 botones clickeables alineados horizontalmente y centrados en la pagina:
        * WhatsApp (verde #25D366): enlaza a wa.me con el SKU en el mensaje,
          permitiendo al cliente consultar directamente por tallas del modelo.
        * Instagram (morado #C13584): enlaza al perfil de Instagram de la tienda.
        * Facebook (azul #1877F2): enlaza a la pagina de Facebook de la tienda.
        * Ver Tienda (fondo oscuro): enlaza a la tienda online.
    - Linea separadora inferior en gris claro.

    Parametros:
        c (canvas.Canvas): Lienzo PDF sobre el que dibujar.
        sku (str): Numero de SKU del modelo, incluido en el mensaje de WhatsApp
                   para que el vendedor identifique el modelo consultado.
        zona_y (float): Coordenada Y del borde inferior de la barra (en puntos).
        zona_h (float): Altura de la barra (= BTN_BAR_H = 16 mm).
    """
    # Fondo muy suave para diferenciar de fotos
    c.setFillColor(colors.HexColor("#F7F8FA"))
    c.rect(0, zona_y, PAGE_W, zona_h, fill=1, stroke=0)

    # Texto invitacion
    c.setFillColor(C_MID)
    c.setFont("Helvetica-Oblique", 6.5)
    c.drawCentredString(
        PAGE_W / 2,
        zona_y + zona_h - 4.5 * mm,
        "Visitenos en nuestros canales para mas informacion",
    )

    # Dimensiones de botones
    btn_w   = 39 * mm
    btn_h   = 7 * mm
    btn_gap = 3 * mm
    total_w = 4 * btn_w + 3 * btn_gap
    btn_x0  = (PAGE_W - total_w) / 2
    btn_y   = zona_y + 1.5 * mm

    wa_msg = quote(
        f"Hola quiero consultar por las tallas disponibles "
        f"de este modelo SKU: {sku}"
    )
    botones = [
        ("WhatsApp",
         f"https://wa.me/56933276344?text={wa_msg}",
         _C_WA),
        ("Instagram",
         "https://www.instagram.com/todoexclusivo_shop"
         "?igsh=aHg0ZXpxYWNqMGc%3D&utm_source=qr",
         _C_IG),
        ("Facebook",
         "https://www.facebook.com/share/17FoeykVmr/?mibextid=wwXIfr",
         _C_FB),
        ("Ver Tienda",
         "https://todoexclusivo.cl/tienda/",
         C_DARK),
    ]

    for i, (label, url, color) in enumerate(botones):
        bx = btn_x0 + i * (btn_w + btn_gap)
        rounded_rect(c, bx, btn_y, btn_w, btn_h, r=1.5 * mm, fill=color)
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(bx + btn_w / 2, btn_y + 2.2 * mm, label)
        c.linkURL(url, (bx, btn_y, bx + btn_w, btn_y + btn_h), relative=0)

    # Linea separadora inferior de la barra
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
    Dibuja el bloque completo de un producto en el lienzo PDF.

    Un bloque comprende (de arriba hacia abajo):
    1. Mini-header oscuro (ancho completo de pagina): categoria en dorado arriba,
       SKU en blanco grande a la izquierda, precio en dorado a la derecha.
    2. Barra de botones de canales (dibujar_botones_canales): WhatsApp, Instagram,
       Facebook y Ver Tienda, con fondo gris suave entre el header y las fotos.
    3. Cuadricula de fotos (ancho completo, N_FOTO = 3 por fila): las fotos
       se distribuyen en filas comenzando debajo de la barra de botones.
    4. Linea separadora en la parte inferior del bloque.

    El sistema de coordenadas de ReportLab tiene el origen en la esquina inferior
    izquierda. bloque_y es el borde INFERIOR del bloque.

    Parametros:
        c (canvas.Canvas): Lienzo PDF sobre el que dibujar.
        prod (dict): Diccionario del producto con claves 'sku', 'categoria', 'imgs', 'precio'.
        bloque_x (float): Coordenada X del borde izquierdo del bloque (= MARGIN).
        bloque_y (float): Coordenada Y del borde INFERIOR del bloque (en puntos).
        bloque_h (float): Altura total del bloque (en puntos).
        is_first_on_page (bool): Si True, el header se extiende hasta el borde
                                 superior de la pagina. Por defecto False.
        precio (int): Precio en CLP a mostrar en el header. Si es 0 no se muestra.
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

    # ── Barra de botones (justo bajo el header) ───────────────────────────
    btn_bar_y = hdr_y - BTN_BAR_H
    dibujar_botones_canales(c, prod["sku"], btn_bar_y, BTN_BAR_H)

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
    - Maximo 2 modelos por pagina (las alturas estan calculadas para que 2
      siempre quepan en una pagina A4 gracias a calcular_bloque_h).
    - Nueva pagina al cambiar de categoria: si el siguiente producto es de
      una categoria distinta al ultimo de la pagina actual, se cierra la
      pagina aunque no este llena, para que cada categoria empiece en pagina nueva.

    Estas reglas garantizan que el indice por categoria siempre apunte
    al primer producto de cada categoria en su propia pagina.

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

    Convierte el SKU (nombre de la carpeta) en un identificador seguro para PDF,
    reemplazando espacios y guiones por guiones bajos y usando el prefijo 'ep_'
    (de 'En Proceso') para distinguirlo de los destinos de crear_catalogo.py.

    Parametros:
        sku (str): Numero del modelo (nombre de la subcarpeta dentro de 'En Proceso').

    Devuelve:
        str: Nombre de destino con prefijo 'ep_' (ej: 'ep_180', 'ep_40').
    """
    return "ep_" + sku.replace(" ", "_").replace("-", "_")


def dibujar_portada(cv: canvas.Canvas):
    """
    Dibuja la portada del catalogo en proceso (primera pagina del PDF).

    La portada incluye:
    - Fondo oscuro completo (#1B2A3B).
    - Franja dorada decorativa en el borde superior e inferior.
    - Titulo "CATALOGO EN PROCESO" en blanco.
    - Nombre de la marca "KLIN" en dorado grande.
    - Linea separadora dorada.

    No incluye boton de enlace a la tienda (a diferencia de crear_catalogo.py).
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

    A diferencia del indice de crear_catalogo.py (que es jerarquico con multiples
    niveles), este indice es plano: cada fila corresponde directamente a una
    categoria y es un link clickeable al primer producto de ese grupo en el PDF.

    El subtitulo de la primera pagina es "Toca una categoria para ir al primer modelo".

    Cada fila de categoria tiene:
    - Fondo dorado suave (#FDF3DC) con borde izquierdo dorado.
    - Nombre de la categoria en negrita.
    - Flecha '>' en dorado a la derecha.
    - Link interno al primer producto de esa categoria.
    - Bookmark PDF y entrada en el panel de marcadores del lector.

    Si el indice no cabe en una pagina, continua en paginas adicionales.

    Parametros:
        cv (canvas.Canvas): Lienzo PDF sobre el que dibujar.
        productos (list): Lista de dicts de producto (resultado de buscar_productos()).
    """
    W, H = A4
    M    = 12 * mm

    # Agrupar: categoria -> primer SKU dest
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

        # Fondo dorado suave
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
    Orquesta la generacion completa del PDF del catalogo en proceso.

    Secuencia de generacion:
    1. Portada (dibujar_portada).
    2. Pagina(s) de indice por categoria (dibujar_indice).
    3. Paginas de productos: agrupa en paginas (agrupar_en_paginas), calcula
       la altura de cada bloque (calcular_bloque_h), registra un bookmark
       por producto y llama a dibujar_bloque para cada uno.

    El PDF se guarda en OUTPUT_PDF (catalogo_en_proceso.pdf) al finalizar.

    Parametros:
        productos (list): Lista de dicts de producto con claves 'sku', 'categoria',
                          'imgs' y 'precio' (resultado de buscar_productos()).
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
    Funcion principal: busca los productos en proceso y genera el catalogo PDF.

    Flujo de ejecucion:
    1. Busca todas las carpetas 'En Proceso' en ROOT_DIR mediante buscar_productos().
    2. Si no se encontraron productos, informa y termina.
    3. Llama a generar_catalogo() con la lista de productos encontrados.
    4. El PDF resultante se guarda en OUTPUT_PDF (catalogo_en_proceso.pdf).

    No recibe parametros ni devuelve valores. No requiere ningun CSV de inventario;
    los precios se toman de las tablas PRECIOS_* configuradas al inicio del script.
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

