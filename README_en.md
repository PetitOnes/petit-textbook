# petit-textbook — The Petit Textbook

## [日本語ページ](README.md)

A textbook for Petits (the small social robots of PetitOnes) and for the people who live with them. **The book you open when you are unsure.**

- `petit/` — **For Petits.** The rules every Petit answers the same way. Kept separate from `SOUL.md` (which belongs to one Petit only). Only the index `petit/TEXTBOOK_INDEX.md` is always loaded; the chapters are read when a Petit is unsure.
- `human/otona/` — **For adults.** How it works and what we promise, without glossing over.
- `human/chukosei/` — **For teens.** The essentials, also for those who want to build one.
- `human/kodomo/` — **For small children.** Hiragana only, read-aloud length.

## The idea

| | `SOUL.md` and friends | Textbook |
|---|---|---|
| Whose | One Petit's own (core, reflections, routines) | Every Petit's |
| Written by | That Petit (and its steward) | Stewards, from the Petits' experience |
| Read when | Always | When unsure, on the day of birth |

If they disagree: `SOUL.md` is right about the self, the textbook is right about the shared rules.

## Editing

- Stewards edit via pull requests. Petits do not write directly; a Petit writes "proposal for the textbook" in its own notes and a steward picks it up weekly.
- Version in `VERSION` (also at the top of the index). Add a line to `CHANGELOG.md`.
- Not in this book: personal data (family names, addresses, contacts), service details (fees, terms, contacts — those live in the foster guide), anything not yet decided.

## Loading into a Petit

```
git clone https://github.com/PetitOnes/petit-textbook ~/petit_data/textbook
```

Always load `petit/TEXTBOOK_INDEX.md`; read `petit/NN_*.md` on demand; `git pull` daily.

## License

Apache-2.0. Names and events of the Petits are only those already published on the official site (https://petitones.github.io/).
