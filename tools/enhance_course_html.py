from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "giao_trinh_nha_vuon_nghi_duong"
HTML_PATH = COURSE / "giao_trinh_hoan_chinh.html"
ASSET_DIR = COURSE / "assets"
IMAGE_DIR = ASSET_DIR / "images"
DIAGRAM_DIR = ASSET_DIR / "diagrams"
DATA_DIR = ASSET_DIR / "data"
ATTRIBUTION_PATH = DATA_DIR / "real-image-attributions.json"


MODULES = [
    ("01", "tu-duy-nen-tang", "Tư Duy Nền Tảng", "Hệ sống", "nhà, vườn, người dùng và bảo trì", ["Hệ sống", "Chất lượng sống", "Bảo trì"]),
    ("02", "doc-khu-dat", "Đọc Khu Đất", "Bản đồ khu đất", "nắng, gió, nước, đất, view và riêng tư", ["Nắng", "Gió", "Nước"]),
    ("03", "trai-nghiem-con-nguoi", "Trải Nghiệm Con Người", "Journey map", "hành trình, điểm dừng và nhịp mở-kín", ["Hành trình", "Điểm dừng", "Mở-kín"]),
    ("04", "kien-truc-nhiet-doi", "Kiến Trúc Nhiệt Đới", "Mặt cắt khí hậu", "mái, hiên, thông gió, kính và mưa tạt", ["Mái", "Hiên", "Thông gió"]),
    ("05", "quan-he-nha-va-vuon", "Quan Hệ Nhà Và Vườn", "Liên kết trong-ngoài", "cửa, hiên, sân, cây và khung nhìn", ["Hiên", "Sân", "Khung nhìn"]),
    ("06", "cay-xanh-nhieu-tang", "Cây Xanh Nhiều Tầng", "Tầng cây", "cây chủ, tầng cao, trung, bụi, nền và khoảng mở", ["Cây chủ", "Tầng cây", "Khoảng mở"]),
    ("07", "dat-nuoc-thoat-nuoc-tuoi", "Đất, Nước Và Tưới", "Dòng nước", "cao độ, thoát nước, bồn cây và vùng tưới", ["Cao độ", "Thoát nước", "Tưới"]),
    ("08", "vat-lieu-mau-sac-chat-cam", "Vật Liệu Và Chất Cảm", "Moodboard", "đá, gỗ, bê tông, gạch, cây và màu nền", ["Vật liệu", "Màu", "Chất cảm"]),
    ("09", "anh-sang-am-thanh-mui-huong", "Giác Quan", "Đêm và giác quan", "ánh sáng, âm thanh, mùi hương và cảm giác ở lại", ["Ánh sáng", "Âm thanh", "Mùi hương"]),
    ("10", "thoi-gian-va-bao-tri", "Thời Gian Và Bảo Trì", "Vườn trưởng thành", "các mốc 6 tháng, 1 năm, 3 năm, 5 năm", ["1 năm", "3 năm", "5 năm"]),
    ("11", "quy-trinh-lam-viec", "Quy Trình Làm Việc", "Process map", "vai trò của chủ nhà, thiết kế, thi công và bảo trì", ["Vai trò", "Duyệt", "Phối hợp"]),
    ("12", "brief-thiet-ke", "Brief Thiết Kế", "Template brief", "nhu cầu, khu đất, ngân sách, phong cách và vận hành", ["Nhu cầu", "Ngân sách", "Vận hành"]),
    ("13", "tong-quan-lo-trinh-trien-khai-du-an", "Lộ Trình Dự Án", "Roadmap", "brief, khảo sát, concept, kỹ thuật, thi công và bảo trì", ["Brief", "Concept", "Thi công"]),
    ("14", "brief-trien-khai-va-yeu-cau-dau-bai", "Brief Triển Khai", "Đầu bài", "phạm vi, yêu cầu, ưu tiên và ranh giới trách nhiệm", ["Phạm vi", "Ưu tiên", "Trách nhiệm"]),
    ("15", "khao-sat-hien-trang-phap-ly-do-dac-ha-tang", "Khảo Sát Hiện Trạng", "Checklist khảo sát", "pháp lý, đo đạc, cây, hạ tầng và thi công", ["Pháp lý", "Đo đạc", "Hạ tầng"]),
    ("16", "concept-tong-the-nha-vuon", "Concept Tổng Thể", "Concept board", "zoning, mood, view, vật liệu và cây chủ", ["Zoning", "Mood", "Cây chủ"]),
    ("17", "thiet-ke-co-so-va-phuong-an-thiet-ke", "Thiết Kế Cơ Sở", "So sánh phương án", "phương án A/B/C và tiêu chí duyệt", ["A/B/C", "Tradeoff", "Duyệt"]),
    ("18", "ho-so-ky-thuat-kien-truc-ket-cau-mep-canh-quan", "Hồ Sơ Kỹ Thuật", "Bộ hồ sơ", "kiến trúc, kết cấu, MEP và cảnh quan", ["Kiến trúc", "MEP", "Cảnh quan"]),
    ("19", "du-toan-boq-pham-vi-cong-viec-ngan-sach", "Dự Toán Và BOQ", "Ngân sách", "nhóm chi phí, phạm vi công việc và dự phòng", ["BOQ", "Phạm vi", "Dự phòng"]),
    ("20", "mau-mockup-vat-lieu-cay-thiet-bi-duyet-mau", "Duyệt Mẫu", "Sample gallery", "vật liệu, cây, thiết bị, mockup và mẫu thực địa", ["Mẫu", "Mockup", "Duyệt"]),
    ("21", "lua-chon-doi-ngu-hop-dong-tien-do-quan-ly-thay-doi", "Đội Ngũ Và Hợp Đồng", "Timeline quản lý", "hợp đồng, tiến độ, thay đổi và cổng duyệt", ["Hợp đồng", "Tiến độ", "Thay đổi"]),
    ("22", "chuan-bi-thi-cong-quan-ly-hien-truong-an-toan-chat-luong", "Chuẩn Bị Thi Công", "Hiện trường", "tổ chức công trường, an toàn và chất lượng", ["Công trường", "An toàn", "QC"]),
    ("23", "thi-cong-phan-nha-tho-hoan-thien-he-thong-ky-thuat", "Thi Công Phần Nhà", "Chuỗi thi công nhà", "móng, thô, hoàn thiện và hệ thống kỹ thuật", ["Móng", "Thô", "MEP"]),
    ("24", "thi-cong-canh-quan-dat-nuoc-cay-tuoi-den-vat-lieu-ngoai-troi", "Thi Công Cảnh Quan", "Chuỗi cảnh quan", "đất, cây, tưới, đèn, nước và vật liệu ngoài trời", ["Đất", "Cây", "Đèn"]),
    ("25", "nghiem-thu-ban-giao-van-hanh-thu-ho-so-hoan-cong", "Nghiệm Thu Bàn Giao", "Flow bàn giao", "nghiệm thu, vận hành thử và hồ sơ hoàn công", ["Nghiệm thu", "Chạy thử", "Hồ sơ"]),
    ("26", "bao-tri-theo-doi-sau-ban-giao-kich-ban-1-3-5-nam", "Theo Dõi Sau Bàn Giao", "Dashboard bảo trì", "theo dõi 1-3-5 năm và điều chỉnh vận hành", ["1-3-5", "Theo dõi", "Bảo trì"]),
    ("27", "nhiem-vu-thiet-ke-nha-va-chuan-dau-vao-du-an", "Nhiệm Vụ Thiết Kế Nhà", "Chuẩn đầu vào", "người dùng, hoạt động, giới hạn và đầu ra", ["Đầu vào", "Nhiệm vụ", "Đầu ra"]),
    ("28", "phap-ly-quy-hoach-giay-phep-va-gioi-han-thiet-ke", "Pháp Lý Và Quy Hoạch", "Khung pháp lý", "chỉ giới, mật độ, tầng cao, giấy phép và hạ tầng", ["Chỉ giới", "Mật độ", "Giấy phép"]),
    ("29", "cong-nang-zoning-va-ma-tran-quan-he-phong", "Công Năng Và Zoning", "Bubble diagram", "zoning chung-riêng, quan hệ phòng và luồng đi", ["Zoning", "Ma trận", "Luồng đi"]),
    ("30", "mat-bang-mat-cat-cao-do-va-to-chuc-hinh-khoi", "Mặt Bằng Mặt Cắt", "Không gian 2D/3D", "mặt bằng, mặt cắt, cao độ và khối tích", ["Mặt bằng", "Mặt cắt", "Cao độ"]),
    ("31", "thiet-ke-khi-hau-cho-vo-nha-mai-hien-cua-kinh-lam", "Vỏ Nhà Khí Hậu", "Lớp vỏ nhà", "mái, hiên, cửa, kính, lam và che nắng", ["Mái", "Kính", "Lam"]),
    ("32", "phoi-hop-ket-cau-mep-va-ky-thuat-van-hanh", "Phối Hợp Kết Cấu MEP", "Coordination", "lưới cột, hộp kỹ thuật, thoát nước và bảo trì", ["Kết cấu", "MEP", "Vận hành"]),
    ("33", "vat-lieu-cau-tao-chong-tham-chong-nong-va-bao-tri", "Cấu Tạo Và Vật Liệu", "Chi tiết cấu tạo", "chống thấm, chống nóng, chống trơn và bảo trì", ["Chống thấm", "Chống nóng", "Bảo trì"]),
    ("34", "ho-so-thiet-ke-checklist-duyet-phuong-an-va-tieu-chuan-nghiem-thu", "Hồ Sơ Và Nghiệm Thu", "Ma trận duyệt", "hồ sơ, checklist, tiêu chuẩn và nghiệm thu", ["Hồ sơ", "Checklist", "Tiêu chuẩn"]),
]


