"""Lint the macros embedded in the generated pages.

Usage: python3 -I tools/validate.py priest.html warlock.html
Exits non-zero if any macro fails.
"""
import json
import re
import sys

LIMIT = 255

COMMANDS = {"/cast", "/spell", "/tar", "/a", "/script", "/use", "/castsequence", "/stopcasting", "/stopmacro", "/focus", "/clearfocus",
            "/target", "/assist", "/petattack", "/petfollow", "/petpassive", "/petdefensive",
            "/petstay", "/cancelaura", "/run", "/cancelform", "/startattack"}
META = {"#showtooltip", "#show"}
CONDITIONS = re.compile(r"^(no)?(help|harm|dead|exists|combat|channeling|stealth|mod(:(shift|ctrl|alt))?|pet(:[A-Za-z/ ]+)?)$")
UNITS = {"@focus", "@mouseover", "@player", "@target", "@pet", "@targettarget"}

# Spell/item names confirmed from the Forever beta spellbook research.
PRIEST = {
    "Flash Heal", "Greater Heal", "Heal", "Renew", "Power Word: Shield", "Power Word: Fortitude",
    "Divine Spirit", "Shadow Protection", "Dispel Magic", "Abolish Disease", "Fear Ward", "Silence",
    "Psychic Scream", "Mind Control", "Mana Burn", "Shackle Undead", "Holy Nova", "Will of the Forsaken",
    "Shadowform", "Fade", "Inner Fire", "Touch of Weakness", "Dark Sacrifice", "Cannibalize",
    "Shadow Word: Pain", "Devouring Plague", "Mind Blast", "Inner Focus", "Shadow Word: Death",
    "Mind Flay", "Smite", "Shadowform", "Holy Fire", "Power Infusion", "Penance", "Prayer of Mending", "Binding Heal",
    "Vampiric Embrace",
}
WARLOCK = {
    "Seduction", "Spell Lock", "Sacrifice", "Phase Shift", "Devour Magic", "Fire Shield", "Suffering",
    "Soothing Kiss", "Torment", "Curse of Tongues", "Curse of Exhaustion", "Amplify Curse",
    "Curse of Weakness", "Curse of Recklessness", "Curse of the Elements", "Bane of Agony", "Bane of Doom",
    "Bane of Havoc", "Fear", "Death Coil", "Howl of Terror", "Banish", "Drain Mana", "Blood Fury",
    "Shadow Bolt", "Incinerate", "Immolate", "Conflagrate", "Shadowburn", "Searing Pain", "Soul Fire",
    "Corruption", "Siphon Life", "Demonic Sacrifice", "Fel Domination", "Summon Imp", "Summon Voidwalker",
    "Summon Succubus", "Summon Incubus", "Summon Felhunter", "Shadow Ward", "Life Tap",
}
DRUID = {
    "Healing Touch", "Regrowth", "Rejuvenation", "Swiftmend", "Innervate", "Rebirth", "Thorns",
    "Gift of the Wild", "Mark of the Wild", "Remove Curse", "Abolish Poison", "Cat Form", "Travel Form",
    "Moonkin Form", "Prowl", "Dash", "Ravage", "Pounce", "Shred", "Rip", "Ferocious Bite", "Rake", "Claw",
    "Feral Charge", "Bash", "Faerie Fire", "Swipe", "Maul", "Growl", "Barkskin", "Frenzied Regeneration",
    "Entangling Roots", "Hibernate", "Nature's Grasp", "Moonfire", "Insect Swarm", "Starfire", "Wrath",
    "Hurricane", "War Stomp",
}
MAGE = {
    "Polymorph", "Counterspell", "Frost Nova", "Cone of Cold", "Blink", "Ice Block", "Ice Barrier",
    "Mana Shield", "Frost Ward", "Fire Ward", "Remove Lesser Curse", "Frostbolt", "Fireball", "Fire Blast",
    "Scorch", "Pyroblast", "Presence of Mind", "Arcane Missiles", "Arcane Power", "Combustion",
    "Arcane Explosion", "Blizzard", "Flamestrike", "Evocation", "Arcane Intellect", "Amplify Magic",
    "Dampen Magic", "Ice Armor", "Mage Armor", "Slow Fall",
}
KNOWN = PRIEST | WARLOCK | DRUID | MAGE
# Names that exist but whose exact form is unconfirmed: macro must be flagged "verify".
UNCERTAIN = {"Healthstone", "Soulstone", "Summon Incubus", "Penance", "Prayer of Mending", "Binding Heal",
             "Fel Domination", "13", "14", "Nature's Swiftness", "Wild Growth", "Revive", "Dire Bear Form",
             "Lacerate", "Cyclone", "Arcane Blast", "Ice Lance", "Frostfire Bolt", "Mana Ruby"}
