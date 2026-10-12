"""Registry of class pages: order here is the order on the index hub."""
from druid import DRUID
from macros import PRIEST, WARLOCK
from mage import MAGE

PAGES = {
    "priest": dict(title="Undead Priest", file="priest.html", macros=PRIEST,
                   sections=["Focus & utility", "Healing", "Dispels", "PvP control", "PvP defensive", "Damage", "Talent & spec"]),
    "warlock": dict(title="Orc Warlock", file="warlock.html", macros=WARLOCK,
                    sections=["Focus & utility", "Pets", "Curses & banes", "Control", "Damage (auto Blood Fury)", "Sacrifice & summon", "Survival"]),
    "druid": dict(title="Tauren Druid", file="druid.html", macros=DRUID,
                  sections=["Focus & utility", "Healing", "Dispels", "Forms & mobility", "Feral", "Control", "Balance", "PvP"]),
    "mage": dict(title="Orc Mage", file="mage.html", macros=MAGE,
                 sections=["Focus & utility", "Control", "Defensive", "Damage (auto Blood Fury)", "Burst & AoE", "Utility"]),
}
