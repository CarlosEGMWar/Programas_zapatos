"""
Generador de catalogo PDF para calzado (version revendedor/cliente).
- 2 modelos por pagina (3 si el modelo tiene 1 sola carpeta)
- PNG con transparencia -> fondo blanco (no negro)
- Imagenes comprimidas a JPEG para reducir peso del PDF
- Sin links externos (sin WhatsApp, Instagram, Facebook, ni tienda)
- Botones de talla en dorado pero sin link clicleable
"""

import csv
import io
import os
from pathlib import Path
from collections import defaultdict

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

# ── Rutas (relativas al script) ───────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent.parent       # .../Zapatos
INVENTARIO = ROOT_DIR / "Inventario/Inventario_web_precios_cliente.csv"
OUTPUT_PDF = SCRIPT_DIR / "catalogo_revendedor.pdf"

# ── Campos a mostrar en ficha tecnica (etiqueta, columna_csv) ─────────────────
FICHA_TECNICA = [
    ("Empeine",        "empeine"),
    ("Forro",          "forro_interior"),
    ("Suela",          "suela"),
    ("Fabricacion",    "fabricacion"),
    ("Anatomico",      "anatomico"),
    ("Antideslizante", "antideslizante"),
    ("Cierre",         "cierre"),
    ("Composicion",    "composicion"),
    ("Uso",            "frecuencia_uso"),
    ("Luces LED",      "luces_leds"),
    ("Alto botin",     "alto_botin"),
    ("Alto botas",     "alto_botas"),
]

# ── Paleta de diseño ──────────────────────────────────────────────────────────
C_DARK   = colors.HexColor("#1B2A3B")
C_ACCENT = colors.HexColor("#C9A050")
C_MID    = colors.HexColor("#4A5568")
C_LIGHT  = colors.HexColor("#EDF2F7")
C_WHITE  = colors.white
C_LINE   = colors.HexColor("#CBD5E0")

# ── Constantes de layout ──────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4          # 595 x 842 pts  (210 x 297 mm)
MARGIN   = 10 * mm
HDR_H    = 14 * mm           # altura del mini-header por modelo
GAP_BLK  = 5  * mm           # espacio vertical entre bloques de modelo
LEFT_W   = 80 * mm
GAP_LR   = 5  * mm
RIGHT_X  = MARGIN + LEFT_W + GAP_LR
RIGHT_W  = PAGE_W - RIGHT_X - MARGIN

# Constantes de foto (compartidas entre dibujar_bloque y funciones de layout)
N_FOTO   = 3          # fotos por fila
FOTO_GAP = 0.5 * mm  # gap horizontal/vertical entre fotos
GRP_GAP  = 1.0 * mm  # gap entre grupos de color (pequeno para pegar colores)
PHOTO_W  = (RIGHT_W - (N_FOTO - 1) * FOTO_GAP) / N_FOTO  # ~34.7mm, fijo
BLK_PAD  = HDR_H + 3 * mm + 2 * mm  # overhead fijo por bloque (header + pads)
MIN_PH   = 18 * mm   # photo_h minimo aceptable


# ─────────────────────────────────────────────────────────────────────────────
# UTILIDADES CSV
# ─────────────────────────────────────────────────────────────────────────────

def leer_inventario(path: Path) -> list:
    for enc in ("utf-8-sig", "utf-8", "cp1252"):
        for delim in (",", ";"):
            try:
                with open(path, encoding=enc, newline="") as f:
                    reader = csv.DictReader(f, delimiter=delim)
                    rows = list(reader)
                    # Validar que se leyeron columnas correctamente
                    if rows and "ref_modelo" in rows[0]:
                        return rows
            except UnicodeDecodeError:
                break   # probar siguiente encoding
    raise RuntimeError(f"No se pudo leer {path}")


def val(v) -> str:
    """Devuelve el valor limpio o cadena vacia si es NULL/vacio."""
    v = (v or "").strip()
    return "" if v.upper() == "NULL" else v


