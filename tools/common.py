"""Shared helpers for the WoW: Forever macro data.

Conventions used throughout:
  click = target (mouseover first where useful), Shift = focus, Alt = self,
  Ctrl = alternate spell / add an off-GCD helper.
"""

# Target patterns
HARM = "[@focus,mod:shift,harm,nodead][@mouseover,harm,nodead][]"
HELP = "[@focus,mod:shift,help,nodead][@player,mod:alt][@mouseover,help,nodead][help,nodead][@player]"
ANY = "[@focus,mod:shift,exists,nodead][@player,mod:alt][@mouseover,exists,nodead][exists,nodead][@player]"
DEAD = "[@focus,mod:shift,help,dead][@mouseover,help,dead][help,dead]"

M_HARM = [["Click", "Mouseover, else target"], ["Shift", "Focus"]]
M_HELP = [["Click", "Mouseover, else friendly target, else you"], ["Shift", "Focus"], ["Alt", "You"]]
M_ANY = [["Click", "Mouseover, else target (friend or foe), else you"], ["Shift", "Focus"], ["Alt", "You"]]
M_DEAD = [["Click", "Dead mouseover, else dead target"], ["Shift", "Focus"]]

TRINKET_NOTE = "Put your PvP trinket (Insignia of the Horde) in the top trinket slot (13), or change 13 to 14. Check its tooltip in Forever for what it breaks."


def m(id, title, section, tags, desc, mods, text, status="ok", note="", race=None, name=None):
    if name is None:
        name = id.replace("-", " ").title()[:16].rstrip()
    return dict(id=id, title=title, section=section, tags=tags, desc=desc, mods=mods,
                text=text.strip("\n"), status=status, note=note, race=race, name=name)


def h(spell):
    """Hostile spell on focus/mouseover/target."""
    return f"#showtooltip\n/cast {HARM} {spell}"


def f(spell):
    """Friendly spell on focus/self/mouseover/target."""
    return f"#showtooltip\n/cast {HELP} {spell}"


def trinket(section="PvP defensive"):
    return m("trinket", "PvP trinket", section, ["PvP"],
             "Breaks crowd control with the trinket in slot 13. Ctrl uses slot 14 instead.",
             [["Click", "Slot 13"], ["Ctrl", "Slot 14"]], "#showtooltip\n/use [mod:ctrl] 14; 13",
             "verify", TRINKET_NOTE, name="PvP Trinket")


# ---------------------------------------------------------------- racials
# Forever racial actives (research, October 2026):
#   Orc     Blood Fury      +10% AP and SP for 15 s, 2 min, off the global cooldown
#   Troll   Berserking      +10% cast and attack speed for 10 s, 3 min, off the global cooldown
#   Undead  Will of the Forsaken (fear/charm/sleep), Cannibalize
#   Tauren  War Stomp       2 s area stun, 0.5 s cast, 2 min
RACIAL = {"Orc": "Blood Fury", "Troll": "Berserking"}
RACIAL_SPELLS = {"Blood Fury": "Orc", "Berserking": "Troll", "Will of the Forsaken": "Undead",
                 "Cannibalize": "Undead", "Touch of Weakness": "Undead", "Dark Sacrifice": "Undead",
                 "War Stomp": "Tauren", "Shadowguard": "Troll", "Hex of Weakness": "Troll"}
ABBR = {"Blood Fury": "BF", "Berserking": "Zerk"}
BURST_DESC = {"Blood Fury": "Blood Fury (+10% attack and spell power)",
              "Berserking": "Berserking (+10% casting and attack speed)"}


def racials(races, nukes, melee=False):
    """Racial macros for each race in `races`.

    nukes: spells that get the Orc/Troll cooldown cast in front of them.
    melee: True for melee attacks (adds /startattack, targets the current target only).
    """
    cards = []
    for race in races:
        if race in RACIAL:
            cd = RACIAL[race]
            for spell in nukes:
                slug = spell.lower().replace("'", "").replace(" ", "-")
                if melee:
                    text = f"#showtooltip {spell}\n/startattack\n/cast {cd}\n/cast {spell}"
                    mods = [["Click", "Your target"], ["Auto", f"{cd} whenever it's ready"]]
                else:
                    text = f"#showtooltip {spell}\n/cast {cd}\n/cast {HARM} {spell}"
                    mods = M_HARM + [["Auto", f"{cd} whenever it's ready"]]
                cards.append(m(f"{race.lower()}-{slug}", f"{spell} + {cd}", "Racials", ["PvP", "PvE"],
                               f"{spell} with {BURST_DESC[cd]} cast automatically whenever it's off cooldown.",
                               mods, text, race=race, name=f"{ABBR[cd]} {spell}"[:16].rstrip(),
                               note=(f"{cd} is off the global cooldown, so it goes out with the spell whenever it's ready "
                                     "and is skipped otherwise. To hide the 'Spell is not ready yet' message, "
                                     "add /run UIErrorsFrame:Clear() as a last line.")))
        if race == "Undead":
            cards.append(m("undead-wotf", "Will of the Forsaken / PvP trinket", "Racials", ["PvP"],
                           "Click breaks fear, charm and sleep with Will of the Forsaken. Shift uses the PvP trinket in slot 13 for stuns and everything else. They're on separate cooldowns, so pressing one never wastes the other.",
                           [["Click", "Will of the Forsaken"], ["Shift", "Trinket in slot 13"]],
                           "#showtooltip\n/use [mod:shift] 13\n/cast [nomod] Will of the Forsaken",
                           "verify", TRINKET_NOTE, race=race, name="WotF Trinket"))
            cards.append(m("undead-cannibalize", "Cannibalize", "Racials", ["PvP", "PvE"],
                           "Eat a nearby humanoid or undead corpse to recover health (2-minute cooldown). Moving or taking damage cancels it.",
                           [["Click", "Cannibalize"]], "#showtooltip\n/cast Cannibalize", race=race))
        if race == "Tauren":
            cards.append(m("tauren-war-stomp", "War Stomp / PvP trinket", "Racials", ["PvP"],
                           "Click War Stomps: a 2-second area stun with a short 0.5-second cast. Shift uses the PvP trinket in slot 13. They're on separate cooldowns.",
                           [["Click", "War Stomp"], ["Shift", "Trinket in slot 13"]],
                           "#showtooltip\n/use [mod:shift] 13\n/cast [nomod] War Stomp",
                           "verify", TRINKET_NOTE, race=race, name="Stomp Trinket"))
    return cards
