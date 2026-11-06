"""Compose the Argus README banner: brand icon on a dark gradient with headline."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "assets" / "brand"

BANNER_W, BANNER_H = 1600, 420
SAGE = (155, 196, 154)          # matches logo sage green
DARK_TOP = (9, 17, 13)          # near-black green
DARK_BOT = (22, 58, 41)         # deep brand green


def make_transparent(img: Image.Image, thresh: int = 40) -> Image.Image:
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    # flood-fill background from the four corners using the corner color itself
    for cx, cy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        ImageDraw.floodfill(img, (cx, cy), (0, 0, 0, 0), thresh=thresh)
    return img


def extract_icon() -> Image.Image:
    logo = make_transparent(Image.open(BRAND / "argus-logo-dark.png"))
    w, h = logo.size
    # find the empty gap separating the icon from the "ARGUS" wordmark:
    # walk columns left→right and cut at the first wide empty run after content
    gap_start, run, seen = w, 0, False
    for x in range(w):
        col_has_ink = any(logo.getpixel((x, y))[3] > 10 for y in range(0, h, 8))
        seen = seen or col_has_ink
        if seen and not col_has_ink:
            run += 1
            if run > 30:
                gap_start = x - run
                break
        else:
            run = 0
    icon = logo.crop((0, 0, gap_start, h))
    return icon.crop(icon.getbbox())


def gradient(w: int, h: int) -> Image.Image:
    base = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(base)
    for y in range(h):
        t = y / h
        c = tuple(int(DARK_TOP[i] + (DARK_BOT[i] - DARK_TOP[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c + (255,))
    return base


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    for name in (["segoeuib", "arialbd"] if bold else ["segoeui", "arial"]):
        try:
            return ImageFont.truetype(f"C:/Windows/Fonts/{name}.ttf", size)
        except OSError:
            continue
    return ImageFont.load_default()


def main() -> None:
    icon = extract_icon()
    banner = gradient(BANNER_W, BANNER_H)

    side = int(BANNER_H * 0.74)
    icon = icon.resize((side, int(side * icon.height / icon.width)), Image.LANCZOS)
    ix, iy = 90, (BANNER_H - icon.height) // 2
    banner.alpha_composite(icon, (ix, iy))

    d = ImageDraw.Draw(banner)
    tx = ix + icon.width + 70
    avail = BANNER_W - tx - 60

    head = "The hundred-eyed steward"
    size = 88
    while d.textlength(head, font=font(size)) > avail:
        size -= 4
    d.text((tx, 118), head, font=font(size), fill=(245, 248, 245))

    sub = "for your UGREEN AI NAS"
    sub_size = int(size * 0.62)
    while d.textlength(sub, font=font(sub_size, bold=False)) > avail:
        sub_size -= 4
    d.text((tx + 4, 250), sub, font=font(sub_size, bold=False), fill=SAGE)
    d.text(
        (tx + 6, 332),
        "audits  ·  proposes  ·  remembers  ·  undoes",
        font=font(28, bold=False),
        fill=(196, 214, 197),
    )

    out = BRAND / "argus-banner-dark.png"
    banner.convert("RGB").save(out, optimize=True)
    print(f"{out.name}: {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