# ─────────────────────────────────────────────────────────────────────────────
# BUSQUEDA DE CARPETAS
# ─────────────────────────────────────────────────────────────────────────────

def buscar_hd(root: Path, numero: str):
    """Busca recursivamente una carpeta de nombre exacto `numero` con subcarpeta HD."""
    for dirpath, dirnames, _ in os.walk(root):
        if numero in dirnames:
            hd = Path(dirpath) / numero / "HD"
            if hd.is_dir():
                return hd
    return None


def imagenes_en_hd(hd: Path) -> list:
    return sorted(
        p for p in hd.iterdir()
        if p.suffix.lower() in (".png", ".jpg", ".jpeg")
    )


# ─────────────────────────────────────────────────────────────────────────────
# PROCESAMIENTO DE IMAGENES
# ─────────────────────────────────────────────────────────────────────────────

_img_cache: dict = {}

def preparar_imagen(img_path: Path, max_px: int = 700) -> tuple:
    """
    Devuelve (ImageReader, ancho_px, alto_px).
    - Transparencia PNG -> fondo blanco
    - Redimensiona a max_px
    - Convierte a JPEG para reducir peso
    """
    cache_key = (str(img_path), max_px)
    if cache_key in _img_cache:
        return _img_cache[cache_key]

    with PILImage.open(img_path) as im:
        # Aplanar transparencia sobre blanco
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


