#!/usr/bin/env python3
"""Read-only PNG inspection; write the engine manifest and offline preview catalog."""
import hashlib
import json
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EXPRESSIONS = {
    "neutral": "日常", "smile": "喜悦", "shy": "害羞",
    "surprised": "惊讶", "serious": "认真", "sad": "落泪",
}
CHARACTERS = {"natsumi": "夏澄", "mio": "澪"}
BACKGROUNDS = {
    "seawall_day": "海堤 / 晴日",
    "seawall_sunset": "海堤 / 夕照",
    "cafe_day": "咖啡馆 / 晴日",
    "cafe_rain": "咖啡馆 / 雨天",
    "station_dusk": "旧车站 / 黄昏",
    "bedroom_night": "旧居卧室 / 夜晚",
    "observatory_exterior": "天文台外 / 蓝调时刻",
    "observatory_interior": "天文台内 / 星夜",
}


def expected_assets():
    result = []
    for character, name in CHARACTERS.items():
        result.append(dict(
            id=f"{character}_reference", category="design",
            label=f"{name} · 角色设计", path=f"assets/design/{character}_reference.png",
            character=character,
        ))
    for character, name in CHARACTERS.items():
        for expression, label in EXPRESSIONS.items():
            result.append(dict(
                id=f"{character}_{expression}", category="character",
                label=f"{name} · {label}",
                path=f"assets/characters/{character}/{expression}.png",
                character=character, expression=expression,
            ))
    for identifier, label in BACKGROUNDS.items():
        result.append(dict(
            id=identifier, category="background", label=label,
            path=f"assets/backgrounds/{identifier}.png",
        ))
    for identifier, label in {
        "natsumi_letter": "夏澄 · 海玻璃来信",
        "mio_stargazing": "澪 · 观星之约",
    }.items():
        result.append(dict(
            id=identifier, category="cg", label=label,
            path=f"assets/cg/{identifier}.png",
        ))
    result.append(dict(
        id="tide_letters_keyvisual", category="keyart", label="潮汐来信 · 双人主视觉",
        path="assets/keyart/tide_letters_keyvisual.png",
    ))
    return result


def inspect(asset):
    path = ROOT / asset["path"]
    if not path.is_file():
        raise ValueError(f"Missing asset: {asset['path']}")
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        image.load()
        character = asset["category"] == "character"
        expected_size = (1024, 1536) if character else (1536, 1024)
        if image.format != "PNG" or image.size != expected_size:
            raise ValueError(f"Unexpected format/size: {path.name}: {image.format} {image.size}")
        has_alpha = "A" in image.getbands()
        asset.update(width=image.width, height=image.height,
                     mode=image.mode, has_alpha=has_alpha)
        if character:
            if image.mode != "RGBA":
                raise ValueError(f"Sprite requires RGBA: {path}")
            alpha = image.getchannel("A")
            low, high = alpha.getextrema()
            # Tool exports may top out at 253/254 rather than exactly 255.
            if low != 0 or high < 240:
                raise ValueError(f"Invalid sprite opacity range: {path}: {low, high}")
            corners = [(0, 0), (image.width-1, 0),
                       (0, image.height-1), (image.width-1, image.height-1)]
            if any(alpha.getpixel(point) != 0 for point in corners):
                raise ValueError(f"Sprite corner is not transparent: {path}")
            histogram = alpha.histogram()
            fraction = sum(histogram[200:]) / (image.width * image.height)
            if not .1 < fraction < .8:
                raise ValueError(f"Unexpected opaque occupancy: {path}: {fraction}")
            # Threshold is used only for measurement, never to modify the asset.
            bounds = alpha.point(lambda value: 255 if value >= 200 else 0).getbbox()
            asset.update(alpha_range=[low, high], opaque_bounds=list(bounds),
                         opaque_fraction=round(fraction, 5),
                         suggested_anchor=[.5, 1.0])
        else:
            asset.update(suggested_fit="cover", suggested_position=[.5, .5],
                         source_aspect_ratio="3:2", preview_aspect_ratio="16:9")
    asset.update(bytes=path.stat().st_size,
                 sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                 source="OpenAI built-in image_gen")
    return asset


def main():
    assets = [inspect(asset) for asset in expected_assets()]
    expected = {asset["path"] for asset in assets}
    actual = {str(path.relative_to(ROOT)) for path in (ROOT / "assets").rglob("*.png")}
    if actual != expected:
        raise ValueError(f"Unexpected PNGs: {sorted(actual - expected)}")
    hashes = [asset["sha256"] for asset in assets]
    if len(set(hashes)) != len(hashes):
        raise ValueError("Duplicate image content found")
    catalog = dict(
        schema_version=1, title="潮汐来信", english_title="Letters of the Tide",
        generated_date="2026-11-22", asset_count=len(assets),
        total_bytes=sum(asset["bytes"] for asset in assets),
        counts=dict(Counter(asset["category"] for asset in assets)),
        notes=["All PNGs are original unmodified tool outputs.",
               "Sprites are independent full images; pixel-perfect face alignment is not guaranteed.",
               "Landscape source is 3:2; the preview crops the center to 16:9."],
        assets=assets,
    )
    encoded = json.dumps(catalog, ensure_ascii=False, indent=2) + "\n"
    (ROOT / "assets/manifest.json").write_text(encoded, encoding="utf-8")
    (ROOT / "preview/catalog.js").write_text(
        "// Generated by scripts/audit_assets.py.\nwindow.ART_CATALOG = " + encoded.rstrip() + ";\n",
        encoding="utf-8",
    )
    print(f"PASS: {len(assets)} unique valid PNGs; {catalog['total_bytes']/1024/1024:.1f} MiB")
    print(json.dumps(catalog["counts"], ensure_ascii=False))
    print("12 sprites: portrait size, real Alpha transparency, clear corners and occupancy verified.")


if __name__ == "__main__":
    main()
