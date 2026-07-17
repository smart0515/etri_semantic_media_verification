import argparse
from pathlib import Path
from PIL import Image, ImageDraw


def main() -> None:
    parser = argparse.ArgumentParser(description="Create four-page PDF QA contact sheets.")
    parser.add_argument("source", nargs="?", default="tmp/pdfs/report")
    parser.add_argument("target", nargs="?", default="tmp/pdfs/contact")
    args = parser.parse_args()

    source = Path(args.source)
    target = Path(args.target)
    target.mkdir(parents=True, exist_ok=True)
    pages = sorted(source.glob("page-*.png"))
    for sheet_index in range(0, len(pages), 4):
        group = pages[sheet_index:sheet_index + 4]
        opened = [Image.open(path).convert("RGB") for path in group]
        width = max(image.width for image in opened)
        height = max(image.height for image in opened)
        canvas = Image.new("RGB", (width * 2 + 36, height * 2 + 60), "#d1d5db")
        draw = ImageDraw.Draw(canvas)
        for offset, (path, image) in enumerate(zip(group, opened)):
            x = 12 + (offset % 2) * (width + 12)
            y = 32 + (offset // 2) * (height + 12)
            canvas.paste(image, (x, y))
            draw.text((x, 8 + (offset // 2) * (height + 12)), path.stem, fill="#111827")
        canvas.save(target / f"contact-{sheet_index // 4 + 1:02d}.png")
    print(f"created {len(list(target.glob('contact-*.png')))} contact sheets")


if __name__ == "__main__":
    main()