PALETTES = [
    ("#153b2c", "#6fa66f", "#f1d38b", "#f7f3ea"),
    ("#17324d", "#6fa8b8", "#e8b86d", "#f6f0e6"),
    ("#3f3a2d", "#a8b56b", "#d68f61", "#f5efe2"),
    ("#233327", "#8dbf88", "#b99566", "#f8f4ec"),
]


def svg_text(text: str, x: int, y: int, size: int, color: str = "#173126", weight: int = 700) -> str:
    return f'<text x="{x}" y="{y}" font-family="Inter, Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(text)}</text>'


def cover_svg(module: tuple[str, str, str, str, str, list[str]], idx: int) -> str:
    num, _, title, visual, desc, tags = module
    dark, leaf, sun, paper = PALETTES[idx % len(PALETTES)]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" role="img" aria-labelledby="title desc">
<title id="title">Module {num}: {escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs><linearGradient id="sky" x1="0" x2="1" y1="0" y2="1"><stop stop-color="{paper}"/><stop offset=".55" stop-color="#dcebdc"/><stop offset="1" stop-color="{leaf}"/></linearGradient><filter id="soft"><feDropShadow dx="0" dy="16" stdDeviation="18" flood-color="#10251c" flood-opacity=".22"/></filter></defs>
<rect width="1280" height="720" fill="url(#sky)"/>
<circle cx="1040" cy="150" r="78" fill="{sun}" opacity=".9"/>
<path d="M0 520 C180 450 300 500 450 430 C610 360 760 410 900 340 C1050 265 1170 325 1280 250 L1280 720 L0 720 Z" fill="{dark}" opacity=".96"/>
<path d="M0 605 C180 565 330 590 505 530 C660 476 800 502 960 450 C1110 400 1210 420 1280 380 L1280 720 L0 720 Z" fill="{leaf}" opacity=".78"/>
<g filter="url(#soft)"><rect x="456" y="306" width="360" height="165" rx="10" fill="#fff8ea"/><path d="M420 315 L636 190 L855 315 Z" fill="{dark}"/><rect x="510" y="350" width="92" height="121" fill="#d8a75b"/><rect x="630" y="346" width="136" height="82" fill="#9fc6c5"/></g>
<path d="M220 460 C250 350 310 280 375 215 C340 320 355 396 430 480 Z" fill="#2f6b42"/><path d="M180 500 C170 385 205 306 270 230 C252 335 275 420 350 515 Z" fill="#5e9d5f"/>
<rect x="72" y="72" width="520" height="240" rx="26" fill="#fffdf6" opacity=".92"/>
{svg_text("MODULE " + num, 108, 128, 28, leaf, 800)}
{svg_text(title, 108, 190, 46, dark, 800)}
{svg_text(visual, 108, 242, 24, "#6f6047", 700)}
<text x="108" y="282" font-family="Inter, Arial, sans-serif" font-size="18" fill="#4b5b4b">{escape(desc)}</text>
<g>{''.join(f'<rect x="{108+i*128}" y="318" width="112" height="34" rx="17" fill="{dark}" opacity=".9"/><text x="{124+i*128}" y="341" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="700" fill="#fff">{escape(tag)}</text>' for i, tag in enumerate(tags))}</g>
</svg>'''


def diagram_svg(module: tuple[str, str, str, str, str, list[str]], idx: int) -> str:
    num, _, title, visual, desc, tags = module
    dark, leaf, sun, paper = PALETTES[(idx + 1) % len(PALETTES)]
    nodes = tags + [visual]
    x_positions = [165, 405, 645, 885]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="620" viewBox="0 0 1000 620" role="img" aria-labelledby="title desc">
<title id="title">Sơ đồ module {num}: {escape(visual)}</title><desc id="desc">{escape(desc)}</desc>
<rect width="1000" height="620" rx="28" fill="{paper}"/>
<rect x="48" y="48" width="904" height="524" rx="24" fill="#fffdf8" stroke="#d8d0be"/>
{svg_text("SƠ ĐỒ TRỌNG TÂM", 92, 112, 22, leaf, 800)}
{svg_text(title, 92, 164, 42, dark, 800)}
<text x="92" y="202" font-family="Inter, Arial, sans-serif" font-size="18" fill="#59685a">{escape(desc)}</text>
<path d="M130 400 C250 250 420 465 535 330 C650 190 770 320 875 235" fill="none" stroke="{leaf}" stroke-width="8" stroke-linecap="round" opacity=".42"/>
{''.join(f'<line x1="{x_positions[i]}" y1="365" x2="{x_positions[i+1]}" y2="365" stroke="{dark}" stroke-width="3" opacity=".25"/>' for i in range(3))}
{''.join(f'<g><circle cx="{x}" cy="365" r="64" fill="{leaf if i % 2 == 0 else sun}" opacity=".95"/><circle cx="{x}" cy="365" r="42" fill="#fffdf8" opacity=".72"/><text x="{x}" y="360" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-size="15" font-weight="800" fill="{dark}">{escape(label[:18])}</text><text x="{x}" y="384" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="700" fill="#5d594e">Lớp {i+1}</text></g>' for i, (x, label) in enumerate(zip(x_positions, nodes)))}
<rect x="92" y="486" width="816" height="50" rx="18" fill="{dark}" opacity=".92"/>
<text x="118" y="518" font-family="Inter, Arial, sans-serif" font-size="18" font-weight="700" fill="#fff">Dùng visual này để đọc nhanh logic trước khi đi vào bảng/checklist chi tiết.</text>
</svg>'''


def mood_svg(module: tuple[str, str, str, str, str, list[str]], idx: int) -> str:
    num, _, title, visual, _, tags = module
    dark, leaf, sun, paper = PALETTES[(idx + 2) % len(PALETTES)]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="560" viewBox="0 0 900 560" role="img" aria-labelledby="title">
<title id="title">Moodboard module {num}: {escape(title)}</title>
<rect width="900" height="560" fill="{paper}"/>
<rect x="42" y="42" width="816" height="476" rx="26" fill="#fffdf8"/>
<rect x="82" y="96" width="250" height="320" rx="18" fill="{dark}"/>
<rect x="358" y="96" width="190" height="150" rx="18" fill="{leaf}"/>
<rect x="574" y="96" width="244" height="150" rx="18" fill="{sun}"/>
<rect x="358" y="272" width="460" height="144" rx="18" fill="#d8d0be"/>
{svg_text("Moodboard", 82, 470, 26, dark, 800)}
{svg_text(title, 82, 502, 22, "#6f6047", 700)}
{''.join(f'<text x="{390+i*135}" y="470" font-family="Inter, Arial, sans-serif" font-size="18" font-weight="800" fill="{dark}">{escape(tag)}</text>' for i, tag in enumerate(tags))}
</svg>'''


def make_assets() -> dict[str, dict[str, object]]:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    DIAGRAM_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    visual_map: dict[str, dict[str, object]] = {}

    hero = '''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">
<title id="title">Nhà vườn nghỉ dưỡng nhiệt đới</title><desc id="desc">Nhà thấp tầng, hiên rộng, cây nhiều lớp và mặt nước trong ánh sáng nhiệt đới.</desc>
<defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#f8f1df"/><stop offset=".48" stop-color="#9fbf93"/><stop offset="1" stop-color="#16372a"/></linearGradient><filter id="d"><feDropShadow dx="0" dy="20" stdDeviation="24" flood-color="#06150f" flood-opacity=".25"/></filter></defs>
<rect width="1600" height="900" fill="url(#g)"/><circle cx="1260" cy="170" r="105" fill="#f1c46c" opacity=".9"/>
<path d="M0 620 C260 520 405 620 650 500 C880 390 1040 480 1260 350 C1420 255 1510 290 1600 240 L1600 900 L0 900 Z" fill="#193c2c"/>
<path d="M0 720 C260 650 470 720 710 620 C930 530 1160 610 1600 470 L1600 900 L0 900 Z" fill="#5d965f"/>
<g filter="url(#d)"><rect x="520" y="380" width="540" height="205" rx="10" fill="#fff5df"/><path d="M470 395 L790 220 L1110 395 Z" fill="#18382a"/><rect x="610" y="430" width="145" height="155" fill="#c99455"/><rect x="790" y="422" width="205" height="104" fill="#9fc6c5"/></g>
<path d="M170 650 C220 470 315 360 430 255 C380 430 430 560 560 700 Z" fill="#2f6b42"/><path d="M90 735 C75 545 135 395 250 270 C230 480 285 620 420 775 Z" fill="#6fa66f"/>
</svg>'''
    (IMAGE_DIR / "hero-garden.svg").write_text(hero, encoding="utf-8")

    attributions = {}
    if ATTRIBUTION_PATH.exists():
        attributions = json.loads(ATTRIBUTION_PATH.read_text(encoding="utf-8"))

    for idx, module in enumerate(MODULES):
        num, slug, title, visual, desc, tags = module
        cover = f"module-{num}-cover.svg"
        diagram = f"module-{num}-diagram.svg"
        mood = f"module-{num}-moodboard.svg"
        (IMAGE_DIR / cover).write_text(cover_svg(module, idx), encoding="utf-8")
        (DIAGRAM_DIR / diagram).write_text(diagram_svg(module, idx), encoding="utf-8")
        (IMAGE_DIR / mood).write_text(mood_svg(module, idx), encoding="utf-8")
        real_cover = next((p for p in sorted(IMAGE_DIR.glob(f"module-{num}-photo.*")) if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}), None)
        cover_path = f"assets/images/{cover}"
        cover_kind = "svg"
        source = None
        if real_cover:
            cover_path = str(real_cover.relative_to(COURSE))
            cover_kind = "real-photo"
            source = attributions.get(num, {})
        visual_map[f"module-{num}"] = {
            "title": title,
            "visual": visual,
            "caption": f"Visual trọng tâm: {visual.lower()} cho {desc}.",
            "cover": cover_path,
            "cover_kind": cover_kind,
            "source": source,
            "diagram": f"assets/diagrams/{diagram}",
            "gallery": [cover_path, f"assets/diagrams/{diagram}", f"assets/images/{mood}"],
            "tags": tags,
            "slug": slug,
        }

    (DATA_DIR / "visual-map.json").write_text(json.dumps(visual_map, ensure_ascii=False, indent=2), encoding="utf-8")
    return visual_map


ENHANCED_CSS = r'''body{margin:0;background:#eef1ed;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#18231c;line-height:1.65}.layout{display:grid;grid-template-columns:310px minmax(0,1fr)}aside{position:sticky;top:0;height:100vh;overflow:auto;padding:22px;background:#f7f5ef;border-right:1px solid #ded7c8}aside h1{font-size:22px;line-height:1.05;margin:0 0 8px}.search{width:100%;box-sizing:border-box;padding:12px 14px;border:1px solid #d7d0c1;border-radius:8px;background:#fffdf8}.filter-tabs{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin:14px 0}.filter-tabs button,.gallery-toggle{border:1px solid #d7d0c1;border-radius:8px;background:#fffdf8;color:#203428;padding:9px 10px;font-weight:750;cursor:pointer}.filter-tabs button.active{background:#18382a;color:#fff;border-color:#18382a}.nav-link{display:flex;justify-content:space-between;gap:10px;padding:10px 12px;border-radius:8px;text-decoration:none;color:#1d1d1f;border:1px solid transparent}.nav-link:hover,.nav-link.active{background:#fffdf8;border-color:#d9d0bf}.nav-link span{font-size:14px;font-weight:700;line-height:1.25}.nav-link small{font-size:11px;color:#6e756c;white-space:nowrap}.hero,.content{max-width:1180px;margin:0 auto;padding:56px}.visual-hero{position:relative;min-height:560px;display:grid;align-items:end;overflow:hidden;background:#173528;color:#fff;padding:0;max-width:none;margin:0}.visual-hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.9}.visual-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#102319e8 0%,#102319b3 43%,#10231933 100%)}.hero-panel{position:relative;z-index:1;max-width:920px;padding:76px 56px}.eyebrow,.module-kicker{font-size:12px;text-transform:uppercase;letter-spacing:.12em;font-weight:900;color:#8da66f}.visual-hero h2{font-size:clamp(44px,7vw,92px);line-height:.94;margin:14px 0 18px;max-width:850px}.visual-hero p{font-size:20px;max-width:720px;color:#f5efe2}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:32px}.stat,.doc-card{background:#fffdf8;border:1px solid #e1dacb;border-radius:8px;padding:22px;box-shadow:0 18px 45px #14201614}.visual-hero .stat{background:#fffdf8e8;color:#18382a;border-color:#fff8;backdrop-filter:blur(8px)}.visual-hero .stat span{color:#314339}.stat b{display:block;font-size:32px}.doc-card{padding:42px;margin:26px 0;position:relative;overflow:hidden}.doc-card::before{content:attr(data-progress);position:absolute;right:28px;top:22px;color:#d8d0be;font-size:14px;font-weight:900}.doc-meta{display:inline-block;background:#edf4e7;color:#36592f;border-radius:999px;padding:6px 10px;font-size:12px;font-weight:800}.chapter-title{font-size:clamp(32px,4vw,52px);line-height:1.05;margin-bottom:24px}.visual-header{display:grid;grid-template-columns:1fr;gap:0;margin:30px 0 38px;padding:0;background:#f8f4ec;border:1px solid #ddd3c1;border-radius:14px;overflow:hidden}.module-cover,.diagram-card,.module-gallery figure{margin:0}.module-cover{position:relative;background:#102319}.module-cover img,.diagram-card img,.module-gallery img{display:block;width:100%;border-radius:8px;background:#e8e0d0}.module-cover img{height:clamp(340px,45vw,520px);object-fit:cover;object-position:center;border-radius:0}.module-cover figcaption{position:absolute;left:22px;right:22px;bottom:18px;color:#fff;background:linear-gradient(90deg,#102319e0,#10231966);padding:12px 14px;border-radius:8px;font-size:14px;font-weight:750;margin:0}.diagram-card figcaption,.module-gallery figcaption{font-size:13px;color:#5e665d;margin-top:8px}.visual-summary{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:20px;padding:24px}.visual-summary h2{font-size:30px;line-height:1.08;margin:8px 0}.visual-summary p{margin:0}.visual-summary .diagram-card{grid-column:2;grid-row:1 / span 5}.visual-summary .gallery-toggle{justify-self:start;align-self:end}.concept-strip{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0}.concept-strip span{background:#18382a;color:#fff;border-radius:999px;padding:7px 10px;font-size:12px;font-weight:800}.image-grid{display:grid;grid-template-columns:1fr;gap:14px}.diagram-card{background:#fffdf8;border:1px solid #ded7c8;border-radius:8px;padding:12px}.module-gallery{grid-column:1 / -1;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:4px}.module-gallery[hidden]{display:none}.module-gallery figure{background:#fffdf8;border:1px solid #ded7c8;border-radius:8px;padding:10px}.module-gallery img{aspect-ratio:4/3;height:auto;object-fit:cover}.table-wrap{overflow:auto;border:1px solid #ddd3c1;border-radius:8px;margin:18px 0;background:#fff}table{width:100%;border-collapse:collapse;min-width:640px}th,td{padding:12px 14px;border-bottom:1px solid #eee7db;text-align:left;vertical-align:top}th{background:#f4efe4}blockquote{border-left:4px solid #6d8f4f;background:#edf4e7;padding:14px 18px;border-radius:8px}.diagram-shell{border:1px solid #ddd3c1;border-radius:8px;padding:18px;overflow:auto;background:#fffdf8}code{background:#f1ece2;padding:2px 6px;border-radius:6px}.tools{position:fixed;right:20px;bottom:20px;display:flex;gap:8px;z-index:20}.tools button{border:0;border-radius:999px;background:#18382a;color:white;padding:12px 16px;font-weight:800;box-shadow:0 12px 28px #10231929}.before-after,.process-timeline,.checklist-panel,.material-board{border:1px solid #ded7c8;border-radius:8px;background:#fffdf8;padding:18px;margin:18px 0}@media(max-width:1060px){.layout{grid-template-columns:280px minmax(0,1fr)}.hero,.content{padding:36px}.visual-hero{padding:0}.visual-summary{grid-template-columns:1fr}.visual-summary .diagram-card{grid-column:auto;grid-row:auto}.stats{grid-template-columns:repeat(2,1fr)}}@media(max-width:760px){.layout{display:block}aside{position:relative;height:auto}.hero,.content{padding:20px}.visual-hero{padding:0;min-height:620px}.hero-panel{padding:52px 24px}.visual-hero h2{font-size:44px}.stats,.module-gallery{grid-template-columns:1fr}.doc-card{padding:24px}.filter-tabs{grid-template-columns:1fr 1fr}.module-cover img{height:320px}.visual-summary{padding:18px}.module-cover figcaption{left:14px;right:14px;bottom:14px}}@media print{aside,.tools,.filter-tabs,.gallery-toggle{display:none!important}.layout{display:block}.visual-hero{min-height:auto;color:#18231c;background:#fff}.visual-hero img{display:none}.visual-hero::after{display:none}.hero-panel{padding:24px}.doc-card{box-shadow:none;border:1px solid #ddd;break-inside:avoid}.visual-header{break-inside:avoid;grid-template-columns:1fr}.module-cover img{height:auto;max-height:360px}.module-gallery{display:none!important}.table-wrap{break-inside:auto}img{max-width:100%;page-break-inside:avoid}}'''


def real_image_path(num: str) -> str:
    real_cover = next((p for p in sorted(IMAGE_DIR.glob(f"module-{num}-photo.*")) if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}), None)
    if real_cover:
        return str(real_cover.relative_to(COURSE))
    return f"assets/images/module-{num}-cover.svg"


def visual_header(module: tuple[str, str, str, str, str, list[str]], total: int) -> str:
    num, _, title, visual, desc, tags = module
    cover_src = real_image_path(num)
    tag_html = "".join(f"<span>{escape(tag)}</span>" for tag in tags)
    gallery = "".join(
        f'<figure><img src="{src}" loading="lazy" alt="{escape(title)} - hình trực quan {i}"><figcaption>{escape(label)}</figcaption></figure>'
        for i, (src, label) in enumerate(
            [
                (cover_src, "Ảnh thật bối cảnh"),
                (f"assets/diagrams/module-{num}-diagram.svg", "Sơ đồ trọng tâm"),
                (f"assets/images/module-{num}-moodboard.svg", "Moodboard mẫu"),
            ],
            start=1,
        )
    )
    return f'''<section class="visual-header" data-visual-module="{num}">
<figure class="module-cover"><img src="{cover_src}" loading="lazy" alt="Module {num}: {escape(title)}"><figcaption>{escape(visual)}: {escape(desc)}.</figcaption></figure>
<div class="visual-summary"><div class="module-kicker">Module {num} / {total}</div><h2>{escape(title)}</h2><p>Visual header này giúp đọc nhanh trọng tâm bài học qua {escape(desc)} trước khi đi vào bảng, checklist và bài tập.</p><div class="concept-strip">{tag_html}</div><figure class="diagram-card"><img src="assets/diagrams/module-{num}-diagram.svg" loading="lazy" alt="Sơ đồ trọng tâm module {num}: {escape(visual)}"><figcaption>Sơ đồ trọng tâm để chuyển nội dung lý thuyết thành logic nhìn được.</figcaption></figure><button class="gallery-toggle" type="button" aria-expanded="false">Hiện gallery trực quan</button><div class="module-gallery" hidden>{gallery}</div></div>
</section>'''


def enhance_html() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    html = re.sub(r"<style>.*?</style>", f"<style>{ENHANCED_CSS}</style>", html, count=1, flags=re.S)
    html = re.sub(r'<section class="visual-header"[\s\S]*?</section>', "", html)
    html = re.sub(r'<div class="filter-tabs"[\s\S]*?</div>', "", html)

    hero_src = "assets/images/hero-garden.svg"
    hero_real = next((p for p in sorted(IMAGE_DIR.glob("hero-garden-real.*")) if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}), None)
    if hero_real:
        hero_src = str(hero_real.relative_to(COURSE))
    hero = f'''<section class="hero visual-hero"><img src="{hero_src}" alt="Nhà vườn nghỉ dưỡng nhiệt đới với hiên rộng, cây nhiều lớp và mặt nước"><div class="hero-panel"><div class="eyebrow">Bản HTML thị giác</div><h2>Thiết kế nhà vườn như một hệ sống.</h2><p>Giáo trình được nâng cấp thành trải nghiệm học trực quan: mỗi module có ảnh thật không trùng lặp, sơ đồ trọng tâm, gallery minh họa, checklist và bảng vẫn giữ đầy đủ để tra cứu và in ấn.</p><div class="stats"><div class="stat"><b>34</b><span> module chuyên sâu</span></div><div class="stat"><b>35</b><span> ảnh thật bối cảnh</span></div><div class="stat"><b>18</b><span> phụ lục thực hành</span></div><div class="stat"><b>Static</b><span> HTML + assets</span></div></div></div></section>'''
    html = re.sub(r'<section class="hero(?: visual-hero)?">.*?</section><section class="content">', hero + '<section class="content">', html, count=1, flags=re.S)

    filters = '<div class="filter-tabs" role="group" aria-label="Lọc nhóm module"><button type="button" class="active" data-filter="all">Tất cả</button><button type="button" data-filter="foundation">Nền tảng</button><button type="button" data-filter="delivery">Triển khai</button><button type="button" data-filter="house">Phần nhà</button></div>'
    html = html.replace('<input id="search" class="search" placeholder="Tìm module, phụ lục, từ khóa...">', '<input id="search" class="search" placeholder="Tìm module, phụ lục, từ khóa...">' + filters, 1)

    total = len(MODULES)
    for idx, module in enumerate(MODULES, start=1):
        num, slug, *_ = module
        article_id = f"doc-modules-module-{num}-{slug}"
        group = "foundation" if int(num) <= 12 else "delivery" if int(num) <= 26 else "house"
        html = html.replace(f'<article class="doc-card" id="{article_id}">', f'<article class="doc-card" id="{article_id}" data-group="{group}" data-progress="{idx:02d}/{total}">', 1)
        html = html.replace(f'href="#{article_id}" data-title=', f'href="#{article_id}" data-group="{group}" data-title=', 1)
        pattern = rf'(<article class="doc-card" id="{re.escape(article_id)}"[^>]*>.*?<h1[^>]*>.*?</h1>)'
        html = re.sub(pattern, lambda m, module=module: m.group(1) + visual_header(module, total), html, count=1, flags=re.S)

    enhanced_js = r'''<script>const s=document.getElementById("search"),l=[...document.querySelectorAll(".nav-link")],c=[...document.querySelectorAll(".doc-card")],filters=[...document.querySelectorAll("[data-filter]")];let activeFilter="all";function applyFilters(){let q=(s?.value||"").toLowerCase();l.forEach(a=>{let group=a.dataset.group||"other",matchFilter=activeFilter==="all"||group===activeFilter,matchText=!q||a.dataset.title.includes(q);a.style.display=matchFilter&&matchText?"flex":"none"});c.forEach(x=>{let group=x.dataset.group||"other",matchFilter=activeFilter==="all"||group===activeFilter,matchText=!q||x.innerText.toLowerCase().includes(q);x.style.display=matchFilter&&matchText?"block":"none"})}s.oninput=applyFilters;filters.forEach(b=>b.onclick=()=>{activeFilter=b.dataset.filter;filters.forEach(x=>x.classList.toggle("active",x===b));applyFilters()});document.querySelectorAll(".gallery-toggle").forEach(btn=>btn.onclick=()=>{const gallery=btn.nextElementSibling,open=gallery.hasAttribute("hidden");gallery.toggleAttribute("hidden",!open);btn.setAttribute("aria-expanded",String(open));btn.textContent=open?"Ẩn gallery trực quan":"Hiện gallery trực quan"});const observer=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){l.forEach(a=>a.classList.toggle("active",a.getAttribute("href")==="#"+e.target.id))}})},{rootMargin:"-20% 0px -70% 0px"});c.forEach(card=>observer.observe(card));document.getElementById("top").onclick=()=>scrollTo({top:0,behavior:"smooth"});document.getElementById("print").onclick=()=>print();applyFilters()</script>'''
    html = re.sub(r"<script>const s=.*?</script></body></html>", enhanced_js + "</body></html>", html, count=1, flags=re.S)
    HTML_PATH.write_text(html, encoding="utf-8")


def main() -> None:
    make_assets()
    enhance_html()


if __name__ == "__main__":
    main()
