# WoW: Forever macros

Copy-ready PvP and PvE macros for every Horde class in World of Warcraft: Forever, plus a page of macros for every character. Open `index.html`.

Conventions on every page: click = target/mouseover, Shift = focus, Alt = self, Ctrl = alternate spell. Class pages filter by race (`warrior.html#race=troll`), and racial macros sit in their own section.

## Installing macros as a file

Each page can download the macros that are showing and ticked as a `macros-cache.txt`:

1. In game, type `/console synchronizeMacros 0`, so Blizzard's server copy doesn't overwrite the file. Exit WoW completely.
2. Open your Forever folder (beta: `_classic_beta_`), then `WTF/Account/<account>/`.
   - All characters (General tab): put the file here.
   - This character only: go into `<Realm>/<Character>/` and put it there.
3. Rename the old `macros-cache.txt` to `macros-cache.bak`, then copy the new file in. To keep your existing macros, choose your old file in the page's "Keep your existing macros" box before downloading; the page appends to it.
4. Start WoW, check with `/macro`, then `/console synchronizeMacros 1` if you want sync back.

File format: `VER 3 <16 hex id> "<name>" "<icon>"`, the macro lines, then `END`, with CRLF line endings. Account macros use ids from 1, character macros from `0000000001000001`.

## Editing

Macro data lives in `tools/`: one file per page (`general.py`, `warrior.py`, …), shared helpers and racial macros in `common.py`, page order in `pages.py`. The HTML pages are generated, so don't edit them by hand.

```sh
python3 -I tools/build.py
python3 -I tools/validate.py *.html
python3 -I tools/validate.py --check-cache path/to/macros-cache.txt warrior.html
```

The validator checks:
- the 255-character limit, and in-game names of 16 characters or fewer;
- commands and conditionals;
- spell names against each class's Forever spellbook, including spells removed or renamed in Forever;
- one global-cooldown spell per press;
- racials tagged with the right race, and races that can actually play the class in Forever.
