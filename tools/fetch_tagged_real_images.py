from __future__ import annotations

import hashlib
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "giao_trinh_nha_vuon_nghi_duong"
IMAGE_DIR = COURSE / "assets" / "images"
DATA_DIR = COURSE / "assets" / "data"
ATTRIBUTION_PATH = DATA_DIR / "real-image-attributions.json"


TAGS = {
    "hero": ("tropical,garden,villa,resort", 9001),
    "01": ("tropical,garden,villa,landscape", 1001),
    "02": ("aerial,landscape,garden,site", 1002),
    "03": ("garden,path,terrace,seating", 1003),
    "04": ("tropical,house,veranda,architecture", 1004),
    "05": ("house,garden,terrace,veranda", 1005),
    "06": ("tropical,plants,garden,botanical", 1006),
    "07": ("rain,garden,drainage,irrigation", 1007),
    "08": ("stone,wood,architecture,material", 1008),
    "09": ("garden,lighting,night,landscape", 1009),
    "10": ("mature,garden,landscape,trees", 1010),
    "11": ("architect,meeting,design,studio", 1011),
    "12": ("materials,design,architecture", 702),
    "13": ("construction,planning,project,meeting", 1013),
    "14": ("architecture,presentation,board,design", 1014),
    "15": ("land,survey,construction,site", 1015),
    "16": ("landscape,architecture,model,concept", 1016),
    "17": ("architecture,model,design,studio", 1017),
    "18": ("blueprint,architecture,drawing", 501),
    "19": ("construction,budget,documents,planning", 1019),
    "20": ("architecture,material,samples,stone", 1020),
    "21": ("construction,team,meeting,contract", 1021),
    "22": ("construction,site,safety,workers", 1022),
    "23": ("house,construction,concrete,structure", 1023),
    "24": ("landscape,construction,planting,irrigation", 1024),
    "25": ("building,inspection,construction,checklist", 1025),
    "26": ("garden,maintenance,pruning,irrigation", 1026),
    "27": ("architect,client,workshop,programming", 1027),
    "28": ("urban,planning,documents,permit", 1028),
    "29": ("floorplan,architecture,drawing", 901),
    "30": ("architectural,model,section,plan", 1030),
    "31": ("architecture,shading,louvers,tropical", 1031),
    "32": ("mechanical,electrical,plumbing,building", 1032),
    "33": ("roof,waterproofing,construction,material", 1033),
    "34": ("construction,inspection,drawings,architecture", 1034),
}


def image_url(tags: str, lock: int) -> str:
    escaped = urllib.parse.quote(tags, safe=",")
    return f"https://loremflickr.com/1400/900/{escaped}/all?lock={lock}"


def download(url: str) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "CodexCourseVisualUpgrade/1.0"})
    with urllib.request.urlopen(req, timeout=45) as response:
        final_url = response.geturl()
        return response.read(), final_url


def main() -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    used_hashes: set[str] = set()
    attributions: dict[str, dict[str, str]] = {}

    for key, (tags, base_lock) in TAGS.items():
        filename = "hero-garden-real.jpg" if key == "hero" else f"module-{key}-photo.jpg"
        out = IMAGE_DIR / filename
        parts = tags.split(",")
        fallback = "construction,architecture" if key >= "21" else "garden,architecture"
        tag_options = [tags, ",".join(parts[:3]), ",".join(parts[:2]), parts[0], fallback]
        saved = False
        for option_index, tag_option in enumerate(dict.fromkeys(tag_options)):
            for offset in range(20):
                lock = base_lock + option_index * 10000 + offset * 97
                url = image_url(tag_option, lock)
                try:
                    data, final_url = download(url)
                except Exception as exc:
                    print(f"{key}: skip tags={tag_option} lock={lock}: {exc}", flush=True)
                    continue
                digest = hashlib.sha256(data).hexdigest()
                if digest in used_hashes:
                    continue
                used_hashes.add(digest)
                out.write_bytes(data)
                attributions[key] = {
                    "file": str(out.relative_to(COURSE)),
                    "title": f"Tagged Flickr photo for {tag_option}",
                    "source_url": url,
                    "direct_url": final_url,
                    "provider": "loremflickr/flickr",
                    "license": "Flickr tagged image via LoremFlickr",
                    "tags": tag_option,
                    "lock": str(lock),
                    "sha256": digest,
                }
                print(f"{key}: saved {filename} tags={tag_option} lock={lock}", flush=True)
                saved = True
                break
            if saved:
                break
        if not saved:
            raise RuntimeError(f"Could not find unique image for {key}: {tags}")
        time.sleep(0.4)

    ATTRIBUTION_PATH.write_text(json.dumps(attributions, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {ATTRIBUTION_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
