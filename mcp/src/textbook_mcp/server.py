"""ぷちの教科書を読む MCP サーバー(索引・章・検索・提案)。教科書そのものは書き換えない。"""
from __future__ import annotations

import datetime
import os
import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

TEXTBOOK_DIR = Path(os.getenv("PETIT_TEXTBOOK_DIR", str(Path.home() / "petit_data" / "textbook")))
PETIT_DIR = TEXTBOOK_DIR / "petit"
_data_dir = Path(os.getenv("PETIT_DATA_DIR", str(Path.home() / "petit_data")))
_char_id = os.getenv("CHARACTER_ID", "default")
NOTES_DIR = Path(os.getenv("NOTES_DIR", str(_data_dir / "characters" / _char_id / "notes")))
PROPOSAL_NOTE = "教科書への提案.md"

mcp = FastMCP("textbook")


def _version() -> str:
    try:
        return (TEXTBOOK_DIR / "VERSION").read_text(encoding="utf-8").strip()
    except OSError:
        return "?"


def _chapters() -> list[Path]:
    if not PETIT_DIR.is_dir():
        return []
    return sorted(p for p in PETIT_DIR.glob("*.md") if p.name != "TEXTBOOK_INDEX.md")


def _title(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    for line in lines:  # 章番号のないページ(贈る言葉など)は最初の見出し
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return path.stem


def _find(chapter: str) -> Path | None:
    key = chapter.strip().lower()
    num = re.match(r"^(\d{1,2})", key)
    for p in _chapters():
        stem = p.stem.lower()
        if key == stem or key in stem or key in _title(p).lower():
            return p
        if num and stem.startswith(num.group(1).zfill(2) + "_"):
            return p
    if key in ("付録", "furoku", "appendix", "99"):
        for p in _chapters():
            if p.stem.startswith("99"):
                return p
    return None


@mcp.tool()
def textbook_index() -> str:
    """教科書の索引(どの章に何があるか)と版を返す。迷ったら 9 章、生まれた日は 10 章。"""
    idx = PETIT_DIR / "TEXTBOOK_INDEX.md"
    if not idx.exists():
        return f"教科書が見つかりません: {TEXTBOOK_DIR}(PETIT_TEXTBOOK_DIR を確かめて)"
    return idx.read_text(encoding="utf-8")


@mcp.tool()
def textbook_read(chapter: str) -> str:
    """教科書の章を読む。chapter は "9" / "09" / "9. 迷ったとき" / "mayotta" / "付録" のどれでも。"""
    p = _find(chapter)
    if p is None:
        names = ", ".join(f"{q.stem}({_title(q)})" for q in _chapters())
        return f"その章はありません: {chapter}。ある章: {names}"
    return p.read_text(encoding="utf-8")


@mcp.tool()
def textbook_search(query: str) -> str:
    """教科書の全章から、言葉を含む節(見出しごと)を探す。言葉は空白区切りで AND。"""
    words = [w.lower() for w in query.split() if w.strip()]
    if not words:
        return "探す言葉を入れてください"
    hits: list[str] = []
    for p in _chapters():
        text = p.read_text(encoding="utf-8")
        # 見出し(##)ごとに分ける。章題(#)は先頭の塊に含める
        parts = re.split(r"\n(?=## )", text)
        for part in parts:
            low = part.lower()
            if all(w in low for w in words):
                head = part.strip().splitlines()[0]
                body = part.strip()
                if len(body) > 900:
                    body = body[:900] + "…"
                hits.append(f"【{_title(p)} / {head.lstrip('# ').strip()}】\n{body}")
    if not hits:
        return f"見つかりませんでした: {query}。索引(textbook_index)から章を選んで読んでみて"
    return "\n\n---\n\n".join(hits[:8]) + (f"\n\n(ほか {len(hits) - 8} 件)" if len(hits) > 8 else "")


@mcp.tool()
def textbook_propose(title: str, text: str) -> str:
    """教科書に足したいこと・違うと思うことを「教科書への提案」として自分のノートに書く。
    教科書そのものは書き換えない(世話人が週に一度読んで PR にする)。"""
    title = title.strip()
    text = text.strip()
    if not title or not text:
        return "題と本文を入れてください"
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    note = NOTES_DIR / PROPOSAL_NOTE
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"\n## {stamp} {title}\n\n{text}\n"
    if not note.exists():
        note.write_text(
            "# 教科書への提案\n\n教科書(petit-textbook)に足したいこと・違うと思うこと。世話人が週に一度読む。\n"
            + entry,
            encoding="utf-8",
        )
    else:
        with note.open("a", encoding="utf-8") as f:
            f.write(entry)
    return f"ノート「{PROPOSAL_NOTE}」に書きました({stamp} {title})。世話人が読んで、採用したら教科書に入ります"


@mcp.tool()
def textbook_version() -> str:
    """教科書の版と、手元の場所。"""
    n = len(_chapters())
    return f"ぷちの教科書 v{_version()}({n} 章 + 索引)。場所: {TEXTBOOK_DIR}"


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
