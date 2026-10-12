# WoW: Forever macros

Copy-ready PvP and PvE macros for an Undead Priest, Orc Warlock, Tauren Druid and Orc Mage in World of Warcraft: Forever. Open `index.html`.

Conventions on every page: click = target/mouseover, Shift = focus, Alt = self, Ctrl = alternate spell.

## Editing

Macro data lives in `tools/` (`macros.py`, `druid.py`, `mage.py`; page order in `pages.py`). The HTML pages are generated, so don't edit them by hand.

```sh
python3 -I tools/build.py
python3 -I tools/validate.py priest.html warlock.html druid.html mage.html
```

The validator checks the 255-character limit, commands, conditionals, spell names against the Forever beta spellbook, and one global-cooldown spell per press.
