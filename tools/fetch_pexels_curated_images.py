from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "giao_trinh_nha_vuon_nghi_duong"
IMAGE_DIR = COURSE / "assets" / "images"
DATA_DIR = COURSE / "assets" / "data"
ATTRIBUTION_PATH = DATA_DIR / "real-image-attributions.json"


PEXELS_IDS = {
    "hero": ("13914273", "Tropical villa pool and garden"),
    "01": ("33581364", "Tropical garden pathway leading to villa"),
    "02": ("30840332", "Tropical garden landscape with palm trees"),
    "03": ("16371355", "Outdoor garden lounge and terrace"),
    "04": ("36107525", "Tropical villa with wooden architecture"),
    "05": ("36183959", "Tropical villa with lush garden"),
    "06": ("16371439", "Tropical garden vegetation and planting"),
    "07": ("29494947", "Rainy lush tropical garden"),
    "08": ("31688478", "Stone and wood architectural material"),
    "09": ("18473577", "Decorative garden lighting at night"),
    "10": ("30338212", "Scenic mature tropical garden"),
    "11": ("3862135", "Engineers reviewing project blueprints"),
    "12": ("6615229", "Architectural sketches and workspace"),
    "13": ("19386931", "Construction project site activity"),
    "14": ("23496705", "Team discussing architectural blueprints"),
    "15": ("4575150", "Site preparation and field work"),
    "16": ("8680960", "Thatched tropical house in greenery"),
    "17": ("35767028", "Villa architecture with garden setting"),
    "18": ("34573691", "Detailed architectural blueprints on desk"),
    "19": ("6474206", "Construction materials and planning"),
    "20": ("13213841", "Stone and wood material palette"),
    "21": ("6285152", "Architects reviewing blueprints"),
    "22": ("24889953", "Construction workers with safety gear"),
    "23": ("11580364", "Building construction structure"),
    "24": ("9026149", "Building materials on construction site"),
    "25": ("34670929", "Construction workers in safety gear"),
    "26": ("32363063", "Tropical garden for maintenance planning"),
    "27": ("9049745", "People discussing house blueprints"),
    "28": ("5582870", "Architect analyzing plans"),
    "29": ("6615098", "Architect working on floor plans"),
    "30": ("31120870", "Architects reviewing drawings"),
    "31": ("35793502", "Pathway lighting and shading mood"),
    "32": ("37198883", "Engineering team reviewing blueprint"),
    "33": ("11806490", "Tile and construction detail"),
    "34": ("8961027", "Construction inspection with plans"),
}


def pexels_image_urls(photo_id: str) -> list[str]:
    return [
        f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.{ext}?auto=compress&cs=tinysrgb&w=1600"
        for ext in ("jpeg", "jpg", "png", "webp")
    ]


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "CodexCourseVisualUpgrade/1.0"})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read()


def download_pexels_photo(photo_id: str) -> tuple[bytes, str]:
    last_error: Exception | None = None
    for url in pexels_image_urls(photo_id):
        try:
            return download(url), url
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code != 404:
                raise
    raise RuntimeError(f"Could not download Pexels photo {photo_id}") from last_error


def main() -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    attributions: dict[str, dict[str, str]] = {}
    hashes: dict[str, str] = {}

    for key, (photo_id, title) in PEXELS_IDS.items():
        filename = "hero-garden-real.jpg" if key == "hero" else f"module-{key}-photo.jpg"
        out = IMAGE_DIR / filename
        data, url = download_pexels_photo(photo_id)
        digest = hashlib.sha256(data).hexdigest()
        if digest in hashes:
            raise RuntimeError(f"Duplicate image hash: {key} duplicates {hashes[digest]}")
        hashes[digest] = key
        out.write_bytes(data)
        attributions[key] = {
            "file": str(out.relative_to(COURSE)),
            "title": title,
            "source_url": f"https://www.pexels.com/photo/{photo_id}/",
            "direct_url": url,
            "provider": "Pexels",
            "license": "Pexels free-use image",
            "photo_id": photo_id,
            "sha256": digest,
        }
        print(f"{key}: saved {filename} from Pexels {photo_id}", flush=True)
        time.sleep(0.25)

    ATTRIBUTION_PATH.write_text(json.dumps(attributions, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {ATTRIBUTION_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