def dibujar_imagen(c: canvas.Canvas, img_path: Path,
                   x, y, w, h, max_px: int = 200):
    """Dibuja imagen centrada en el rectangulo (x,y,w,h)."""
    try:
        img_reader, iw, ih = preparar_imagen(img_path, max_px)
        ratio = min(w / iw, h / ih)
        dw, dh = iw * ratio, ih * ratio
        cx = x + (w - dw) / 2
        cy = y + (h - dh) / 2
        c.drawImage(img_reader, cx, cy, dw, dh)
    except Exception as e:
        print(f"  [WARN] imagen {img_path.name}: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS DE DIBUJO
# ─────────────────────────────────────────────────────────────────────────────

def rounded_rect(c: canvas.Canvas, x, y, w, h, r=2*mm,
                 fill=None, stroke=None, lw=0.4):
    if fill:
        c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    p = c.beginPath()
    p.roundRect(x, y, w, h, r)
    c.drawPath(p, fill=1 if fill else 0, stroke=1 if stroke else 0)


# ─────────────────────────────────────────────────────────────────────────────
# BLOQUE DE UN MODELO
# ─────────────────────────────────────────────────────────────────────────────

def dibujar_bloque(c: canvas.Canvas, filas: list, carpetas_hd: dict,
                   bloque_x: float, bloque_y: float, bloque_h: float,
                   is_first_on_page: bool = False,
                   photo_h: float = None):
    """
    Dibuja un bloque completo de 1 modelo.
    bloque_y: coordenada Y de la PARTE INFERIOR del bloque (en puntos ReportLab).
    bloque_h: altura total del bloque.
    """
    bw = PAGE_W - 2 * MARGIN     # ancho util del bloque

    base = filas[0]

    # Agrupar tallas por color
    color_tallas: dict = defaultdict(list)
    for f in filas:
        col = val(f.get("color", "")) or "Sin color"
        t   = val(f.get("talla", ""))
        if t:
            color_tallas[col].append(t)

    # Asociar carpetas -> colores ordenando por ref_combinacion minimo de cada color.
    color_min_ref: dict = {}
    for f in filas:
        col = val(f.get("color", "")) or "Sin color"
        try:
            ref_val = int(val(f.get("ref_combinacion", "")) or "0")
        except ValueError:
            ref_val = 999999
        if col not in color_min_ref:
            color_min_ref[col] = ref_val
        else:
            color_min_ref[col] = min(color_min_ref[col], ref_val)

    nums_carpeta  = sorted(n.strip() for n in base["ref_modelo"].split("-"))
    colores_orden = sorted(color_min_ref.keys(), key=lambda col: color_min_ref[col])
    carpeta_color = {num: (colores_orden[i] if i < len(colores_orden) else f"Var. {num}")
                     for i, num in enumerate(nums_carpeta)}
    _ = carpeta_color  # suprimir warning

    # ── Mini-header ───────────────────────────────────────────────────────
    hdr_y = bloque_y + bloque_h - HDR_H
    hdr_top = PAGE_H if is_first_on_page else (hdr_y + HDR_H)
    c.setFillColor(C_DARK)
    c.rect(0, hdr_y, PAGE_W, hdr_top - hdr_y, fill=1, stroke=0)

    producto  = val(base.get("producto", "")) or "Producto"
    precio    = val(base.get("precio_con_iva", ""))
    estacion  = val(base.get("estaciones", ""))
    categoria = val(base.get("categoria_completa", ""))

    precio_str = ""
    if precio:
        try:
            precio_str = f"${int(float(precio)):,}".replace(",", ".")
        except ValueError:
            precio_str = precio

    # Nombre del producto
    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, hdr_y + 4.5*mm, producto)

    # Categoria pequeña sobre el nombre
    if categoria:
        c.setFillColor(C_ACCENT)
        c.setFont("Helvetica-Oblique", 7)
        c.drawString(MARGIN, hdr_y + HDR_H - 3.5*mm, categoria.upper())

    # Precio a la derecha
    if precio_str:
        c.setFillColor(C_ACCENT)
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(PAGE_W - MARGIN, hdr_y + 4.5*mm, precio_str)
    if estacion:
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica", 7)
        c.drawRightString(PAGE_W - MARGIN, hdr_y + HDR_H - 3.5*mm,
                          estacion.upper())

    # ── Area de contenido ─────────────────────────────────────────────────
    content_top = hdr_y - 2*mm
    content_bot = bloque_y + 1*mm

    # ── COLUMNA DERECHA: fotos ────────────────────────────────────────────
    N_LARGE   = 3
    FOTO_GAP  = 0.5 * mm

    all_imgs = {num: imagenes_en_hd(hd) for num, hd in carpetas_hd.items()}

    max_rows = 2 if any(len(v) > N_LARGE for v in all_imgs.values()) else 1

    if photo_h is None:
        photo_h = PHOTO_W

    y_band = content_top

    for num in sorted(carpetas_hd.keys()):
        imgs = all_imgs[num]

        for row_i in range(max_rows):
            row_imgs  = imgs[row_i * N_FOTO : (row_i + 1) * N_FOTO]
            if not row_imgs:
                break
            y_row_bot = y_band - photo_h
            for j, img in enumerate(row_imgs):
                fx = RIGHT_X + j * (PHOTO_W + FOTO_GAP)
                dibujar_imagen(c, img, fx, y_row_bot, PHOTO_W, photo_h, max_px=350)
            y_band = y_row_bot - (FOTO_GAP if row_i < max_rows - 1 else 0)

        y_band -= GRP_GAP

    # ── COLUMNA IZQUIERDA ─────────────────────────────────────────────────
    lx  = bloque_x
    cy  = content_top - 3 * mm

    def sec_title(txt, yy):
        c.setFillColor(C_ACCENT)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(lx, yy, txt)
        yy -= 2.5 * mm
        c.setStrokeColor(C_ACCENT)
        c.setLineWidth(0.6)
        c.line(lx, yy, lx + LEFT_W, yy)
        return yy - 4 * mm

    def row(label, value, yy, label_w=25*mm):
        c.setFillColor(C_MID)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(lx, yy, label + ":")
        c.setFillColor(C_DARK)
        c.setFont("Helvetica", 7.5)
        max_c = int((LEFT_W - label_w) / 4.3)
        v = value if len(value) <= max_c else value[:max_c - 1] + "..."
        c.drawString(lx + label_w, yy, v)
        return yy - 4.8 * mm

    # SKU
    sku = val(base.get("ref_modelo", ""))
    c.setFillColor(C_ACCENT)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(lx, cy, f"SKU: {sku}")
    cy -= 6 * mm

    cy -= 2 * mm

    # Tallas por color
    cy = sec_title("Tallas disponibles", cy)

    for color, tallas in color_tallas.items():
        if cy < content_bot + 12 * mm:
            break
        # Badge de color
        badge_h = 5 * mm
        rounded_rect(c, lx, cy - badge_h + 1*mm, LEFT_W, badge_h,
                     fill=C_LIGHT, stroke=C_LINE)
        c.setFillColor(C_DARK)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(lx + 2*mm, cy - badge_h + 2.5*mm, color)
        cy -= badge_h + 1.5 * mm

        # Chips de talla (dorados, sin link)
        chip_w  = 17 * mm
        chip_h  = 5  * mm
        chip_g  = 2  * mm
        cx_chip = lx
        for talla in tallas:
            if cx_chip + chip_w > lx + LEFT_W + 1*mm:
                cx_chip = lx
                cy -= chip_h + chip_g
                if cy < content_bot + 5*mm:
                    break
            # Siempre dorado, sin link
            rounded_rect(c, cx_chip, cy - chip_h, chip_w, chip_h,
                         r=2*mm, fill=C_ACCENT, stroke=C_ACCENT)
            c.setFillColor(C_DARK)
            c.setFont("Helvetica-Bold", 6.5)
            num_t = talla.split(" - ")[0].replace("(", "").replace(")", "").strip()
            c.drawCentredString(cx_chip + chip_w/2, cy - chip_h + 1.5*mm, num_t)
            cx_chip += chip_w + chip_g
        cy -= chip_h + 3 * mm

    cy -= 2 * mm

    # Ficha tecnica
    if cy > content_bot + 8 * mm:
        cy = sec_title("Ficha tecnica", cy)
        for label, col in FICHA_TECNICA:
            v = val(base.get(col, ""))
            if v:
                cy = row(label, v, cy)
            if cy < content_bot + 5 * mm:
                break

    # Linea separadora al final del bloque
    c.setStrokeColor(C_LINE)
    c.setLineWidth(0.4)
    c.line(bloque_x, bloque_y, bloque_x + bw, bloque_y)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS PARA INDICE Y NAVEGACION
