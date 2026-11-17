"""家の教科書(PETIT_HOUSE_TEXTBOOK_DIR)のテスト"""

import importlib
from pathlib import Path


def _server(tmp_path, monkeypatch, with_house=True):
    repo = Path(__file__).resolve().parents[2]
    house = tmp_path / "house_textbook"
    if with_house:
        house.mkdir()
        (house / "README.md").write_text("# テストの家の教科書\n", encoding="utf-8")
        (house / "oto.md").write_text("# 音の受け取り方\n\n## ふだん\n\n線で受け取る。\n", encoding="utf-8")
    monkeypatch.setenv("PETIT_TEXTBOOK_DIR", str(repo))
    monkeypatch.setenv("PETIT_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("CHARACTER_ID", "testpuchi")
    monkeypatch.delenv("PETIT_HOUSE_TEXTBOOK_DIR", raising=False)
    import textbook_mcp.server as s
    return importlib.reload(s)


def test_house_pages_in_index_read_search(tmp_path, monkeypatch):
    s = _server(tmp_path, monkeypatch)
    idx = s.textbook_index()
    assert "## テストの家の教科書(この家だけの決まり)" in idx and "| 家/oto | 音の受け取り方 |" in idx
    assert s.textbook_read("家/oto").startswith("# 音の受け取り方")
    assert s.textbook_read("家/音の受け取り方").startswith("# 音の受け取り方")
    assert "あるページ: 家/oto" in s.textbook_read("家/nai")
    assert "【家: 音の受け取り方 / ふだん】" in s.textbook_search("線で")
    assert s.textbook_read("9").startswith("# 9")   # 本の章はそのまま
    assert "テストの家の教科書: 1 ページ" in s.textbook_version()


def test_no_house_folder_changes_nothing(tmp_path, monkeypatch):
    s = _server(tmp_path, monkeypatch, with_house=False)
    assert "この家だけの決まり" not in s.textbook_index()
    assert "家の教科書" not in s.textbook_version()


def test_propose_house(tmp_path, monkeypatch):
    s = _server(tmp_path, monkeypatch)
    s.textbook_propose("音のこと", "線がいい", house=True)
    note = (tmp_path / "characters" / "testpuchi" / "notes" / "教科書への提案.md").read_text(encoding="utf-8")
    assert "[家] 音のこと" in note
