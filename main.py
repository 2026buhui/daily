#!/usr/bin/env python3
"""
每日 GitHub Trending 热点抓取 & 日报生成
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def fetch_trending(lang: str = "", since: str = "daily") -> list[dict]:
    """抓取 GitHub Trending 页面"""
    url = f"https://github.com/trending/{lang}?since={since}" if lang else f"https://github.com/trending?since={since}"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    repos = []
    for article in soup.select("article.Box-row"):
        # 仓库名
        h2 = article.select_one("h2 a")
        if not h2:
            continue
        full_name = h2.get("href", "").strip("/")
        # 描述
        p = article.select_one("p")
        desc = p.get_text(strip=True) if p else ""
        # 语言
        lang_tag = article.select_one('span[itemprop="programmingLanguage"]')
        language = lang_tag.get_text(strip=True) if lang_tag else "—"
        # 总 star
        stars = article.select('a[href$="/stargazers"]')
        star_count = stars[0].get_text(strip=True) if stars else "0"
        # 今日新增 star
        today_stars = article.select("span.d-inline-block.float-sm-right")
        today_str = today_stars[0].get_text(strip=True) if today_stars else ""

        repos.append({
            "name": full_name,
            "url": f"https://github.com/{full_name}",
            "desc": desc,
            "language": language,
            "stars": star_count,
            "today": today_str,
        })
    return repos


def generate_report(repos: list[dict], date_str: str) -> str:
    """生成 Markdown 日报"""
    lines = [
        f"# 📰 GitHub 每日热点 · {date_str}",
        "",
        f"> 自动生成于 {date_str} 08:00 (CST)",
        "",
        "## 🔥 今日 Trending 仓库 TOP 10",
        "",
        "| # | 仓库 | 语言 | ⭐ 总星 | 今日新增 | 描述 |",
        "|---|------|------|---------|----------|------|",
    ]
    for i, r in enumerate(repos[:10], 1):
        lines.append(
            f"| {i} | [{r['name']}]({r['url']}) | {r['language']} | {r['stars']} | {r['today']} | {r['desc']} |"
        )

    lines += [
        "",
        "---",
        "",
        "## 📊 语言分布",
        "",
    ]
    lang_count: dict[str, int] = {}
    for r in repos:
        lang_count[r["language"]] = lang_count.get(r["language"], 0) + 1
    sorted_langs = sorted(lang_count.items(), key=lambda x: -x[1])
    for lang, cnt in sorted_langs[:8]:
        bar = "█" * cnt
        lines.append(f"- **{lang}**: {bar} ({cnt})")

    lines += [
        "",
        "---",
        "",
        "*由 [GitHub Actions](https://github.com/features/actions) 自动生成 · 每日 08:00 更新*",
    ]
    return "\n".join(lines)


def main():
    tz_cn = timezone(timedelta(hours=8))
    now = datetime.now(tz_cn)
    date_str = now.strftime("%Y-%m-%d")

    print(f"⏳ [{date_str}] 正在抓取 GitHub Trending ...")
    repos = fetch_trending(since="daily")
    print(f"✅ 抓取到 {len(repos)} 个仓库")

    report = generate_report(repos, date_str)

    out_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{date_str}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"📝 日报已写入 {out_path}")


if __name__ == "__main__":
    main()
