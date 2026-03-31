"""
Generador de catalogo PDF para zapatos EN PROCESO — version revendedor/cliente.
- Sin botones ni links de contacto (WhatsApp, Instagram, Facebook, Tienda)
- Muestra "Consultar stock de tallas" encima de cada modelo
- Precios ajustados para reventa:
    Bebés          → 16.990
    10.000 base    → 19.990
    15.000 base    → 24.990
    20.000 base    → 29.990
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
    """Convierte el precio base al precio de reventa para el cliente."""
    if categoria == "Bebés":
        return 16990
    return _PRECIO_REVENTA.get(precio_base, precio_base)


def obtener_precio(categoria: str, sku: str) -> int:
    """Devuelve el precio de reventa CLP para una carpeta dado su SKU y categoría."""
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
    n_rows = max(1, -(-n_imgs // N_FOTO))
    ph_max = (MAX_CONTENT_H - (n_rows - 1) * FOTO_GAP) / n_rows
    return min(PHOTO_W, ph_max)


def calcular_bloque_h(n_imgs: int) -> float:
    n_rows = max(1, -(-n_imgs // N_FOTO))
    ph = calcular_ph(n_imgs)
    content_h = n_rows * ph + (n_rows - 1) * FOTO_GAP
    return BLK_PAD + content_h

# ─────────────────────────────────────────────────────────────────────────────
# BARRA "CONSULTAR STOCK DE TALLAS"  (sin botones, sin links)
# ─────────────────────────────────────────────────────────────────────────────

def dibujar_barra_consulta(c: canvas.Canvas, zona_y: float, zona_h: float):
    """Reemplaza la barra de botones: solo muestra texto informativo."""
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
    return "ep_" + sku.replace(" ", "_").replace("-", "_")


def dibujar_portada(cv: canvas.Canvas):
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
