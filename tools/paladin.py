"""Paladin macros for WoW: Forever (Horde race: Undead, new in Forever)."""
from common import ANY, HARM, HELP, M_ANY, M_HARM, M_HELP, f, h, m, racials, trinket

MACROS = [
    # Healing
    m("holy-light", "Holy Light + Divine Favor", "Healing", ["PvE", "PvP"],
      "Big heal. Ctrl pops Divine Favor first (talent) for a guaranteed crit.",
      M_HELP + [["Ctrl", "Divine Favor first"]],
      f"#showtooltip Holy Light\n/cast [mod:ctrl] Divine Favor\n/cast {HELP} Holy Light", name="Holy Light"),
    m("flash-of-light", "Flash of Light", "Healing", ["PvP", "PvE"],
      "Fast, cheap heal. Shift heals your focus.", M_HELP, f("Flash of Light")),
    m("holy-shock", "Holy Shock", "Healing", ["PvP", "PvE", "Talent"],
      "Instant: heals a friend or damages an enemy depending on the target.", M_ANY,
      f"#showtooltip\n/cast {ANY} Holy Shock"),
    m("lay-on-hands", "Lay on Hands", "Healing", ["PvE", "PvP"],
      "Full heal for your focus, mouseover or yourself.", M_HELP, f("Lay on Hands")),
    m("cleanse", "Cleanse", "Healing", ["PvP", "PvE"],
      "Removes a poison, disease and magic effect. Shift cleanses your focus.", M_HELP, f("Cleanse")),
    m("blessings", "Blessings", "Healing", ["PvE"],
      "Three blessings on one key, on a friendly target, otherwise you. Here Shift and Ctrl choose the blessing, not the focus.",
      [["Click", "Might"], ["Shift", "Kings"], ["Ctrl", "Wisdom"]],
      "#showtooltip\n/cast [mod:shift,help][mod:shift,@player] Blessing of Kings; [mod:ctrl,help][mod:ctrl,@player] Blessing of Wisdom; [help][@player] Blessing of Might"),

    # Protection
    m("freedom", "Blessing of Freedom", "Protection", ["PvP"],
      "Frees your focus (or yourself) from roots and snares.", M_HELP, f("Blessing of Freedom"), name="BoFreedom"),
    m("bop", "Blessing of Protection", "Protection", ["PvP", "PvE"],
      "Physical immunity on your focus healer or a squishy mouseover.", M_HELP, f("Blessing of Protection"),
      name="BoProtection"),
    m("sacrifice", "Blessing of Sacrifice", "Protection", ["PvP", "PvE"],
      "Takes some of your focus's damage. Can break crowd control on them in PvP.", M_HELP,
      f("Blessing of Sacrifice"), name="BoSacrifice"),
    m("bubble", "Divine Shield / Divine Protection", "Protection", ["PvP", "PvE"],
      "Bubble. Pressing it again while shielded cancels Divine Shield early. Shift casts Divine Protection instead.",
      [["Click", "Divine Shield (again to cancel)"], ["Shift", "Divine Protection"]],
      "#showtooltip\n/stopcasting\n/cancelaura [nomod] Divine Shield\n/cast [mod:shift] Divine Protection; Divine Shield",
      name="Bubble"),
    trinket("Protection"),

    # Seals & judgement
    m("judge-reseal", "Judgement + reseal", "Seals & judgement", ["PvP", "PvE"],
      "Judges your seal (off the global cooldown in Forever) and puts a new one up in the same press.",
      [["Click", "Judge, then Seal of Righteousness"], ["Shift", "Judge, then Seal of the Crusader"], ["Ctrl", "Judge, then Seal of Wisdom"]],
      "#showtooltip Judgement\n/startattack\n/cast Judgement\n/cast [mod:shift] Seal of the Crusader; [mod:ctrl] Seal of Wisdom; Seal of Righteousness",
      name="Judge Reseal"),
    m("seals", "Seals", "Seals & judgement", ["PvE", "PvP"],
      "Pick a seal. In Forever Seal of Light and Seal of Wisdom aren't used up when you judge them.",
      [["Click", "Command"], ["Shift", "Justice"], ["Ctrl", "Light"]],
      "#showtooltip\n/cast [mod:shift] Seal of Justice; [mod:ctrl] Seal of Light; Seal of Command"),
    m("seal-of-fury", "Seal of Fury", "Seals & judgement", ["PvE"],
      "New tanking seal in Forever. Judging it taunts.", [["Click", "Seal of Fury"]],
      "#showtooltip\n/cast Seal of Fury", "verify", "New in Forever. Name taken from the beta spellbook."),
    m("holy-strike", "Holy Strike", "Seals & judgement", ["PvE", "PvP"],
      "New baseline melee attack: weapon damage plus holy damage.", [["Click", "Holy Strike"]],
      "#showtooltip\n/startattack\n/cast Holy Strike", "verify", "New in Forever. Name taken from the beta spellbook."),

    # Control & damage
    m("hoj", "Hammer of Justice", "Control & damage", ["PvP", "PvE"],
      "Stun or interrupt. Shift stuns your focus.", M_HARM, h("Hammer of Justice")),
    m("repentance", "Repentance", "Control & damage", ["PvP", "Talent"],
      "Retribution talent: 6-second incapacitate on your focus.", M_HARM, h("Repentance")),
    m("turn-undead", "Turn Undead", "Control & damage", ["PvP", "PvE"],
      "Fears undead, including Forsaken players. Shift turns your focus.", M_HARM, h("Turn Undead")),
    m("hammer-of-wrath", "Hammer of Wrath", "Control & damage", ["PvP", "PvE"],
      "Ranged execute. Shift throws it at your focus.", M_HARM, h("Hammer of Wrath")),
    m("exorcism", "Exorcism", "Control & damage", ["PvE", "PvP"],
      "Works on undead and demons only: Forsaken players, warlock pets.", M_HARM, h("Exorcism")),
    m("aoe", "Consecration / Holy Wrath", "Control & damage", ["PvE"],
      "AoE. Holy Wrath only hits undead and demons.", [["Click", "Consecration"], ["Ctrl", "Holy Wrath"]],
      "#showtooltip\n/cast [mod:ctrl] Holy Wrath; Consecration"),

    # Auras & tanking
    m("auras", "Auras", "Auras & tanking", ["PvE", "PvP"],
      "Auras on one key.", [["Click", "Devotion"], ["Shift", "Retribution"], ["Ctrl", "Concentration"]],
      "#showtooltip\n/cast [mod:shift] Retribution Aura; [mod:ctrl] Concentration Aura; Devotion Aura"),
    m("righteous-fury", "Righteous Fury / Holy Shield", "Auras & tanking", ["PvE"],
      "Tank setup. The ! stops a second press from turning Righteous Fury off. Shift casts Holy Shield (talent).",
      [["Click", "Righteous Fury"], ["Shift", "Holy Shield"]],
      "#showtooltip\n/cast [mod:shift] Holy Shield; !Righteous Fury", name="Righteous Fury"),
] + racials(["Undead"], [])

SPELLS = {
    "Holy Light", "Divine Favor", "Flash of Light", "Holy Shock", "Lay on Hands", "Cleanse",
    "Blessing of Kings", "Blessing of Wisdom", "Blessing of Might", "Blessing of Freedom",
    "Blessing of Protection", "Blessing of Sacrifice", "Divine Protection", "Divine Shield", "Judgement",
    "Seal of the Crusader", "Seal of Wisdom", "Seal of Righteousness", "Seal of Justice", "Seal of Light",
    "Seal of Command", "Seal of Fury", "Holy Strike", "Hammer of Justice", "Repentance", "Turn Undead",
    "Hammer of Wrath", "Exorcism", "Holy Wrath", "Consecration", "Retribution Aura", "Concentration Aura",
    "Devotion Aura", "Holy Shield", "Righteous Fury",
}
UNSURE = {"Seal of Fury", "Holy Strike"}
