from __future__ import annotations

import re
from dataclasses import dataclass
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "giao_trinh_sketchup_d5_nha_vuon"
LESSON_DIR = COURSE / "bai_hoc"
OUTPUT = COURSE / "giao_trinh_hoan_chinh.html"


@dataclass
class Document:
    path: Path
    title: str
    kind: str
    week: int | None = None
    lesson: int | None = None


WEEK_TITLES = {
    1: "Làm chủ không gian 3D",
    2: "Tổng mặt bằng và cao độ",
    3: "Khối nhà, mái, hiên, cửa",
    4: "Sân vườn, nước, cây",
    5: "D5, vật liệu, thư viện",
    6: "Ánh sáng ngày-đêm",
    7: "Render ảnh",
    8: "Video và hồ sơ",
}


def lesson_week(lesson: int) -> int:
    return ((lesson - 1) // 5) + 1


def slugify(text: str) -> str:
    text = text.lower()
    replacements = {
        "đ": "d",
        "á": "a",
        "à": "a",
        "ả": "a",
        "ã": "a",
        "ạ": "a",
        "ă": "a",
        "ắ": "a",
        "ằ": "a",
        "ẳ": "a",
        "ẵ": "a",
        "ặ": "a",
        "â": "a",
        "ấ": "a",
        "ầ": "a",
        "ẩ": "a",
        "ẫ": "a",
        "ậ": "a",
        "é": "e",
        "è": "e",
        "ẻ": "e",
        "ẽ": "e",
        "ẹ": "e",
        "ê": "e",
        "ế": "e",
        "ề": "e",
        "ể": "e",
        "ễ": "e",
        "ệ": "e",
        "í": "i",
        "ì": "i",
        "ỉ": "i",
        "ĩ": "i",
        "ị": "i",
        "ó": "o",
        "ò": "o",
        "ỏ": "o",
        "õ": "o",
        "ọ": "o",
        "ô": "o",
        "ố": "o",
        "ồ": "o",
        "ổ": "o",
        "ỗ": "o",
        "ộ": "o",
        "ơ": "o",
        "ớ": "o",
        "ờ": "o",
        "ở": "o",
        "ỡ": "o",
        "ợ": "o",
        "ú": "u",
        "ù": "u",
        "ủ": "u",
        "ũ": "u",
        "ụ": "u",
        "ư": "u",
        "ứ": "u",
        "ừ": "u",
        "ử": "u",
        "ữ": "u",
        "ự": "u",
        "ý": "y",
        "ỳ": "y",
        "ỷ": "y",
        "ỹ": "y",
        "ỵ": "y",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "section"


def inline_markdown(text: str) -> str:
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def parse_table(lines: list[str], start: int) -> tuple[str, int]:
    rows: list[list[str]] = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|"):
        parts = [cell.strip() for cell in lines[i].strip().strip("|").split("|")]
        rows.append(parts)
        i += 1
    if len(rows) < 2:
        return "", start
    header = rows[0]
    body = rows[2:] if all(re.fullmatch(r":?-{3,}:?", c) for c in rows[1]) else rows[1:]
    html = ["<div class=\"table-wrap\"><table><thead><tr>"]
    html.extend(f"<th>{inline_markdown(cell)}</th>" for cell in header)
    html.append("</tr></thead><tbody>")
    for row in body:
        html.append("<tr>")
        for cell in row:
            html.append(f"<td>{inline_markdown(cell)}</td>")
        html.append("</tr>")
    html.append("</tbody></table></div>")
    return "".join(html), i


def markdown_to_html(markdown: str, article_id: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    list_stack: list[str] = []
    in_code = False
    code_lang = ""
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            out.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph = []

    def close_lists() -> None:
        while list_stack:
            out.append(f"</{list_stack.pop()}>")

    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            if not in_code:
                flush_paragraph()
                close_lists()
                in_code = True
                code_lang = stripped.removeprefix("```").strip()
                code_lines = []
            else:
                lang = f" language-{escape(code_lang)}" if code_lang else ""
                out.append(f"<pre><code class=\"{lang.strip()}\">{escape(chr(10).join(code_lines))}</code></pre>")
                in_code = False
            i += 1
            continue
        if in_code:
            code_lines.append(raw)
            i += 1
            continue

        if not stripped:
            flush_paragraph()
            close_lists()
            i += 1
            continue

        if stripped.startswith("|"):
            flush_paragraph()
            close_lists()
            table_html, next_i = parse_table(lines, i)
            if table_html:
                out.append(table_html)
                i = next_i
                continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_lists()
            level = len(heading.group(1))
            text = heading.group(2).strip()
            h_level = min(level + 1, 6)
            hid = f"{article_id}-{slugify(text)}"
            out.append(f"<h{h_level} id=\"{hid}\">{inline_markdown(text)}</h{h_level}>")
            i += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            close_lists()
            quote = stripped.lstrip(">").strip()
            out.append(f"<blockquote>{inline_markdown(quote)}</blockquote>")
            i += 1
            continue

        unordered = re.match(r"^[-*]\s+(.+)$", stripped)
        ordered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if unordered or ordered:
            flush_paragraph()
            tag = "ul" if unordered else "ol"
            if not list_stack or list_stack[-1] != tag:
                close_lists()
                out.append(f"<{tag}>")
                list_stack.append(tag)
            item = (unordered or ordered).group(1)
            out.append(f"<li>{inline_markdown(item)}</li>")
            i += 1
            continue

        paragraph.append(stripped)
        i += 1

    flush_paragraph()
    close_lists()
    if in_code:
        out.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
    return "\n".join(out)


def read_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return path.stem.replace("-", " ").title()


def collect_documents() -> list[Document]:
    docs = [
        Document(COURSE / "00_muc_luc_va_huong_dan_hoc.md", "Mục lục và hướng dẫn học", "guide"),
        Document(COURSE / "01_tieu_chuan_chat_luong_chung.md", "Tiêu chuẩn chất lượng chung", "standard"),
        Document(COURSE / "02_quy_uoc_dat_ten_file_va_to_chuc_du_an.md", "Quy ước tổ chức dự án", "standard"),
        Document(COURSE / "03_checklist_dau_ra_cuoi_khoa.md", "Checklist đầu ra cuối khóa", "standard"),
    ]
    for path in sorted(LESSON_DIR.glob("bai-*.md")):
        match = re.search(r"bai-(\d+)-", path.name)
        if not match:
            continue
        lesson = int(match.group(1))
        docs.append(Document(path, read_title(path), "lesson", lesson_week(lesson), lesson))
    return docs


def lesson_cards(docs: list[Document]) -> str:
    cards: list[str] = []
    for week in range(1, 9):
        week_docs = [doc for doc in docs if doc.week == week]
        cards.append(
            f'<section class="week-card" id="week-{week}">'
            f'<div><span class="eyebrow">Tuần {week}</span><h3>{WEEK_TITLES[week]}</h3></div>'
            '<div class="lesson-strip">'
        )
        for doc in week_docs:
            cards.append(
                f'<a href="#doc-{doc.lesson:02d}" class="mini-lesson">'
                f'<span>{doc.lesson:02d}</span>{escape(doc.title.replace(f"Bài {doc.lesson:02d}. ", ""))}</a>'
            )
        cards.append("</div></section>")
    return "\n".join(cards)


def navigation(docs: list[Document]) -> str:
    links = [
        '<a class="nav-link" href="#tong-quan" data-title="Tổng quan"><span>Tổng quan</span><small>Start</small></a>',
    ]
    for doc in docs:
        if doc.kind == "lesson":
            label = f"Bài {doc.lesson:02d}"
            href = f"#doc-{doc.lesson:02d}"
            data_kind = f"Tuần {doc.week}"
        else:
            label = "Tài liệu"
            href = f"#doc-{slugify(doc.title)}"
            data_kind = "Khung"
        links.append(
            f'<a class="nav-link" href="{href}" data-title="{escape(doc.title.lower())}">'
            f'<span>{escape(doc.title)}</span><small>{label}</small><em>{data_kind}</em></a>'
        )
    return "\n".join(links)


def render_articles(docs: list[Document]) -> str:
    articles: list[str] = []
    for doc in docs:
        article_id = f"doc-{doc.lesson:02d}" if doc.kind == "lesson" else f"doc-{slugify(doc.title)}"
        raw = doc.path.read_text(encoding="utf-8")
        body = markdown_to_html(raw, article_id)
        if doc.kind == "lesson":
            meta = f'<span class="lesson-number">Bài {doc.lesson:02d}</span><span>Tuần {doc.week}</span><span>{escape(WEEK_TITLES[doc.week])}</span>'
        else:
            meta = '<span>Tài liệu khung</span><span>Tra cứu nhanh</span>'
        articles.append(
            f'<article class="doc-section {doc.kind}" id="{article_id}" data-search="{escape((doc.title + " " + raw).lower())}">'
            f'<div class="article-meta">{meta}</div>{body}</article>'
        )
    return "\n".join(articles)


def build_html() -> str:
    docs = collect_documents()
    total_words = sum(len(doc.path.read_text(encoding="utf-8").split()) for doc in docs)
    lessons = [doc for doc in docs if doc.kind == "lesson"]
    css = r"""
:root {
  color-scheme: light;
  --bg: #f5f5f7;
  --panel: rgba(255, 255, 255, 0.82);
  --panel-solid: #ffffff;
  --ink: #1d1d1f;
  --muted: #6e6e73;
  --line: #d2d2d7;
  --blue: #0071e3;
  --blue-dark: #005bb5;
  --green: #2f7d5b;
  --gold: #b7791f;
  --soft-blue: #eaf4ff;
  --soft-green: #edf7f1;
  --soft-gold: #fff6e6;
  --radius: 8px;
  --shadow: 0 18px 50px rgba(0, 0, 0, 0.08);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", sans-serif;
  line-height: 1.65;
  letter-spacing: 0;
}
a { color: var(--blue); text-decoration: none; }
a:hover { color: var(--blue-dark); }
.shell { display: grid; grid-template-columns: 332px minmax(0, 1fr); min-height: 100vh; }
.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: auto;
  padding: 22px;
  border-right: 1px solid var(--line);
  background: rgba(245, 245, 247, 0.86);
  backdrop-filter: blur(24px);
}
.brand {
  display: grid;
  gap: 8px;
  padding: 14px 0 18px;
}
.brand-mark {
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  border-radius: var(--radius);
  background: var(--ink);
  color: #fff;
  font-weight: 800;
}
.brand h1 { margin: 0; font-size: 22px; line-height: 1.1; }
.brand p { margin: 0; color: var(--muted); font-size: 14px; }
.search-wrap { position: sticky; top: -22px; z-index: 2; padding: 12px 0; background: rgba(245, 245, 247, 0.92); backdrop-filter: blur(18px); }
#search {
  width: 100%;
  border: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.92);
  border-radius: var(--radius);
  padding: 12px 14px;
  font: inherit;
  outline: none;
}
#search:focus { border-color: var(--blue); box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.12); }
.nav-group { display: grid; gap: 6px; padding-bottom: 28px; }
.nav-link {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 4px 10px;
  align-items: center;
  padding: 10px 12px;
  border-radius: var(--radius);
  color: var(--ink);
  border: 1px solid transparent;
}
.nav-link span { font-size: 14px; font-weight: 700; line-height: 1.28; }
.nav-link small { color: var(--muted); font-size: 12px; white-space: nowrap; }
.nav-link em { grid-column: 1 / -1; color: var(--muted); font-size: 11px; font-style: normal; }
.nav-link:hover, .nav-link.active { background: var(--panel-solid); border-color: var(--line); color: var(--ink); }
.main { min-width: 0; }
.hero {
  min-height: 92vh;
  display: grid;
  align-items: end;
  padding: 64px;
  background: linear-gradient(135deg, #fbfbfd 0%, #eef5ff 50%, #edf7f1 100%);
  border-bottom: 1px solid var(--line);
}
.hero-inner { max-width: 1120px; }
.eyebrow {
  margin: 0 0 14px;
  color: var(--blue);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.hero h2 {
  max-width: 980px;
  margin: 0;
  font-size: 92px;
  line-height: 0.96;
  font-weight: 800;
}
.hero-lead {
  max-width: 760px;
  margin: 24px 0 0;
  color: #424245;
  font-size: 23px;
}
.hero-actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 30px; }
.button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 999px;
  background: var(--blue);
  color: #fff;
  font-weight: 800;
}
.button.secondary { background: #fff; color: var(--ink); border: 1px solid var(--line); }
.stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin-top: 42px;
}
.stat {
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow);
  backdrop-filter: blur(20px);
}
.stat b { display: block; font-size: 34px; line-height: 1; }
.stat span { display: block; margin-top: 8px; color: var(--muted); font-size: 14px; }
.content { max-width: 1180px; margin: 0 auto; padding: 44px 56px 80px; }
.section-title { font-size: 54px; line-height: 1; margin: 0 0 16px; }
.intro-grid, .quality-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin: 24px 0 34px;
}
.info-card, .week-card, .doc-section {
  background: var(--panel-solid);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}
.info-card { padding: 22px; }
.info-card h3 { margin: 0 0 8px; font-size: 20px; }
.info-card p { margin: 0; color: var(--muted); }
.week-card { display: grid; grid-template-columns: 260px 1fr; gap: 18px; padding: 22px; margin: 14px 0; }
.week-card h3 { margin: 4px 0 0; font-size: 24px; line-height: 1.1; }
.lesson-strip { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 10px; }
.mini-lesson {
  min-height: 92px;
  display: grid;
  align-content: start;
  gap: 8px;
  border-radius: var(--radius);
  border: 1px solid var(--line);
  background: #fbfbfd;
  padding: 12px;
  color: var(--ink);
  font-size: 13px;
  font-weight: 700;
}
.mini-lesson span {
  width: 34px;
  height: 28px;
  display: grid;
  place-items: center;
  border-radius: 999px;
  color: #fff;
  background: var(--ink);
  font-size: 12px;
}
.doc-section {
  margin: 26px 0;
  padding: 46px;
  scroll-margin-top: 24px;
}
.doc-section.lesson { border-top: 5px solid var(--blue); }
.doc-section.standard { border-top: 5px solid var(--green); }
.article-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 18px;
}
.article-meta span {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 6px 10px;
  background: var(--soft-blue);
  color: #0a4f93;
  font-size: 12px;
  font-weight: 800;
}
.doc-section.standard .article-meta span { background: var(--soft-green); color: #236144; }
.doc-section h2 {
  margin: 0 0 16px;
  font-size: 46px;
  line-height: 1.04;
}
.doc-section h3 {
  margin: 30px 0 8px;
  font-size: 22px;
  line-height: 1.18;
}
.doc-section h4 { margin: 22px 0 6px; font-size: 18px; }
.doc-section p { margin: 10px 0; }
.doc-section ul, .doc-section ol { padding-left: 22px; }
.doc-section li { margin: 7px 0; }
.doc-section h3:nth-of-type(7),
.doc-section h3:nth-of-type(8),
.doc-section h3:nth-of-type(9) {
  padding: 16px;
  border-radius: var(--radius);
}
.doc-section h3:nth-of-type(7) { background: var(--soft-green); }
.doc-section h3:nth-of-type(8) { background: var(--soft-blue); }
.doc-section h3:nth-of-type(9) { background: var(--soft-gold); }
.table-wrap {
  overflow: auto;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  margin: 18px 0;
}
table { width: 100%; border-collapse: collapse; min-width: 680px; background: #fff; }
th, td { padding: 12px 14px; border-bottom: 1px solid #e8e8ed; vertical-align: top; text-align: left; }
th { background: #f5f5f7; font-weight: 800; }
pre {
  overflow: auto;
  padding: 16px;
  border-radius: var(--radius);
  background: #1d1d1f;
  color: #f5f5f7;
}
code {
  font-family: "SFMono-Regular", Consolas, monospace;
  background: #f5f5f7;
  border: 1px solid #e8e8ed;
  border-radius: 6px;
  padding: 2px 6px;
}
pre code { background: transparent; border: 0; padding: 0; }
blockquote {
  margin: 18px 0;
  border-left: 4px solid var(--blue);
  background: var(--soft-blue);
  padding: 14px 18px;
  border-radius: var(--radius);
}
.tools {
  position: fixed;
  right: 18px;
  bottom: 18px;
  display: flex;
  gap: 8px;
  z-index: 10;
}
.tools button {
  border: 0;
  border-radius: 999px;
  background: var(--ink);
  color: #fff;
  padding: 12px 15px;
  font: inherit;
  font-weight: 800;
  cursor: pointer;
  box-shadow: var(--shadow);
}
.hidden-by-search { display: none; }
@media (max-width: 1120px) {
  .shell { grid-template-columns: 292px minmax(0, 1fr); }
  .hero { padding: 44px; }
  .hero h2 { font-size: 68px; }
  .hero-lead { font-size: 21px; }
  .content { padding: 34px; }
  .section-title { font-size: 46px; }
  .doc-section h2 { font-size: 38px; }
  .stats, .intro-grid, .quality-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .week-card { grid-template-columns: 1fr; }
  .lesson-strip { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
@media (max-width: 780px) {
  .shell { display: block; }
  .sidebar { position: relative; height: auto; }
  .hero { min-height: auto; padding: 42px 22px; }
  .hero h2 { font-size: 44px; }
  .hero-lead { font-size: 18px; }
  .content { padding: 24px 18px 70px; }
  .section-title { font-size: 34px; }
  .doc-section h2 { font-size: 30px; }
  .stats, .intro-grid, .quality-grid, .lesson-strip { grid-template-columns: 1fr; }
  .doc-section { padding: 22px; }
  .tools { left: 18px; right: auto; }
}
@media print {
  .sidebar, .tools, .hero-actions, .search-wrap { display: none !important; }
  .shell { display: block; }
  .hero { min-height: auto; padding: 24px; border-bottom: 1px solid #ddd; background: #fff; }
  .content { max-width: none; padding: 0 24px; }
  .doc-section, .info-card, .week-card { box-shadow: none; break-inside: avoid; }
}
"""
    script = r"""
const search = document.querySelector('#search');
const sections = Array.from(document.querySelectorAll('.doc-section'));
const navLinks = Array.from(document.querySelectorAll('.nav-link'));

search?.addEventListener('input', () => {
  const q = search.value.trim().toLowerCase();
  sections.forEach(section => {
    section.classList.toggle('hidden-by-search', q && !section.dataset.search.includes(q));
  });
  navLinks.forEach(link => {
    const title = link.dataset.title || '';
    link.classList.toggle('hidden-by-search', q && !title.includes(q));
  });
});

const observer = new IntersectionObserver(entries => {
  const visible = entries.filter(entry => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
  if (!visible) return;
  navLinks.forEach(link => link.classList.toggle('active', link.getAttribute('href') === '#' + visible.target.id));
}, { rootMargin: '-20% 0px -70% 0px', threshold: [0.05, 0.15, 0.3] });

document.querySelectorAll('section[id], article[id]').forEach(section => observer.observe(section));

document.querySelector('[data-print]')?.addEventListener('click', () => window.print());
document.querySelector('[data-top]')?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
"""
    return f"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Giáo Trình SketchUp + D5 Cho Dự Án Nhà Vườn</title>
  <meta name="description" content="Giáo trình 8 tuần học SketchUp và D5 bằng cách triển khai trực tiếp dự án nhà vườn.">
  <style>{css}</style>
</head>
<body>
  <div class="shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">D5</div>
        <h1>SketchUp + D5 Nhà Vườn</h1>
        <p>40 bài học thực hành, học đến đâu triển khai dự án đến đó.</p>
      </div>
      <div class="search-wrap">
        <input id="search" type="search" placeholder="Tìm bài, tiêu chuẩn, từ khóa...">
      </div>
      <nav class="nav-group" aria-label="Mục lục">{navigation(docs)}</nav>
    </aside>
    <main class="main">
      <section class="hero" id="tong-quan">
        <div class="hero-inner">
          <p class="eyebrow">Giáo trình hoàn chỉnh</p>
          <h2>Vừa học SketchUp + D5, vừa triển khai dự án nhà vườn.</h2>
          <p class="hero-lead">Một bản HTML tĩnh, trực quan, dễ tra soát: mục lục cố định, tìm kiếm nhanh, 8 tuần học rõ ràng, mỗi bài có mục tiêu, bản chất, thao tác, bài tập dự án và tiêu chuẩn đạt.</p>
          <div class="hero-actions">
            <a class="button" href="#week-1">Bắt đầu học</a>
            <a class="button secondary" href="#doc-checklist-dau-ra-cuoi-khoa">Xem đầu ra cuối khóa</a>
          </div>
          <div class="stats">
            <div class="stat"><b>{len(lessons)}</b><span>Bài học Markdown</span></div>
            <div class="stat"><b>8</b><span>Tuần triển khai</span></div>
            <div class="stat"><b>{total_words:,}</b><span>Từ nội dung gốc</span></div>
            <div class="stat"><b>1</b><span>Hồ sơ concept cuối</span></div>
          </div>
        </div>
      </section>
      <div class="content">
        <section aria-labelledby="overview-title">
          <p class="eyebrow">Tổng quan</p>
          <h2 class="section-title" id="overview-title">Thiết kế để học sâu, làm thật, kiểm được.</h2>
          <div class="intro-grid">
            <div class="info-card"><h3>Học bằng dự án thật</h3><p>Mỗi bài đều yêu cầu áp dụng trực tiếp vào model nhà vườn, không tách rời lý thuyết và thực hành.</p></div>
            <div class="info-card"><h3>Tiêu chuẩn rõ</h3><p>Mỗi bài có tiêu chí đạt để tự kiểm: đo được, nhìn được, so sánh được hoặc ghi chú được.</p></div>
            <div class="info-card"><h3>Tra cứu nhanh</h3><p>Sidebar cố định và ô tìm kiếm giúp quay lại bài, thuật ngữ, checklist hoặc đầu ra rất nhanh.</p></div>
          </div>
        </section>
        <section aria-labelledby="roadmap-title">
          <p class="eyebrow">Lộ trình 8 tuần</p>
          <h2 class="section-title" id="roadmap-title">Từ file trắng đến ảnh render và video walkthrough.</h2>
          {lesson_cards(docs)}
        </section>
        {render_articles(docs)}
      </div>
    </main>
  </div>
  <div class="tools">
    <button type="button" data-top>Đầu trang</button>
    <button type="button" data-print>In/PDF</button>
  </div>
  <script>{script}</script>
</body>
</html>
"""


def main() -> None:
    OUTPUT.write_text(build_html(), encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
