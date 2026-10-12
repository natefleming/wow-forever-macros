"""Rogue macros for WoW: Forever (Horde races: Orc, Undead, Troll)."""
from common import HARM, M_HARM, h, m, racials, trinket

POISON_NOTE = "Poison item names include the rank (Instant Poison VI, Deadly Poison V). Change them to the ranks in your bags."

MACROS = [
    # Openers & combo points
    m("opener", "Stealth opener / Sinister Strike", "Openers & combo points", ["PvP", "PvE"],
      "From stealth: Cheap Shot (stun), Ambush with Shift, Garrote with Ctrl. Out of stealth it Sinister Strikes. It won't start auto-attack while you're stealthed, so you don't break stealth by accident.",
      [["Stealthed", "Cheap Shot"], ["Stealthed + Shift", "Ambush"], ["Stealthed + Ctrl", "Garrote"], ["Otherwise", "Sinister Strike"]],
      "#showtooltip\n/startattack [nostealth]\n/cast [stealth,mod:shift] Ambush; [stealth,mod:ctrl] Garrote; [stealth] Cheap Shot; Sinister Strike"),
    m("builder", "Backstab / Hemorrhage", "Openers & combo points", ["PvE", "PvP"],
      "Dagger builder from behind, Hemorrhage (Subtlety talent) with Ctrl.",
      [["Click", "Backstab"], ["Ctrl", "Hemorrhage"]],
      "#showtooltip\n/startattack\n/cast [mod:ctrl] Hemorrhage; Backstab"),
    m("mutilate", "Mutilate", "Openers & combo points", ["PvE", "PvP", "Talent"],
      "New Assassination talent in Forever. Dual-dagger attack that hits harder on poisoned targets.",
      [["Click", "Mutilate"]], "#showtooltip\n/startattack\n/cast Mutilate",
      "verify", "New in Forever. Name taken from the beta talent tree."),
    m("finishers", "Finishers", "Openers & combo points", ["PvP", "PvE"],
      "All finishers on one key.", [["Click", "Eviscerate"], ["Shift", "Slice and Dice"], ["Ctrl", "Rupture"]],
      "#showtooltip\n/startattack\n/cast [mod:shift] Slice and Dice; [mod:ctrl] Rupture; Eviscerate"),

    # Control
    m("kick", "Kick", "Control", ["PvP", "PvE"],
      "Interrupt. Shift kicks your focus (the enemy healer) without swapping targets.", M_HARM, h("Kick")),
    m("kidney", "Kidney Shot", "Control", ["PvP"],
      "Finishing stun. Shift stuns your focus.", M_HARM, h("Kidney Shot")),
    m("gouge", "Gouge", "Control", ["PvP", "PvE"],
      "Short incapacitate. Shift gouges your focus.", M_HARM, h("Gouge")),
    m("blind", "Blind", "Control", ["PvP"],
      "Long disorient. Blind the focus healer, or the player you're not killing.", M_HARM, h("Blind")),
    m("sap", "Sap", "Control", ["PvP", "PvE"],
      "Sap from stealth. Shift saps your focus.", M_HARM, h("Sap")),
    m("distract", "Distract", "Control", ["PvP", "PvE"],
      "Turns enemies away so you can slip past. In Forever it also lowers their stealth detection.",
      [["Click", "Place Distract"]], "#showtooltip\n/cast Distract"),

    # Defensive
    m("vanish", "Vanish", "Defensive", ["PvP", "PvE"],
      "Stops auto-attack first, then Vanishes. Breaks roots and snares.", [["Click", "Vanish"]],
      "#showtooltip\n/stopattack\n/cast Vanish"),
    m("evasion", "Evasion / Sprint", "Defensive", ["PvP", "PvE"],
      "Survival cooldowns on one key.", [["Click", "Sprint"], ["Shift", "Evasion"]],
      "#showtooltip\n/cast [mod:shift] Evasion; Sprint"),
    m("feint", "Feint", "Defensive", ["PvE"],
      "Drops threat in dungeons and raids.", [["Click", "Feint"]], "#showtooltip\n/cast Feint"),
    m("stealth", "Stealth", "Defensive", ["PvP", "PvE"],
      "The ! keeps a second press from taking you out of stealth.", [["Click", "Stealth"]],
      "#showtooltip\n/cast !Stealth"),
    trinket("Defensive"),

    # Cooldowns & utility
    m("cooldowns", "Cold Blood / Adrenaline Rush / Blade Flurry", "Cooldowns & utility", ["PvP", "PvE", "Talent"],
      "Talent cooldowns on one key.", [["Click", "Cold Blood"], ["Shift", "Adrenaline Rush"], ["Ctrl", "Blade Flurry"]],
      "#showtooltip\n/cast [mod:shift] Adrenaline Rush; [mod:ctrl] Blade Flurry; Cold Blood", name="Cooldowns"),
    m("preparation", "Preparation", "Cooldowns & utility", ["PvP", "Talent"],
      "Resets Vanish, Evasion, Sprint and your other cooldowns.", [["Click", "Preparation"]],
      "#showtooltip\n/cast Preparation"),
    m("shadowstep", "Shadowstep", "Cooldowns & utility", ["PvP"],
      "Teleport behind your target. Shift steps to your focus.", M_HARM, h("Shadowstep"),
      "verify", "Only one source lists Shadowstep in Forever. Check your spellbook."),
    m("thistle-tea", "Thistle Tea", "Cooldowns & utility", ["PvE", "PvP"],
      "Restores 100 energy (5-minute cooldown).", [["Click", "Thistle Tea"]], "#showtooltip\n/use Thistle Tea"),
    m("poison-instant", "Poison: Instant / Deadly", "Cooldowns & utility", ["PvP", "PvE"],
      "Applies Instant Poison to your main hand; Shift applies Deadly Poison to your off hand.",
      [["Click", "Instant Poison, main hand"], ["Shift", "Deadly Poison, off hand"]],
      "#showtooltip\n/use [mod:shift] Deadly Poison V; Instant Poison VI\n/use [mod:shift] 17; 16",
      "verify", POISON_NOTE, name="Poison Main"),
    m("poison-pvp", "Poison: Crippling / Mind-numbing", "Cooldowns & utility", ["PvP"],
      "PvP poisons: Crippling to your main hand, Mind-numbing to your off hand with Shift.",
      [["Click", "Crippling Poison, main hand"], ["Shift", "Mind-numbing Poison, off hand"]],
      "#showtooltip\n/use [mod:shift] Mind-numbing Poison III; Crippling Poison II\n/use [mod:shift] 17; 16",
      "verify", POISON_NOTE, name="Poison PvP"),
] + racials(["Orc", "Undead", "Troll"], ["Sinister Strike", "Eviscerate"], melee=True)

SPELLS = {
    "Ambush", "Garrote", "Cheap Shot", "Sinister Strike", "Hemorrhage", "Backstab", "Mutilate",
    "Slice and Dice", "Rupture", "Eviscerate", "Kick", "Kidney Shot", "Gouge", "Blind", "Sap", "Distract",
    "Vanish", "Evasion", "Sprint", "Feint", "Stealth", "Adrenaline Rush", "Blade Flurry", "Cold Blood",
    "Preparation", "Shadowstep",
}
UNSURE = {"Mutilate", "Shadowstep", "Deadly Poison V", "Instant Poison VI",
          "Mind-numbing Poison III", "Crippling Poison II"}
