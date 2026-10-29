#!/usr/bin/env python3
"""Fail closed if bilingual academic-homepage content or output diverges."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

def section(document: str, start: str, end: str) -> list[str]:
    lines = document.splitlines()
    a = next(i for i, x in enumerate(lines) if x.startswith(start))
    b = next(i for i, x in enumerate(lines) if i > a and x.startswith(end))
    return lines[a + 1:b]

def bullets(lines: list[str]) -> list[str]:
    return [line for line in lines if line.startswith("- ")]

def publication_url(line: str) -> str:
    match = re.search(r"\]\((https?://[^)]+)\)", line)
    if not match:
        # Some already-listed papers have no hyperlink. Compare their full
        # bibliographic text across languages instead of rejecting them.
        return "unlinked:" + re.sub(r"\\s+", " ", line).strip()
    return match.group(1)

def patent_id(line: str) -> str:
    match = re.search(r"(?:ZL|CN)\s*(20\d{10}\.\d)\b", line)
    if not match:
        raise AssertionError(f"Patent number is missing: {line[:95]}")
    return match.group(1)

def check_source() -> None:
    zh = read("_pages/about.md")
    en = read("_pages/about_en.md")
    zh_layout = read("_layouts/page_zh.html")
    en_layout = read("_layouts/page_en.html")
    profile = read("_includes/author-profile.html")
    config = read("_config.yml")

    assert "<title>孙泽敏</title>" in zh_layout, "Chinese page title must remain unchanged"
    assert "Zemin Sun" in config and "name_en" in profile
    assert "2027 年博士研究生招生名额已满" in zh
    assert "暂不接受海外 CSC 申请" in zh
    assert "All Ph.D. positions for 2027 have been filled" in en
    assert "not accepting overseas CSC applications" in en

    for layout in (zh_layout, en_layout):
        for tag in ('rel="canonical"', 'hreflang="zh-CN"', 'hreflang="en"',
                    'type="application/ld+json"', 'name="description"'):
            assert tag in layout, f"Missing SEO metadata: {tag}"

    zh_pubs = bullets(section(zh, "# 发表文章", "# 教改项目"))
    en_pubs = bullets(section(en, "# Publications", "# Teaching Reform Projects"))
    assert len(zh_pubs) == len(en_pubs) == 29, (
        f"Publication counts: Chinese={len(zh_pubs)}, English={len(en_pubs)}"
    )
    assert list(map(publication_url, zh_pubs)) == list(map(publication_url, en_pubs)), (
        "English publication order and links must match Chinese"
    )

    zh_patents = bullets(section(zh, "# 发明专利", "# 学术兼职"))
    en_patents = bullets(section(en, "# Patents", "# Academic Services"))
    assert len(zh_patents) == len(en_patents) == 10, (
        f"Patent counts: Chinese={len(zh_patents)}, English={len(en_patents)}"
    )
    assert list(map(patent_id, zh_patents)) == list(map(patent_id, en_patents)), (
        "English patent order or identifiers differ from Chinese"
    )

    zh_projects = bullets(section(zh, "# 科研项目", "# 发明专利"))
    en_projects = [x for x in section(en, "# Research Projects", "# Patents")
                   if re.match(r"^\d+\.\s", x)]
    assert len(zh_projects) == len(en_projects) == 12, "Research project count mismatch"

    zh_awards = bullets(section(zh, "# 获奖情况", "\0")) if "\0" in zh else bullets(
        zh.split("# 获奖情况")[1].splitlines()
    )
    en_awards = bullets(en.split("# Awards and Honors")[1].splitlines())
    assert len(zh_awards) == len(en_awards) == 8, "Award count mismatch"
    assert "Application (8/12)" in en, "Award ranking attribution is missing"
    assert "Award (2024, Changchun Branch) (8/12)" not in en, "Award ranking incorrectly attributed"

    # Check that all Markdown heading anchors are unique on each page.
    for name, doc in (("Chinese", zh), ("English", en)):
        anchors = re.findall(r"^#+ .*\{#([^}]+)\}", doc, re.MULTILINE)
        assert len(anchors) == len(set(anchors)), f"Duplicate {name} anchors"
    print("PASS: Chinese title, notices, metadata, 29 publications, 12 projects, 10 patents, 8 awards")

def check_built(site: Path) -> None:
    pages = [(site / "index.html", "孙泽敏"), (site / "en/about/index.html", "Zemin Sun")]
    for page, title in pages:
        assert page.is_file(), f"Built page is missing: {page}"
        html = page.read_text(encoding="utf-8")
        assert f"<title>{title}</title>" in html or (
            title == "Zemin Sun" and "<title>Zemin Sun |" in html
        ), f"Wrong built title: {page}"
        assert 'application/ld+json' in html, f"Structured data missing from {page}"
    print("PASS: Built Chinese and English pages and SEO metadata")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--built", type=Path, help="Check Jekyll output under this directory")
    args = parser.parse_args()
    check_source()
    if args.built:
        check_built(args.built)

if __name__ == "__main__":
    main()