# ─────────────────────────────────────────────────────────────────────────────

def dest_name(ref_modelo: str) -> str:
    """Nombre de destino PDF para un modelo (solo alfanumerico + _)."""
    return "prod_" + ref_modelo.replace("-", "_").replace(" ", "_")


def parse_categoria(cat: str) -> list:
    """'Ballerinas > Ninas' -> ['Ballerinas', 'Ninas']"""
    return [p.strip() for p in (cat or "Sin categoria").split(">") if p.strip()]


def _layout_prod(carpetas_hd: dict) -> tuple:
    """Devuelve (n_grupos, max_rows) para un producto."""
    n_g = len(carpetas_hd) if carpetas_hd else 1
    max_rows = 2 if any(
        len(imagenes_en_hd(hd)) > N_FOTO for hd in carpetas_hd.values()
    ) else 1
    return n_g, max_rows


def calcular_bloque_h_con_ph(carpetas_hd: dict, ph: float) -> float:
    """Altura del bloque dado un photo_h concreto."""
    n_g, max_rows = _layout_prod(carpetas_hd)
    content_h = (n_g * (max_rows * ph + (max_rows - 1) * FOTO_GAP)
                 + max(0, n_g - 1) * GRP_GAP)
    return BLK_PAD + content_h


def agrupar_en_paginas(productos: list) -> list:
    """
    Agrupa productos en paginas con photo_h = PHOTO_W fijo (sin reduccion).
    - Modelos con 3+ colores: siempre solos en su propia pagina.
    - Modelos con 1-2 colores: se agregan greedily mientras quepan.
    """
    if not productos:
        return []
    pages   = []
    current = []

    for prod in productos:
        n_colores = len(prod["carpetas_hd"])
        if n_colores >= 3:
            if current:
                pages.append(current)
                current = []
            pages.append([prod])
        else:
            trial   = current + [prod]
            avail   = PAGE_H - 2 * MARGIN - (len(trial) - 1) * GAP_BLK
            total_h = sum(calcular_bloque_h_con_ph(p["carpetas_hd"], PHOTO_W)
                          for p in trial)
            if total_h <= avail:
                current = trial
            else:
                if current:
                    pages.append(current)
                current = [prod]

    if current:
        pages.append(current)
    return pages


