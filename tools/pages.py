"""Registry of pages: order here is the order on the index hub."""
import druid
import general
import hunter
import mage
import paladin
import priest
import rogue
import shaman
import warlock
import warrior


def page(mod, title, file, races, sections):
    return dict(title=title, file=file, macros=mod.MACROS, races=races, spells=mod.SPELLS, unsure=mod.UNSURE,
                sections=sections + (["Racials"] if races else []))


PAGES = {
    "general": page(general, "All characters", "general.html", [],
                    ["Focus & targeting", "Travel", "Combat", "Group", "Interface"]),
    "warrior": page(warrior, "Warrior", "warrior.html", ["Orc", "Undead", "Tauren", "Troll"],
                    ["Gap closers & interrupts", "Attacks", "Tanking", "Cooldowns & shouts"]),
    "paladin": page(paladin, "Paladin", "paladin.html", ["Undead"],
                    ["Healing", "Protection", "Seals & judgement", "Control & damage", "Auras & tanking"]),
    "hunter": page(hunter, "Hunter", "hunter.html", ["Orc", "Tauren", "Troll"],
                   ["Shots", "Control", "Melee & defensive", "Pet"]),
    "rogue": page(rogue, "Rogue", "rogue.html", ["Orc", "Undead", "Troll"],
                  ["Openers & combo points", "Control", "Defensive", "Cooldowns & utility"]),
    "priest": page(priest, "Priest", "priest.html", ["Undead", "Troll"],
                   ["Healing", "Dispels", "PvP control", "PvP defensive", "Damage", "Talent & spec"]),
    "shaman": page(shaman, "Shaman", "shaman.html", ["Orc", "Tauren", "Troll"],
                   ["Healing", "Shocks & spells", "Totems", "Buffs & utility"]),
    "mage": page(mage, "Mage", "mage.html", ["Orc", "Undead", "Troll"],
                 ["Control", "Defensive", "Damage", "Burst & AoE", "Utility"]),
    "warlock": page(warlock, "Warlock", "warlock.html", ["Orc", "Undead", "Troll"],
                    ["Pets", "Curses & banes", "Control", "Damage", "Sacrifice & summon", "Survival"]),
    "druid": page(druid, "Druid", "druid.html", ["Tauren"],
                  ["Healing", "Dispels", "Forms & mobility", "Feral", "Control", "Balance"]),
}
