"""Lint the macros embedded in the generated pages.

Usage:
  python3 -I tools/validate.py *.html                       lint every page
  python3 -I tools/validate.py --check-cache FILE PAGE.html  check a downloaded macros-cache.txt
Exits non-zero if anything fails.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import RACIAL_SPELLS  # noqa: E402
from pages import PAGES  # noqa: E402

LIMIT = 255
NAME_LIMIT = 16

COMMANDS = {"/cast", "/spell", "/use", "/castsequence", "/stopcasting", "/stopmacro", "/focus", "/clearfocus",
            "/target", "/tar", "/assist", "/a", "/petattack", "/petfollow", "/petpassive", "/petdefensive",
            "/petstay", "/cancelaura", "/cancelform", "/startattack", "/stopattack", "/run", "/script",
            "/targetenemyplayer", "/targetfriendplayer", "/targetmarker", "/dismount", "/follow", "/equipset",
            "/readycheck", "/roll", "/reload", "/console", "/equip"}
NO_NAME_CHECK = {"/focus", "/clearfocus", "/target", "/tar", "/assist", "/a", "/petattack", "/petfollow",
                 "/petpassive", "/petdefensive", "/petstay", "/stopmacro", "/stopcasting", "/startattack",
                 "/stopattack", "/targetenemyplayer", "/targetfriendplayer", "/targetmarker", "/dismount",
                 "/follow", "/equipset", "/readycheck", "/roll", "/reload", "/console", "/cancelform"}
META = {"#showtooltip", "#show"}
CONDITIONS = re.compile(r"^(no)?(help|harm|dead|exists|combat|channeling|stealth|mounted|pet|mod|"
                        r"mod:(shift|ctrl|alt)|pet:[A-Za-z/ ]+|stance:[0-3]|equipped:[A-Za-z ]+)$")
UNITS = {"@focus", "@mouseover", "@player", "@target", "@pet", "@targettarget"}  # no @cursor on purpose

# Race x class in Forever (research, October 2026)
RACES = {"Warrior": {"Orc", "Undead", "Tauren", "Troll"}, "Rogue": {"Orc", "Undead", "Troll"},
         "Hunter": {"Orc", "Tauren", "Troll"}, "Shaman": {"Orc", "Tauren", "Troll"}, "Priest": {"Undead", "Troll"},
         "Mage": {"Orc", "Undead", "Troll"}, "Warlock": {"Orc", "Undead", "Troll"}, "Druid": {"Tauren"},
         "Paladin": {"Undead"}, "All characters": set()}
REMOVED = {"Curse of Agony", "Curse of Doom", "Curse of Shadows", "Dark Pact", "Command", "Elemental Mastery",
           "Wyvern Sting", "Crusader Strike", "Divine Storm", "Avenger's Shield", "Tranquil Air Totem",
           "Cloak of Shadows", "Shadow Dance"}
OFF_GCD = {"Blood Fury", "Berserking", "Amplify Curse", "Fel Domination", "Inner Focus", "Will of the Forsaken",
           "Nature's Swiftness", "Presence of Mind", "Arcane Power", "Combustion", "Heroic Strike", "Cleave",
           "Charge", "Intercept", "Auto Shot", "Feign Death", "Disengage", "Judgement", "Divine Favor"}
PET_SPELLS = {"Seduction", "Spell Lock", "Sacrifice", "Phase Shift", "Devour Magic", "Fire Shield",
              "Suffering", "Soothing Kiss", "Torment"}
ITEMS = {"Healthstone", "Soulstone", "Mana Ruby", "Thistle Tea", "Hearthstone", "Deadly Poison V",
         "Instant Poison VI", "Mind-numbing Poison III", "Crippling Poison II", "Horn of the Swift Brown Wolf",
         "Conjured Crystal Water", "Roasted Quail", "Strong Fishing Pole", "Aquadynamic Fish Attractor"}
STABLE_ITEMS = {"Thistle Tea"}


def split_clauses(args):
    for clause in args.split(";"):
        clause = clause.strip()
        conds = re.findall(r"\[([^\]]*)\]", clause)
        rest = re.sub(r"\[[^\]]*\]", "", clause).strip()
        yield conds, rest


def check_conditions(conds, errs):
    for group in conds:
        for tok in filter(None, (t.strip() for t in group.split(","))):
            if tok.startswith("@"):
                if tok not in UNITS:
                    errs.append(f"unknown unit {tok}")
            elif not CONDITIONS.match(tok):
                errs.append(f"unknown conditional {tok}")


def lint(macro, page):
    errs, names = [], set()
    text = macro["text"]
    if len(text) > LIMIT:
        errs.append(f"{len(text)} chars > {LIMIT}")
    if text.count("[") != text.count("]"):
        errs.append("unbalanced brackets")
    gcd_lines = 0
    for line in text.splitlines():
        cmd, _, args = line.partition(" ")
        if cmd in META:
            continue
        if cmd not in COMMANDS:
            errs.append(f"unknown command {cmd}")
            continue
        if cmd in ("/run", "/script"):
            continue
        clauses = list(split_clauses(args))
        for conds, _ in clauses:
            check_conditions(conds, errs)
        if cmd in NO_NAME_CHECK:
            continue
        if cmd == "/equip":
            names |= {rest for _, rest in clauses if rest}
            continue
        if cmd in ("/cast", "/spell", "/use"):
            spells = {rest.lstrip("!") for _, rest in clauses if rest and not rest.startswith("item:")}
            names |= spells
            if {s for s in spells if not s.isdigit()} - OFF_GCD - PET_SPELLS - ITEMS:
                gcd_lines += 1
        elif cmd == "/castsequence":
            seq = re.sub(r"^reset=\S+\s*", "", clauses[0][1])
            names |= {s.strip() for s in seq.split(",")}
            gcd_lines += 1
        elif cmd == "/cancelaura":
            names |= {rest for _, rest in clauses if rest}
    if gcd_lines > 1:
        errs.append(f"{gcd_lines} lines cast global-cooldown spells; only the first can fire per press")

    known = page["spells"] | set(RACIAL_SPELLS) | ITEMS
    unsure = page["unsure"] | (ITEMS - STABLE_ITEMS)
    for n in names:
        if n in REMOVED:
            errs.append(f"'{n}' was removed or renamed in Forever")
        elif n not in known and n not in unsure and not n.isdigit():
            errs.append(f"unknown spell/item '{n}'")
        if n in unsure and macro["status"] != "verify":
            errs.append(f"'{n}' is unconfirmed; mark the macro verify")
        if n in RACIAL_SPELLS and macro.get("race") != RACIAL_SPELLS[n]:
            errs.append(f"'{n}' is a {RACIAL_SPELLS[n]} racial but the macro is tagged {macro.get('race')}")
    race = macro.get("race")
    if race and race not in RACES[page["title"]]:
        errs.append(f"{race} can't be a {page['title']} in Forever")
    if macro["status"] == "verify" and not macro.get("note"):
        errs.append("verify macro needs a note explaining what to check")
    name = macro.get("name", "")
    if not name or len(name) > NAME_LIMIT or '"' in name:
        errs.append(f"in-game name '{name}' must be 1-{NAME_LIMIT} characters without quotes")
    return errs


def load(path):
    src = open(path, encoding="utf-8").read()
    m = re.search(r'<script type="application/json" id="macro-data">(.*?)</script>', src, re.S)
    data = json.loads(m.group(1))
    page = next(p for p in PAGES.values() if p["file"] == pathlib.Path(path).name)
    return data, page


def main(paths):
    failed = total = 0
    for path in paths:
        if pathlib.Path(path).name == "index.html":
            continue
        data, page = load(path)
        for label, items in (("ids", [x["id"] for x in data["macros"]]), ("in-game names", [x["name"] for x in data["macros"]])):
            dup = {i for i in items if items.count(i) > 1}
            if dup:
                print(f"FAIL {path}: duplicate {label}: {', '.join(sorted(dup))}")
                failed += 1
        for x in data["macros"]:
            total += 1
            errs = [f"section '{x['section']}' not listed"] if x["section"] not in data["sections"] else []
            errs += lint(x, page)
            if errs:
                failed += 1
                print(f"FAIL {path}: {x['id']}: " + "; ".join(errs))
        verify = sum(x["status"] == "verify" for x in data["macros"])
        print(f"{path}: {len(data['macros'])} macros, {verify} flagged check-in-game")
    print(f"{total - failed}/{total} passed" if failed else f"all {total} macros passed")
    return 1 if failed else 0


def check_cache(cache_path, page_path):
    """Parse a downloaded macros-cache.txt and confirm it round-trips against the page."""
    data, _ = load(page_path)
    by_name = {x["name"]: x["text"] for x in data["macros"]}
    raw = open(cache_path, "rb").read().decode("utf-8")
    errs = []
    if "\n" in raw.replace("\r\n", ""):
        errs.append("bare LF line endings (expected CRLF)")
    lines = raw.split("\r\n")
    ids, i = [], 0
    while i < len(lines) and lines[i]:
        hdr = re.fullmatch(r'VER 3 ([0-9A-F]{16}) "([^"]*)" "([^"]*)"', lines[i])
        if not hdr:
            errs.append(f"line {i + 1}: bad header {lines[i]!r}")
            break
        j = lines.index("END", i + 1)
        ids.append(int(hdr.group(1), 16))
        if hdr.group(2) in by_name and by_name[hdr.group(2)] != "\n".join(lines[i + 1:j]):
            errs.append(f"{hdr.group(2)}: body differs from the page")
        i = j + 1
    if len(ids) != len(set(ids)):
        errs.append("duplicate ids")
    scopes = {"character" if x >= 0x1000000 else "account" for x in ids}
    if len(scopes) > 1:
        errs.append("mixes account and character ids")
    print(f"{cache_path}: {len(ids)} macros, ids {min(ids):#x}..{max(ids):#x}, scope {', '.join(scopes)}")
    for e in errs:
        print("FAIL", e)
    return 1 if errs else 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["--check-cache"]:
        sys.exit(check_cache(sys.argv[2], sys.argv[3]))
    sys.exit(main(sys.argv[1:]))
