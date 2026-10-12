"""Priest macros for WoW: Forever (Horde races: Undead, Troll)."""
from common import ANY, HARM, HELP, M_ANY, M_HARM, M_HELP, h, f, m, racials, trinket

MACROS = [

    # Healing
    m("flash-heal", "Flash Heal", "Healing", ["PvP", "PvE"],
      "Fast heal. Mouseover healing on party/raid frames, Shift to keep your focus (tank or arena partner) alive.",
      M_HELP, f"#showtooltip\n/cast {HELP} Flash Heal"),
    m("greater-heal", "Greater Heal + Inner Focus", "Healing", ["PvE"],
      "Big heal. Hold Ctrl to pop Inner Focus first (off the global cooldown) for a free, high-crit Greater Heal.",
      M_HELP + [["Ctrl", "Inner Focus first"]],
      f"#showtooltip Greater Heal\n/cast [mod:ctrl] Inner Focus\n/cast {HELP} Greater Heal"),
    m("heal", "Heal", "Healing", ["PvE"],
      "Mana-efficient heal for long raid fights.", M_HELP, f"#showtooltip\n/cast {HELP} Heal"),
    m("renew", "Renew", "Healing", ["PvP", "PvE"],
      "Instant HoT. Keep it rolling on your focus while kiting.", M_HELP, f"#showtooltip\n/cast {HELP} Renew"),
    m("pws", "Power Word: Shield", "Healing", ["PvP", "PvE"],
      "Bubble. Alt shields yourself without dropping your enemy target.", M_HELP,
      f"#showtooltip\n/cast {HELP} Power Word: Shield"),
    m("buffs", "Buffs", "Healing", ["PvE"],
      "Three buffs on one key. Casts on a friendly target, otherwise you. Here Shift and Ctrl choose the buff, not the focus.",
      [["Click", "Power Word: Fortitude"], ["Shift", "Divine Spirit"], ["Ctrl", "Shadow Protection"]],
      """
#showtooltip
/cast [mod:shift,help][mod:shift,@player] Divine Spirit; [mod:ctrl,help][mod:ctrl,@player] Shadow Protection; [help][@player] Power Word: Fortitude
"""),

    # Dispels
    m("dispel", "Dispel Magic", "Dispels", ["PvP", "PvE"],
      "Cleanses a friend or purges an enemy; the target decides. Shift purges or cleanses your focus.",
      M_ANY, f"#showtooltip\n/cast {ANY} Dispel Magic"),
    m("abolish", "Abolish Disease", "Dispels", ["PvE", "PvP"],
      "Removes a disease and keeps checking for new ones for a few seconds. Good on tanks in plague-heavy dungeons.",
      M_HELP, f"#showtooltip\n/cast {HELP} Abolish Disease"),
    m("fear-ward", "Fear Ward", "Dispels", ["PvP", "PvE"],
      "Baseline for every Priest in Forever. Pre-ward your focus before a warlock or warrior can fear them.",
      M_HELP, f"#showtooltip\n/cast {HELP} Fear Ward"),

    # PvP control
    m("silence", "Silence", "PvP control", ["PvP", "PvE", "Talent"],
      "Stops your own cast first so the interrupt goes out instantly. Shift silences your focus (enemy healer) without swapping targets.",
      M_HARM, f"#showtooltip\n/stopcasting\n/cast {HARM} Silence"),
    m("scream", "Psychic Scream", "PvP control", ["PvP"],
      "Cancels your current cast and fears everything in melee range.",
      [["Click", "Fear nearby enemies"]], "#showtooltip\n/stopcasting\n/cast Psychic Scream"),
    m("mind-control", "Mind Control", "PvP control", ["PvP"],
      "Shift mind-controls your focus. Park a healer on a ledge or walk a flag carrier into your team.",
      M_HARM, f"#showtooltip\n/cast {HARM} Mind Control"),
    m("mana-burn", "Mana Burn", "PvP control", ["PvP"],
      "Burn the enemy healer's mana from focus while keeping your current target.", M_HARM,
      f"#showtooltip\n/cast {HARM} Mana Burn"),
    m("shackle", "Shackle Undead", "PvP control", ["PvP", "PvE"],
      "Shift re-shackles your focused undead: another Forsaken in PvP, or your CC target in dungeons.",
      M_HARM, f"#showtooltip\n/cast {HARM} Shackle Undead"),
    m("holy-nova", "Holy Nova", "PvP control", ["PvP"],
      "Cancels your cast and pulses Holy Nova, which knocks nearby rogues and druids out of stealth.",
      [["Click", "Holy Nova"]], "#showtooltip\n/stopcasting\n/cast Holy Nova"),

    # PvP defensive
    trinket(),
    m("inner-fire", "Inner Fire", "PvP defensive", ["PvP", "PvE"],
      "Keeps Inner Fire up: armor and spell power.", [["Click", "Inner Fire"]], "#showtooltip\n/cast Inner Fire"),
    m("shadowform-heal", "Drop Shadowform + Flash Heal", "PvP defensive", ["PvP", "Talent"],
      "Leaves Shadowform and heals in the same press. Shift heals your focus instead of you.",
      [["Click", "Heal you"], ["Shift", "Heal focus"]],
      "#showtooltip Flash Heal\n/cancelaura Shadowform\n/cast [@focus,mod:shift,help,nodead][@player] Flash Heal"),
    m("fade", "Fade", "PvP defensive", ["PvE"],
      "Stops your cast and drops threat for when a heal pulls aggro.",
      [["Click", "Fade"]], "#showtooltip\n/stopcasting\n/cast Fade"),

    # Damage
    m("swp", "Shadow Word: Pain", "Damage", ["PvP", "PvE"],
      "DoT your focus or mouseover without losing your target. Spread it on rogues before they vanish.",
      M_HARM, f"#showtooltip\n/cast {HARM} Shadow Word: Pain"),
    m("plague", "Devouring Plague", "Damage", ["PvP", "PvE"],
      "Baseline for every Priest in Forever. Heals you as it ticks.", M_HARM,
      f"#showtooltip\n/cast {HARM} Devouring Plague"),
    m("mind-blast", "Mind Blast + Inner Focus", "Damage", ["PvP", "PvE"],
      "Ctrl adds Inner Focus (off the global cooldown) for a free, high-crit Mind Blast.",
      M_HARM + [["Ctrl", "Inner Focus first"]],
      f"#showtooltip Mind Blast\n/cast [mod:ctrl] Inner Focus\n/cast {HARM} Mind Blast"),
    m("swd", "Shadow Word: Death", "Damage", ["PvP", "PvE"],
      "Baseline at level 32. Execute your low-health focus without swapping targets.", M_HARM,
      f"#showtooltip\n/cast {HARM} Shadow Word: Death"),
    m("mind-flay", "Mind Flay (no clipping)", "Damage", ["PvP", "PvE", "Talent"],
      "Won't restart the channel if you press it while already channeling, so spamming it never clips ticks.",
      M_HARM,
      "#showtooltip\n/cast [nochanneling,@focus,mod:shift,harm,nodead][nochanneling,@mouseover,harm,nodead][nochanneling] Mind Flay"),
    m("smite", "Smite / Holy Fire", "Damage", ["PvE"],
      "Holy leveling and solo damage on one key.",
      [["Click", "Smite"], ["Ctrl", "Holy Fire"]],
      "#showtooltip\n/cast [mod:ctrl] Holy Fire; Smite"),

    # Talent & spec
    m("power-infusion", "Power Infusion", "Talent & spec", ["PvP", "PvE", "Talent"],
      "Shift gives Power Infusion to your focus (your mage or warlock) mid-fight.", M_HELP,
      f"#showtooltip\n/cast {HELP} Power Infusion"),
    m("penance", "Penance", "Talent & spec", ["PvP", "PvE", "Talent"],
      "New Discipline spell. Heals a friend or damages an enemy depending on the target.", M_ANY,
      f"#showtooltip\n/cast {ANY} Penance",
      "verify", "New in Forever. Confirm in-game that one Penance spell does both damage and healing."),
    m("pom", "Prayer of Mending", "Talent & spec", ["PvE", "PvP", "Talent"],
      "Holy capstone. Put it on your focus tank so it starts bouncing from the player taking damage.", M_HELP,
      f"#showtooltip\n/cast {HELP} Prayer of Mending", "verify", "New in Forever. Name taken from the beta spellbook."),
    m("binding-heal", "Binding Heal", "Talent & spec", ["PvE", "PvP", "Talent"],
      "Heals you and another player at once. Shift heals you and your focus.",
      [["Click", "Mouseover, else friendly target"], ["Shift", "Focus"]],
      "#showtooltip\n/cast [@focus,mod:shift,help,nodead][@mouseover,help,nodead][help,nodead] Binding Heal",
      "verify", "New in Forever. Name taken from the beta spellbook."),
    m("shadowform", "Shadowform (no toggle-off)", "Talent & spec", ["PvP", "PvE", "Talent"],
      "The ! keeps a second press from dropping you out of Shadowform. Pair it with Drop Shadowform + Flash Heal to step out on purpose.",
      [["Click", "Enter Shadowform"]], "#showtooltip\n/cast !Shadowform"),
    m("ve", "Vampiric Embrace", "Talent & spec", ["PvP", "PvE", "Talent"],
      "Shadow self-healing debuff on your target or focus.", M_HARM,
      f"#showtooltip\n/cast {HARM} Vampiric Embrace"),

    # Racials: Undead
    m("undead-touch", "Touch of Weakness", "Racials", ["PvP", "PvE"],
      "Undead Priest only. Your next melee attacker takes shadow damage and loses attack power. Keep it up in PvP.",
      [["Click", "Touch of Weakness"]], "#showtooltip\n/cast Touch of Weakness", race="Undead", name="Touch Weakness"),
    m("undead-dark-sacrifice", "Dark Sacrifice", "Racials", ["PvE", "PvP"],
      "Undead Priest only. Turns health into mana over 15 seconds (10-minute cooldown). Pair it with a Renew on yourself.",
      [["Click", "Dark Sacrifice"]], "#showtooltip\n/cast Dark Sacrifice", race="Undead", name="Dark Sacrifice"),

    # Racials: Troll
    m("troll-shadowguard", "Shadowguard", "Racials", ["PvP", "PvE"],
      "Troll Priest only. Melee and ranged attackers get hit with shadow damage.",
      [["Click", "Shadowguard"]], "#showtooltip\n/cast Shadowguard", race="Troll"),
    m("troll-hex", "Hex of Weakness", "Racials", ["PvP", "PvE"],
      "Troll Priest only. Weakens your target's damage and the healing they receive. Shift hexes your focus.",
      M_HARM, h("Hex of Weakness"), race="Troll", name="Hex Weakness"),
] + racials(["Undead", "Troll"], ["Mind Blast", "Smite"])

SPELLS = {
    "Flash Heal", "Greater Heal", "Heal", "Renew", "Power Word: Shield", "Power Word: Fortitude",
    "Divine Spirit", "Shadow Protection", "Dispel Magic", "Abolish Disease", "Fear Ward", "Silence",
    "Psychic Scream", "Mind Control", "Mana Burn", "Shackle Undead", "Holy Nova", "Shadowform", "Fade",
    "Inner Fire", "Shadow Word: Pain", "Devouring Plague", "Mind Blast", "Inner Focus", "Shadow Word: Death",
    "Mind Flay", "Smite", "Holy Fire", "Power Infusion", "Penance", "Prayer of Mending", "Binding Heal",
    "Vampiric Embrace",
}
UNSURE = {"Penance", "Prayer of Mending", "Binding Heal"}
