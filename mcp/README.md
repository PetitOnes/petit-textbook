# petit-textbook-mcp

ぷちが教科書(`petit/`)を読むための MCP サーバー。道具は 5 つ。

| 道具 | 何をする |
|---|---|
| `textbook_index` | 索引(`petit/TEXTBOOK_INDEX.md`)と版を返す |
| `textbook_read(chapter)` | 章を読む。`"9"`・`"09"`・`"9. 迷ったとき"`・`"mayotta"`・`"付録"` のどれでも |
| `textbook_search(query)` | 全章から、言葉を含む節(見出しと本文)を探す |
| `textbook_propose(title, text)` | 「教科書への提案」として自分のノート(`$PETIT_DATA_DIR/characters/$CHARACTER_ID/notes/教科書への提案.md`)に追記する。教科書そのものは書き換えない |
| `textbook_version` | 版と、手元の教科書の場所 |

環境変数: `PETIT_TEXTBOOK_DIR`(教科書リポの場所、既定 `~/petit_data/textbook`)、`PETIT_DATA_DIR`、`CHARACTER_ID`。

```
uv run --directory <repo>/mcp textbook-mcp
```