# ─────────────────────────────────────────────────────────────────────────────
# INDICE
# ─────────────────────────────────────────────────────────────────────────────

def dibujar_indice(cv: canvas.Canvas, productos_info: list):
    """
    Genera la(s) pagina(s) de indice jerarquico.
    Solo muestra categorias; la categoria hoja (ultimo nivel) es el link
    al primer producto de ese grupo.
    """
    W, H = A4
    M    = 12 * mm

    entries = sorted(
        productos_info,
        key=lambda p: (parse_categoria(p["categoria"]), p["nombre"].lower())
    )

    cat_first_dest: dict = {}
    seen_order: list = []
    for p in entries:
        cats = tuple(parse_categoria(p["categoria"]))
        if cats not in cat_first_dest:
            cat_first_dest[cats] = p["dest"]
            seen_order.append(cats)

    LH = {0: 9*mm, 1: 7.5*mm, 2: 7*mm}
    LEAF_H = 8 * mm

    def new_index_page(first: bool = False):
        cv.setFillColor(C_DARK)
        cv.rect(0, H - 20*mm, W, 20*mm, fill=1, stroke=0)
        cv.setFillColor(C_WHITE)
        cv.setFont("Helvetica-Bold", 15)
        cv.drawCentredString(W / 2, H - 12*mm, "CATALOGO  —  TABLA DE CONTENIDOS")
        cv.setFillColor(C_ACCENT)
        cv.setFont("Helvetica-Oblique", 7.5)
        label = "Indice de categorias" if first else "(continuacion)"
        cv.drawCentredString(W / 2, H - 18*mm, label)

    new_index_page(first=True)
    cy = H - 24*mm
    current_cats: list = []
    cat_seen: set = set()

    for cats in seen_order:
        cats_list  = list(cats)
        leaf_level = len(cats_list) - 1
        leaf_label = cats_list[-1]
        dest       = cat_first_dest[cats]

        parent_new = sum(
            1 for i in range(leaf_level)
            if i >= len(current_cats) or current_cats[i] != cats_list[i]
        )
        needed = parent_new * LH.get(min(parent_new - 1, 2), 7*mm) + LEAF_H + 2*mm
        if cy - needed < M:
            cv.showPage()
            new_index_page(first=False)
            cy = H - 24*mm
            current_cats = []

        # ── Cabeceras de los niveles padre (no-hoja) ──────────────────────
        parent_changed = False
        for level in range(leaf_level):
            level_changed = (parent_changed
                             or level >= len(current_cats)
                             or current_cats[level] != cats_list[level])
            if level_changed:
                parent_changed = True
            if level_changed:
                cat_label = cats_list[level]
                cat_key   = "__".join(cats_list[:level + 1]).replace(" ", "_")
                cat_dest  = f"cat_{cat_key}"
                lh        = LH.get(level, 7*mm)

                if level == 0:
                    cv.setFillColor(C_DARK)
                    cv.rect(0, cy - lh, W, lh, fill=1, stroke=0)
                    cv.setFillColor(C_WHITE)
                    cv.setFont("Helvetica-Bold", 11)
                    cv.drawString(M, cy - lh + 3*mm, cat_label.upper())
                elif level == 1:
                    cv.setFillColor(colors.HexColor("#2C3E50"))
                    cv.rect(M, cy - lh, W - 2*M, lh, fill=1, stroke=0)
                    cv.setFillColor(C_ACCENT)
                    cv.setFont("Helvetica-Bold", 9.5)
                    cv.drawString(M + 4*mm, cy - lh + 2.5*mm, "  " + cat_label)
                else:
                    cv.setFillColor(C_LIGHT)
                    cv.rect(M + 8*mm, cy - lh, W - 2*M - 8*mm, lh - 1*mm, fill=1, stroke=0)
                    cv.setFillColor(C_MID)
                    cv.setFont("Helvetica-Bold", 8.5)
                    cv.drawString(M + 12*mm, cy - lh + 2*mm, "  >> " + cat_label)

                if cat_dest not in cat_seen:
                    cv.bookmarkHorizontal(cat_dest, 0, cy)
                    cat_seen.add(cat_dest)
                cv.addOutlineEntry(cat_label, cat_dest, level=level, closed=False)
                cy -= lh

        # ── Fila hoja: categoria final ────────────────────────────────────
        indent = leaf_level * 5 * mm
        row_x  = M + indent
        row_w  = W - M - row_x
        row_y  = cy - LEAF_H

        # Fondo dorado suave
        cv.setFillColor(colors.HexColor("#FDF3DC"))
        cv.rect(row_x, row_y + 0.5*mm, row_w, LEAF_H - 1*mm, fill=1, stroke=0)
        # Borde izquierdo dorado
        cv.setFillColor(C_ACCENT)
        cv.rect(row_x, row_y + 0.5*mm, 1.5*mm, LEAF_H - 1*mm, fill=1, stroke=0)

        cv.setFillColor(C_DARK)
        cv.setFont("Helvetica-Bold", 9)
        cv.drawString(row_x + 4*mm, row_y + 2.5*mm, leaf_label)

        cv.setFillColor(C_ACCENT)
        cv.setFont("Helvetica-Bold", 9)
        cv.drawRightString(row_x + row_w - 2*mm, row_y + 2.5*mm, ">")

        cv.setStrokeColor(C_LINE)
        cv.setLineWidth(0.3)
        cv.line(row_x, row_y, row_x + row_w, row_y)

        # Link interno al primer producto de esta categoria hoja
        cv.linkAbsolute("", dest,
                        Rect=(row_x, row_y, row_x + row_w, row_y + LEAF_H),
                        thickness=0)

        cv.addOutlineEntry(leaf_label, dest, level=leaf_level, closed=True)

        cy -= LEAF_H
        current_cats = cats_list

    cv.showPage()


