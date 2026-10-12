"""Macro data for the WoW: Forever Undead Priest and Orc Warlock pages.

Conventions used throughout:
  click = target (mouseover first where useful), Shift = focus, Alt = self,
  Ctrl = alternate spell / add an off-GCD helper.
"""

# Target patterns
HARM = "[@focus,mod:shift,harm,nodead][@mouseover,harm,nodead][]"
HELP = "[@focus,mod:shift,help,nodead][@player,mod:alt][@mouseover,help,nodead][help,nodead][@player]"
ANY = "[@focus,mod:shift,exists,nodead][@player,mod:alt][@mouseover,exists,nodead][exists,nodead][@player]"

M_HARM = [["Click", "Mouseover, else target"], ["Shift", "Focus"]]
M_HELP = [["Click", "Mouseover, else friendly target, else you"], ["Shift", "Focus"], ["Alt", "You"]]
M_ANY = [["Click", "Mouseover, else target (friend or foe), else you"], ["Shift", "Focus"], ["Alt", "You"]]


def m(id, title, section, tags, desc, mods, text, status="ok", note=""):
    return dict(id=id, title=title, section=section, tags=tags, desc=desc,
                mods=mods, text=text.strip("\n"), status=status, note=note)


FOCUS = m(
    "set-focus", "Set focus", "Focus & utility", ["PvP", "PvE"],
    "One button to manage your focus. Bind it somewhere easy — most of the other macros read from it.",
    [["Click", "Focus your mouseover, else your target"], ["Shift", "Target your focus"], ["Alt", "Clear focus"]],
    """
/clearfocus [mod:alt]
/stopmacro [mod:alt]
/target [mod:shift] focus
/stopmacro [mod:shift]
/focus [@mouseover,exists][]
""")

ASSIST = m(
    "assist-focus", "Assist focus", "Focus & utility", ["PvP", "PvE"],
    "Target whatever your focus is targeting. Focus your tank or a teammate and pick up their kill target.",
    [["Click", "Take your focus's target"]],
    """
/assist [@focus,exists]
""")

PRIEST = [
    FOCUS, ASSIST,

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
    m("wotf", "Will of the Forsaken / PvP trinket", "PvP defensive", ["PvP"],
      "Click breaks fear, charm and sleep with Will of the Forsaken. Shift uses the PvP trinket in slot 13 for stuns and everything else. They're on separate cooldowns, so pressing one never wastes the other.",
      [["Click", "Will of the Forsaken"], ["Shift", "Trinket in slot 13"]],
      "#showtooltip\n/use [mod:shift] 13\n/cast [nomod] Will of the Forsaken",
      "verify", "Put your PvP trinket (Insignia of the Horde) in the top trinket slot (13), or change 13 to 14. Check the trinket's tooltip in Forever for what it breaks."),
    m("shadowform-heal", "Drop Shadowform + Flash Heal", "PvP defensive", ["PvP", "Talent"],
      "Leaves Shadowform and heals in the same press. Shift heals your focus instead of you.",
      [["Click", "Heal you"], ["Shift", "Heal focus"]],
      "#showtooltip Flash Heal\n/cancelaura Shadowform\n/cast [@focus,mod:shift,help,nodead][@player] Flash Heal"),
    m("fade", "Fade", "PvP defensive", ["PvE"],
      "Stops your cast and drops threat for when a heal pulls aggro.",
      [["Click", "Fade"]], "#showtooltip\n/stopcasting\n/cast Fade"),
    m("self-buffs", "Inner Fire / Touch of Weakness", "PvP defensive", ["PvP", "PvE"],
      "Undead Priest self-buffs on one key. Touch of Weakness punishes the next melee hit and weakens the attacker.",
      [["Click", "Inner Fire"], ["Shift", "Touch of Weakness"]],
      "#showtooltip\n/cast [mod:shift] Touch of Weakness; Inner Fire"),
    m("undead-sustain", "Dark Sacrifice / Cannibalize", "PvP defensive", ["PvP", "PvE"],
      "Undead mana and health recovery. Dark Sacrifice turns health into mana (10-minute cooldown). Shift cannibalizes a nearby humanoid or undead corpse.",
      [["Click", "Dark Sacrifice"], ["Shift", "Cannibalize"]],
      "#showtooltip\n/cast [mod:shift] Cannibalize; Dark Sacrifice"),

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
]

# ---------------------------------------------------------------- Warlock

def bf(spell):
    return f"#showtooltip {spell}\n/cast Blood Fury\n/cast {HARM} {spell}"


M_BF = M_HARM + [["Auto", "Blood Fury whenever it's ready"]]
BF_NOTE = ("Blood Fury is off the global cooldown, so it goes out with the spell whenever it's ready and is skipped otherwise. "
           "To hide the 'Spell is not ready yet' message, add /run UIErrorsFrame:Clear() as a last line.")

WARLOCK = [
    FOCUS, ASSIST,

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

    # Damage with Blood Fury
    m("shadow-bolt", "Shadow Bolt + Blood Fury", "Damage (auto Blood Fury)", ["PvP", "PvE"],
      "Your main nuke, with Blood Fury cast automatically on cooldown.", M_BF, bf("Shadow Bolt"), note=BF_NOTE),
    m("incinerate", "Incinerate + Blood Fury", "Damage (auto Blood Fury)", ["PvE", "PvP", "Talent"],
      "Destruction 31-point talent. Hits harder on targets with Immolate.", M_BF, bf("Incinerate"), note=BF_NOTE),
    m("immolate", "Immolate + Blood Fury", "Damage (auto Blood Fury)", ["PvP", "PvE"],
      "Fire DoT opener.", M_BF, bf("Immolate"), note=BF_NOTE),
    m("conflagrate", "Conflagrate + Blood Fury", "Damage (auto Blood Fury)", ["PvP", "PvE", "Talent"],
      "Instant burst on an Immolated target.", M_BF, bf("Conflagrate"), note=BF_NOTE),
    m("shadowburn", "Shadowburn + Blood Fury", "Damage (auto Blood Fury)", ["PvP", "Talent"],
      "Instant finisher. Can refund its Soul Shard in Forever.", M_BF, bf("Shadowburn"), note=BF_NOTE),
    m("searing-pain", "Searing Pain + Blood Fury", "Damage (auto Blood Fury)", ["PvP"],
      "Fast fire spam to finish a kiting fight.", M_BF, bf("Searing Pain"), note=BF_NOTE),
    m("soul-fire", "Soul Fire + Blood Fury", "Damage (auto Blood Fury)", ["PvE"],
      "Big opener, and the Decimation execute.", M_BF, bf("Soul Fire"), note=BF_NOTE),
    m("corruption", "Corruption", "Damage (auto Blood Fury)", ["PvP", "PvE"],
      "DoT your focus or mouseover to spread pressure.", M_HARM, f"#showtooltip\n/cast {HARM} Corruption"),
    m("siphon-life", "Siphon Life", "Damage (auto Blood Fury)", ["PvP", "PvE", "Talent"],
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
]