REMOVED = {"Curse of Agony", "Curse of Doom", "Curse of Shadows", "Dark Pact", "Command"}
OFF_GCD = {"Blood Fury", "Amplify Curse", "Fel Domination", "Inner Focus", "Will of the Forsaken",
           "Nature's Swiftness", "Presence of Mind", "Arcane Power", "Combustion"}
PET_SPELLS = {"Seduction", "Spell Lock", "Sacrifice", "Phase Shift", "Devour Magic", "Fire Shield",
              "Suffering", "Soothing Kiss", "Torment"}
ITEMS = {"Healthstone", "Soulstone", "Mana Ruby"}


def split_clauses(args):
    """Yield (conditions, target-text) for each ';' clause."""
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


def lint(macro):
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
        if cmd in ("/cast", "/spell", "/use"):
            spells = {rest.lstrip("!") for _, rest in clauses if rest and not rest.startswith("item:")}
            names |= spells
            if {s for s in spells if not s.isdigit()} - OFF_GCD - PET_SPELLS:
                gcd_lines += 1
        elif cmd == "/castsequence":
            seq = re.sub(r"^reset=\S+\s*", "", clauses[0][1])
            spells = {s.strip() for s in seq.split(",")}
            names |= spells
            gcd_lines += 1
        elif cmd in ("/cancelaura", "/startattack", "/cancelform"):
            names |= {rest for _, rest in clauses if rest}
    if gcd_lines > 1:
        errs.append(f"{gcd_lines} lines cast global-cooldown spells; only the first can fire per press")
    for n in names:
        if n in REMOVED:
            errs.append(f"'{n}' was removed or renamed in Forever")
        elif n not in KNOWN and n not in UNCERTAIN and n not in ITEMS and not n.isdigit():
            errs.append(f"unknown spell/item '{n}'")
        if n in UNCERTAIN and macro["status"] != "verify":
            errs.append(f"'{n}' is unconfirmed; mark the macro verify")
    if macro["status"] == "verify" and not macro.get("note"):
        errs.append("verify macro needs a note explaining what to check")
    return errs


def main(paths):
    failed = total = 0
    for path in paths:
        src = open(path, encoding="utf-8").read()
        m = re.search(r'<script type="application/json" id="macro-data">(.*?)</script>', src, re.S)
        data = json.loads(m.group(1))
        ids = [x["id"] for x in data["macros"]]
        if len(ids) != len(set(ids)):
            print(f"{path}: duplicate ids")
            failed += 1
        for x in data["macros"]:
            total += 1
            if x["section"] not in data["sections"]:
                print(f"{path}: {x['id']}: section '{x['section']}' not listed")
                failed += 1
            errs = lint(x)
            if errs:
                failed += 1
                print(f"FAIL {path}: {x['id']}: " + "; ".join(errs))
        verify = [x["id"] for x in data["macros"] if x["status"] == "verify"]
        print(f"{path}: {len(data['macros'])} macros, {len(verify)} flagged check-in-game: {', '.join(verify)}")
    print(f"{total - failed}/{total} passed" if failed else f"all {total} macros passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
