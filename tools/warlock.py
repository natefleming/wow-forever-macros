"""Warlock macros for WoW: Forever (Horde races: Orc, Undead, Troll)."""
from common import ANY, HARM, HELP, M_ANY, M_HARM, M_HELP, h, f, m, racials, trinket

MACROS = [

    # Pets
    m("pet-special", "Pet special (every demon)", "Pets", ["PvP", "PvE"],
      "One key for whichever demon is out: Succubus/Incubus Seduction, Felhunter Spell Lock, Voidwalker Sacrifice, Imp Phase Shift. Shift aims Seduction or Spell Lock at your focus.",
      [["Click", "Your target"], ["Shift", "Focus (Seduction, Spell Lock)"]],
      """
#showtooltip
/cast [pet:Succubus/Incubus,@focus,mod:shift,harm][pet:Succubus/Incubus] Seduction; [pet:Felhunter,@focus,mod:shift,harm][pet:Felhunter] Spell Lock; [pet:Voidwalker] Sacrifice; [pet:Imp] Phase Shift
""", "verify", "Confirm [pet:Incubus] matches the new Incubus in-game. If it doesn't, replace Incubus with your demon's name."),
    m("pet-utility", "Pet utility / dispel (every demon)", "Pets", ["PvP", "PvE"],
      "Felhunter Devour Magic cleanses a friend or purges an enemy, falling back to you. Also Imp Fire Shield (friendly target, else you), Voidwalker Suffering and Succubus Soothing Kiss.",
      [["Click", "Mouseover, else target, else you"], ["Shift", "Focus (Devour Magic)"]],
      """
#showtooltip
/cast [pet:Felhunter,@focus,mod:shift,exists][pet:Felhunter,@mouseover,exists][pet:Felhunter,exists][pet:Felhunter,@player] Devour Magic; [pet:Imp,help][pet:Imp,@player] Fire Shield; [pet:Voidwalker] Suffering; [pet] Soothing Kiss
"""),
    m("pet-attack", "Pet attack / follow / passive", "Pets", ["PvP", "PvE"],
      "Send your pet in. A Voidwalker also Torments to grab threat. Shift sends it at your focus.",
      [["Click", "Attack target"], ["Shift", "Attack focus"], ["Ctrl", "Follow"], ["Alt", "Passive"]],
      """
/petfollow [mod:ctrl]
/petpassive [mod:alt]
/stopmacro [mod:ctrl][mod:alt]
/petattack [@focus,mod:shift,harm,nodead][]
/cast [pet:Voidwalker,@focus,mod:shift,harm][pet:Voidwalker] Torment
"""),

    # Curses & banes
    m("tongues", "Curse of Tongues", "Curses & banes", ["PvP", "PvE"],
      "Slows casting. Shift keeps it on the enemy healer (focus) while you damage someone else.", M_HARM,
      f"#showtooltip\n/cast {HARM} Curse of Tongues"),
    m("exhaustion", "Curse of Exhaustion + Amplify Curse", "Curses & banes", ["PvP", "Talent"],
      "Snare. Ctrl casts Amplify Curse first (off the global cooldown) for a stronger slow.",
      M_HARM + [["Ctrl", "Amplify Curse first"]],
      f"#showtooltip Curse of Exhaustion\n/cast [mod:ctrl] Amplify Curse\n/cast {HARM} Curse of Exhaustion"),
    m("weakness", "Curse of Weakness", "Curses & banes", ["PvP", "PvE"],
      "Lowers attack power. Put it on the warrior or rogue chasing your healer.", M_HARM,
      f"#showtooltip\n/cast {HARM} Curse of Weakness"),
    m("recklessness", "Curse of Recklessness", "Curses & banes", ["PvP", "PvE"],
      "Lowers armor and stops the target from fleeing in fear.", M_HARM,
      f"#showtooltip\n/cast {HARM} Curse of Recklessness"),
    m("elements", "Curse of the Elements", "Curses & banes", ["PvE"],
      "In Forever this raises all magic damage taken. The raid curse.", M_HARM,
      f"#showtooltip\n/cast {HARM} Curse of the Elements"),
    m("agony", "Bane of Agony + Amplify Curse", "Curses & banes", ["PvP", "PvE"],
      "Formerly Curse of Agony. Banes sit alongside your curse. Ctrl adds Amplify Curse.",
      M_HARM + [["Ctrl", "Amplify Curse first"]],
      f"#showtooltip Bane of Agony\n/cast [mod:ctrl] Amplify Curse\n/cast {HARM} Bane of Agony"),
    m("doom", "Bane of Doom", "Curses & banes", ["PvE"],
      "Formerly Curse of Doom. For long boss fights.", M_HARM, f"#showtooltip\n/cast {HARM} Bane of Doom"),
    m("havoc", "Bane of Havoc", "Curses & banes", ["PvE", "PvP", "Talent"],
      "Put it on your focus as the second target. Part of the damage you deal to your main target is copied onto it.", M_HARM,
      f"#showtooltip\n/cast {HARM} Bane of Havoc"),

    # Control
    m("fear", "Fear", "Control", ["PvP", "PvE"],
      "Shift fears your focus (enemy healer) without dropping your kill target.", M_HARM,
      f"#showtooltip\n/cast {HARM} Fear"),
    m("death-coil", "Death Coil", "Control", ["PvP"],
      "Instant horror and self-heal. Stops your cast first so it goes out immediately. Your best peel.",
      M_HARM, f"#showtooltip\n/stopcasting\n/cast {HARM} Death Coil"),
    m("howl", "Howl of Terror", "Control", ["PvP", "Talent"],
      "Stops your cast and fears everyone around you.", [["Click", "Fear nearby enemies"]],
      "#showtooltip\n/stopcasting\n/cast Howl of Terror"),
    m("banish", "Banish", "Control", ["PvE", "PvP"],
      "Shift re-banishes your focused demon or elemental.", M_HARM, f"#showtooltip\n/cast {HARM} Banish"),
    m("drain-mana", "Drain Mana", "Control", ["PvP"],
      "Drain the enemy healer on focus.", M_HARM, f"#showtooltip\n/cast {HARM} Drain Mana"),

    # Damage
    m("shadow-bolt", "Shadow Bolt", "Damage", ["PvP", "PvE"],
      "Your main nuke. Shift casts it at your focus.", M_HARM, h("Shadow Bolt")),
    m("incinerate", "Incinerate", "Damage", ["PvE", "PvP", "Talent"],
      "Destruction 31-point talent. Hits harder on targets with Immolate.", M_HARM, h("Incinerate")),
    m("immolate", "Immolate", "Damage", ["PvP", "PvE"],
      "Fire DoT opener.", M_HARM, h("Immolate")),
    m("conflagrate", "Conflagrate", "Damage", ["PvP", "PvE", "Talent"],
      "Instant burst on an Immolated target.", M_HARM, h("Conflagrate")),
    m("shadowburn", "Shadowburn", "Damage", ["PvP", "Talent"],
      "Instant finisher. Can refund its Soul Shard in Forever.", M_HARM, h("Shadowburn")),
    m("searing-pain", "Searing Pain", "Damage", ["PvP"],
      "Fast fire spam to finish a kiting fight.", M_HARM, h("Searing Pain")),
    m("soul-fire", "Soul Fire", "Damage", ["PvE"],
      "Big opener, and the Decimation execute.", M_HARM, h("Soul Fire")),
    m("corruption", "Corruption", "Damage", ["PvP", "PvE"],
      "DoT your focus or mouseover to spread pressure.", M_HARM, f"#showtooltip\n/cast {HARM} Corruption"),
    m("siphon-life", "Siphon Life", "Damage", ["PvP", "PvE", "Talent"],
      "Affliction drain-heal DoT on focus or mouseover.", M_HARM, f"#showtooltip\n/cast {HARM} Siphon Life"),

    # Sacrifice & summon
    m("sacrifice", "Demonic Sacrifice", "Sacrifice & summon", ["PvP", "PvE", "Talent"],
      "Sacrifices your active demon for its buff: Imp for shadow damage, Succubus/Incubus for fire damage, Voidwalker for mana, Felhunter for health.",
      [["Click", "Sacrifice current demon"]],
      "#showtooltip Demonic Sacrifice\n/cast Demonic Sacrifice"),
    m("fel-summon", "Summon any demon (Fel Domination in combat)", "Sacrifice & summon", ["PvP", "PvE"],
      "In combat it pops Fel Domination first (off the global cooldown) for a near-instant summon. Out of combat it summons normally and saves the cooldown.",
      [["Click", "Felhunter"], ["Shift", "Succubus"], ["Ctrl", "Imp"], ["Alt", "Voidwalker"], ["Ctrl+Shift", "Incubus"]],
      """
#showtooltip
/cast [combat] Fel Domination
/cast [mod:ctrl,mod:shift] Summon Incubus; [mod:shift] Summon Succubus; [mod:ctrl] Summon Imp; [mod:alt] Summon Voidwalker; Summon Felhunter
""", "verify", "Fel Domination's cooldown in Forever is reported as both 5 and 15 minutes. Check the tooltip."),
    m("sac-resummon", "Sacrifice, then resummon", "Sacrifice & summon", ["PvP", "PvE", "Talent"],
      "Press twice. The first press sacrifices your demon (and pops Fel Domination in combat); the second summons a Felhunter. With the Demonic Pact talent your sacrifice buff stays when you summon a different demon. Resets after 15 seconds.",
      [["1st press", "Demonic Sacrifice"], ["2nd press", "Summon Felhunter"]],
      """
#showtooltip
/cast [combat] Fel Domination
/castsequence reset=15 Demonic Sacrifice, Summon Felhunter
""", "verify", "Swap Summon Felhunter for whichever demon you want after the sacrifice. Summoning the same demon you sacrificed removes the buff."),

    # Survival
    m("trinket", "PvP trinket", "Survival", ["PvP"],
      "Breaks crowd control with the trinket in slot 13. Ctrl uses slot 14 instead.",
      [["Click", "Slot 13"], ["Ctrl", "Slot 14"]], "#showtooltip\n/use [mod:ctrl] 14; 13",
      "verify", "Check your Insignia of the Horde tooltip in Forever for which effects it removes."),
    m("healthstone", "Healthstone", "Survival", ["PvP", "PvE"],
      "Stops your cast and eats a Healthstone.", [["Click", "Use Healthstone"]],
      "#showtooltip\n/stopcasting\n/use Healthstone",
      "verify", "Forever merges Healthstone ranks into one Create Healthstone spell. Confirm the item in your bags is named just 'Healthstone'."),
    m("soulstone", "Soulstone your focus", "Survival", ["PvE", "PvP"],
      "Soulstone your focused healer without targeting them. Click uses it on your friendly target, otherwise you.",
      [["Click", "Friendly target, else you"], ["Shift", "Focus"]],
      "#showtooltip\n/use [@focus,mod:shift,help,nodead][help,nodead][@player] Soulstone",
      "verify", "Confirm the item is named just 'Soulstone' in Forever (ranks are merged)."),
    m("tap-ward", "Life Tap / Shadow Ward", "Survival", ["PvP", "PvE"],
      "Life Tap scales with Spirit in Forever. Shift casts Shadow Ward against shadow damage instead.",
      [["Click", "Life Tap"], ["Shift", "Shadow Ward"]], "#showtooltip\n/cast [mod:shift] Shadow Ward; Life Tap"),
] + racials(["Orc", "Undead", "Troll"], ["Shadow Bolt", "Incinerate", "Searing Pain"])

SPELLS = {
    "Seduction", "Spell Lock", "Sacrifice", "Phase Shift", "Devour Magic", "Fire Shield", "Suffering",
    "Soothing Kiss", "Torment", "Curse of Tongues", "Curse of Exhaustion", "Amplify Curse",
    "Curse of Weakness", "Curse of Recklessness", "Curse of the Elements", "Bane of Agony", "Bane of Doom",
    "Bane of Havoc", "Fear", "Death Coil", "Howl of Terror", "Banish", "Drain Mana", "Shadow Bolt",
    "Incinerate", "Immolate", "Conflagrate", "Shadowburn", "Searing Pain", "Soul Fire", "Corruption",
    "Siphon Life", "Demonic Sacrifice", "Fel Domination", "Summon Imp", "Summon Voidwalker",
    "Summon Succubus", "Summon Incubus", "Summon Felhunter", "Shadow Ward", "Life Tap",
}
UNSURE = {"Healthstone", "Soulstone", "Summon Incubus", "Fel Domination"}
