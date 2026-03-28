from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from PIL import Image
from PIL import ImageFilter


SCRIPT_DIR = Path(__file__).resolve().parent

TEMPLATES_DIR = SCRIPT_DIR / "Poster mod"

# Shoes root folder relative to this script folder
# Adjust the number of .. until it points to your Zapatos folder
SHOES_ROOT_DIR = (SCRIPT_DIR / ".." / ".." / ".." / "..").resolve()

# If you prefer fixed path, uncomment and use this:
# SHOES_ROOT_DIR = Path(r"C:\Users\table\Documents\Carlos\Personales\B\Zapatos")


@dataclass(frozen=True)
class Slot:
    x: int
    y: int
    w: int
    h: int
    glow: bool  # True or False

    def exists(self) -> bool:
        return self.w > 0 and self.h > 0


@dataclass(frozen=True)
class Fondo:
    name: str
    max_fotos: int
    slots: Tuple[Slot, Slot, Slot, Slot, Slot]

    def capacity(self) -> int:
        return sum(1 for s in self.slots if s.exists())

    def validate(self) -> None:
        cap = self.capacity()
        if cap != self.max_fotos:
            raise ValueError(
                "Template " + self.name + " max_fotos " + str(self.max_fotos) +
                " but slots " + str(cap) + " must match"
            )

    def path(self) -> Path:
        return TEMPLATES_DIR / self.name


def slot_center(slot):
    # New version uses cx,cy
    if hasattr(slot, "cx") and hasattr(slot, "cy"):
        return slot.cx, slot.cy
    # Old version uses x,y (assume those are center now)
    if hasattr(slot, "x") and hasattr(slot, "y"):
        return slot.x, slot.y
    raise AttributeError("Slot has no cx/cy or x/y")


def find_hd_folders(root: Path) -> List[Path]:
    return sorted([p for p in root.rglob("HD") if p.is_dir()])


def list_shoe_images(hd_dir: Path) -> List[Path]:
    pngs = sorted(hd_dir.glob("*.png"))
    pngs += sorted(hd_dir.glob("*.PNG"))
    return sorted(set(pngs), key=lambda p: p.name.lower())


def ensure_processed_dir(hd_dir: Path) -> Path:
    processed = hd_dir.parent / "Procesadas"
    processed.mkdir(parents=True, exist_ok=True)
    return processed


def load_image_rgba(path: Path) -> Image.Image:
    img = Image.open(path)
    return img.convert("RGBA")


def resize_contain(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    if target_w <= 0 or target_h <= 0:
        return img
    w, h = img.size
    if w <= 0 or h <= 0:
        return img
    scale = min(target_w / w, target_h / h)
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))
    return img.resize((new_w, new_h), Image.Resampling.LANCZOS)


def paste_center(bg, fg, slot, glow_radius=100, glow_intensity=255):
    fg_resized = resize_contain(fg, slot.w, slot.h)
    fw, fh = fg_resized.size

    cx, cy = slot_center(slot)

    top_left_x = cx - fw // 2
    top_left_y = cy - fh // 2

    do_glow = False
    if hasattr(slot, "glow"):
        do_glow = bool(slot.glow)

    if do_glow:
        mask = fg_resized.split()[-1]
        white_layer = Image.new("RGBA", fg_resized.size, (255, 255, 255, 0))
        white_layer.paste((255, 255, 255, glow_intensity), mask=mask)
        glow = white_layer.filter(ImageFilter.GaussianBlur(glow_radius))
        bg.alpha_composite(glow, (top_left_x, top_left_y))

    bg.alpha_composite(fg_resized, (top_left_x, top_left_y))


def chunk_with_reuse(items: List[Path], chunk_size: int) -> List[List[Path]]:
    if not items or chunk_size <= 0:
        return []

    n = len(items)
    total_groups = int(math.ceil(n / chunk_size))
    groups: List[List[Path]] = []

    for gi in range(total_groups):
        start = gi * chunk_size
        group = items[start:start + chunk_size]

        if len(group) < chunk_size:
            needed = chunk_size - len(group)
            reps: List[Path] = []
            idx = 0
            while len(reps) < needed:
                reps.append(items[idx % n])
                idx += 1
            group = group + reps

        groups.append(group)

    return groups


def render_post(fondo: Fondo, shoe_imgs: List[Path], out_path: Path) -> None:
    fondo_path = fondo.path()
    if not fondo_path.exists():
        raise FileNotFoundError("Missing template file " + str(fondo_path))

    bg = load_image_rgba(fondo_path)

    used = 0
    for slot in fondo.slots:
        if not slot.exists():
            continue
        if used >= len(shoe_imgs):
            break
        shoe = load_image_rgba(shoe_imgs[used])
        paste_center(bg, shoe, slot)
        used += 1

    bg.save(out_path, format="PNG")


def process_hd_folder(hd_dir: Path, fondo: Fondo, template_index: int) -> int:
    shoe_paths = list_shoe_images(hd_dir)
    if not shoe_paths:
        print("WARN no png in " + str(hd_dir))
        return 0

    processed_dir = ensure_processed_dir(hd_dir)
    cap = fondo.capacity()
    if cap <= 0:
        print("WARN template has no slots " + fondo.name)
        return 0

    groups = chunk_with_reuse(shoe_paths, cap)

    created = 0
    for i, group in enumerate(groups, start=1):
        out_name = hd_dir.parent.name + "_T" + str(template_index).zfill(2) + "_P" + str(i).zfill(2) + ".png"
        out_path = processed_dir / out_name
        render_post(fondo, group, out_path)
        created += 1

    return created


def build_fondos() -> List[Fondo]:
    Z = Slot(0, 0, 0, 0, 0)

    fondos = [
        Fondo(
            name="1.png",
            max_fotos=3,
            slots=(
                Slot(710, 1290, 550, 550, False),  # slot 1 (top left oval)
                Slot(715, 960, 450, 450, False), # slot 2 (middle right oval)
                Slot(715, 608, 450, 450, False), # slot 3 (bottom left oval)
                Z,
                Z,
            ),
        ),
        Fondo(
            name="11.png",
            max_fotos=3,
            slots=(
                Slot(333, 700, 600, 600, True),  # slot 1 (top left oval)
                Slot(750, 1131, 600, 600, False), # slot 2 (middle right oval)
                Slot(333, 1570, 600, 600, False), # slot 3 (bottom left oval)
                Z,
                Z,
            ),
        ),
        # Add more templates here until you have 20 total
        # Fondo(name="fondo02.png", max_fotos=5, slots=(...)),
    ]

    for f in fondos:
        f.validate()

    return fondos


def main() -> None:
    fondos = build_fondos()
    if len(fondos) < 1:
        raise RuntimeError("No templates defined")

    if not TEMPLATES_DIR.exists():
        raise FileNotFoundError("Templates folder not found " + str(TEMPLATES_DIR))

    if not SHOES_ROOT_DIR.exists():
        raise FileNotFoundError("Shoes root folder not found " + str(SHOES_ROOT_DIR))

    hd_folders = find_hd_folders(SHOES_ROOT_DIR)
    print("Found " + str(len(hd_folders)) + " HD folders in " + str(SHOES_ROOT_DIR))

    template_idx = 0
    for hd in hd_folders:
        fondo = fondos[template_idx % len(fondos)]
        created = process_hd_folder(hd, fondo, template_idx % len(fondos))
        print("OK " + str(hd) + " created " + str(created) + " images using " + fondo.name)
        template_idx += 1


if __name__ == "__main__":
    main()