# ─────────────────────────────────────────────────────────────────────────────
# GENERACION DEL PDF
# ─────────────────────────────────────────────────────────────────────────────

def dibujar_portada(cv: canvas.Canvas):
    """Pagina 1: portada del catalogo con titulo."""
    W, H = A4

    # Fondo oscuro completo
    cv.setFillColor(C_DARK)
    cv.rect(0, 0, W, H, fill=1, stroke=0)

    # Franja dorada decorativa superior
    cv.setFillColor(C_ACCENT)
    cv.rect(0, H - 6*mm, W, 6*mm, fill=1, stroke=0)

    # Franja dorada decorativa inferior
    cv.setFillColor(C_ACCENT)
    cv.rect(0, 0, W, 6*mm, fill=1, stroke=0)

    # Titulo principal
    cv.setFillColor(C_WHITE)
    cv.setFont("Helvetica-Bold", 28)
    cv.drawCentredString(W / 2, H / 2 + 18*mm, "CATALOGO DE CALZADOS")

    # Nombre de marca en dorado, mas grande
    cv.setFillColor(C_ACCENT)
    cv.setFont("Helvetica-Bold", 42)
    cv.drawCentredString(W / 2, H / 2 - 8*mm, "KLIN")

    # Linea separadora
    cv.setStrokeColor(C_ACCENT)
    cv.setLineWidth(1.5)
    cv.line(W/2 - 40*mm, H/2 + 8*mm, W/2 + 40*mm, H/2 + 8*mm)

    cv.showPage()


def generar_catalogo(productos: list):
    """
    productos: lista de dict con claves filas, carpetas_hd.
    Genera indice primero y luego todas las paginas de productos.
    """
    cv = canvas.Canvas(str(OUTPUT_PDF), pagesize=A4)
    cv.setTitle("Catalogo de Calzado")
    cv.setAuthor("Catalogo Zapatos")

    # Preparar metadata para el indice
    productos_info = []
    for prod in productos:
        base = prod["filas"][0]
        productos_info.append({
            "nombre":    val(base.get("producto", "")) or "Producto",
            "ref":       val(base.get("ref_modelo", "")),
            "categoria": val(base.get("categoria_completa", "")) or "Sin categoria",
            "dest":      dest_name(val(base.get("ref_modelo", ""))),
        })

    # 1. Portada
    dibujar_portada(cv)

    # 2. Pagina(s) de indice
    dibujar_indice(cv, productos_info)

    # 3. Agrupar en paginas y calcular photo_h optimo por pagina
    paginas = agrupar_en_paginas(productos)

    for pagina in paginas:
        ph = PHOTO_W

        cursor_y      = PAGE_H - MARGIN
        first_on_page = True

        for prod in pagina:
            bh   = calcular_bloque_h_con_ph(prod["carpetas_hd"], ph)
            base = prod["filas"][0]
            dest = dest_name(val(base.get("ref_modelo", "")))

            bloque_y = cursor_y - bh
            cv.bookmarkHorizontal(dest, 0, cursor_y)

            dibujar_bloque(cv, prod["filas"], prod["carpetas_hd"],
                           MARGIN, bloque_y, bh,
                           is_first_on_page=first_on_page,
                           photo_h=ph)

            cursor_y      = bloque_y - GAP_BLK
            first_on_page = False

        cv.showPage()

    cv.save()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

# Cuantos modelos procesar (None = todos)
MODELOS_A_PROCESAR = None


def cargar_producto(rows: list, ref: str):
    """Busca carpetas HD y devuelve el dict de producto, o None si no hay imagenes."""
    filas = [r for r in rows if r["ref_modelo"].strip() == ref]
    if not filas:
        return None
    nums = [n.strip() for n in ref.split("-")]
    carpetas_hd = {}
    for num in nums:
        hd = buscar_hd(ROOT_DIR, num)
        if hd:
            carpetas_hd[num] = hd
    if not carpetas_hd:
        print(f"  [WARN] {ref}: sin carpetas HD, se omite.")
        return None
    imgs_total = sum(len(imagenes_en_hd(hd)) for hd in carpetas_hd.values())
    print(f"  OK  {filas[0]['producto']:<30}  SKU: {ref:<10}  "
          f"{len(carpetas_hd)} carpeta(s)  {imgs_total} fotos")
    return {"filas": filas, "carpetas_hd": carpetas_hd}


def main():
    print(f"Leyendo inventario: {INVENTARIO}")
    rows = leer_inventario(INVENTARIO)
    if not rows:
        print("El inventario esta vacio.")
        return

    refs_vistos: dict = {}
    for row in rows:
        ref = row["ref_modelo"].strip()
        if ref not in refs_vistos:
            refs_vistos[ref] = True

    refs = list(refs_vistos.keys())
    if MODELOS_A_PROCESAR is not None:
        refs = refs[:MODELOS_A_PROCESAR]

    print(f"\nProcesando {len(refs)} modelos:\n")
    productos = []
    for ref in refs:
        prod = cargar_producto(rows, ref)
        if prod:
            productos.append(prod)

    if not productos:
        print("Sin productos con imagenes. Abortando.")
        return

    print(f"\nGenerando PDF: {OUTPUT_PDF}  ({len(productos)} modelos)")
    generar_catalogo(productos)
    print("Listo.")


if __name__ == "__main__":
    main()
