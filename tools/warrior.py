"""Warrior macros for WoW: Forever (Horde races: Orc, Undead, Tauren, Troll).

Stances: 1 = Battle, 2 = Defensive, 3 = Berserker.
"""
from common import HARM, M_HARM, m, racials, trinket

FOCUS_HARM = "@focus,mod:shift,harm"
STANCE_NOTE = "If you're in the wrong stance, the first press switches stance and the second press uses the ability. Tactical Mastery is baseline in Forever, so you keep some rage when you switch."

MACROS = [
    # Gap closers & interrupts
    m("charge", "Charge / Intercept", "Gap closers & interrupts", ["PvP", "PvE"],
      "Charge in Battle Stance, Intercept in Berserker Stance, and switch to Battle Stance from Defensive. Shift charges your focus.",
      [["Battle", "Charge"], ["Berserker", "Intercept"], ["Defensive", "Battle Stance"], ["Shift", "At focus"]],
      f"#showtooltip\n/startattack\n/cast [stance:1,{FOCUS_HARM}][stance:1] Charge; [stance:3,{FOCUS_HARM}][stance:3] Intercept; Battle Stance",
      note=STANCE_NOTE + " With the Vanguard talent you can Charge from Defensive Stance too."),
    m("interrupt", "Pummel / Shield Bash", "Gap closers & interrupts", ["PvP", "PvE"],
      "One interrupt key: Pummel in Berserker Stance, Shield Bash when you have a shield on. Otherwise it switches to Berserker Stance. Shift interrupts your focus.",
      [["Berserker", "Pummel"], ["Shield", "Shield Bash"], ["Otherwise", "Berserker Stance"], ["Shift", "At focus"]],
      f"#showtooltip\n/cast [stance:3,{FOCUS_HARM}][stance:3] Pummel; [equipped:Shields,{FOCUS_HARM}][equipped:Shields] Shield Bash; Berserker Stance",
      note=STANCE_NOTE),
    m("hamstring", "Hamstring", "Gap closers & interrupts", ["PvP"],
      "Snare to keep casters and runners in melee range.", [["Click", "Your target"]],
      "#showtooltip\n/startattack\n/cast Hamstring"),
    m("intimidating", "Intimidating Shout", "Gap closers & interrupts", ["PvP"],
      "Fears your target and nearby enemies. Peel for a healer, or cast-break.", [["Click", "Fear"]],
      "#showtooltip\n/cast Intimidating Shout"),

    # Attacks
    m("hs-bloodthirst", "Bloodthirst + Heroic Strike", "Attacks", ["PvE", "PvP", "Talent"],
      "Queues Heroic Strike on your next swing (off the global cooldown) and casts Bloodthirst. Ctrl queues Cleave instead for packs.",
      [["Click", "Heroic Strike + Bloodthirst"], ["Ctrl", "Cleave + Bloodthirst"]],
      "#showtooltip Bloodthirst\n/startattack\n/cast [mod:ctrl] Cleave; Heroic Strike\n/cast Bloodthirst",
      note="In Forever Bloodthirst no longer heals; it gives 10% movement speed instead.", name="BT Heroic"),
    m("hs-mortal", "Mortal Strike + Heroic Strike", "Attacks", ["PvP", "PvE", "Talent"],
      "Arms version: queues Heroic Strike and casts Mortal Strike. Ctrl queues Cleave.",
      [["Click", "Heroic Strike + Mortal Strike"], ["Ctrl", "Cleave + Mortal Strike"]],
      "#showtooltip Mortal Strike\n/startattack\n/cast [mod:ctrl] Cleave; Heroic Strike\n/cast Mortal Strike",
      "verify", "Mortal Strike wasn't in the Forever ability list the research found. Check your Arms talents.", name="MS Heroic"),
    m("overpower", "Overpower (stance dance)", "Attacks", ["PvP", "PvE"],
      "Overpower after a dodge. Switches to Battle Stance first if needed.",
      [["Battle", "Overpower"], ["Otherwise", "Battle Stance"]],
      "#showtooltip Overpower\n/startattack\n/cast [stance:1] Overpower; Battle Stance", note=STANCE_NOTE),
    m("whirlwind", "Whirlwind (stance dance)", "Attacks", ["PvE", "PvP"],
      "Whirlwind in Berserker Stance; switches there first if needed. In Forever it hits with both weapons.",
      [["Berserker", "Whirlwind"], ["Otherwise", "Berserker Stance"]],
      "#showtooltip Whirlwind\n/startattack\n/cast [stance:3] Whirlwind; Berserker Stance", note=STANCE_NOTE),
    m("execute", "Execute / Victory Rush", "Attacks", ["PvP", "PvE"],
      "Execute below 20% health. Ctrl uses Victory Rush (back in Forever at level 20) after a kill for a 10% heal.",
      [["Click", "Execute"], ["Ctrl", "Victory Rush"]],
      "#showtooltip\n/startattack\n/cast [mod:ctrl] Victory Rush; Execute"),
    m("rend-sunder", "Rend / Sunder Armor / Thunder Clap", "Attacks", ["PvE", "PvP"],
      "Debuffs on one key. Rend scales with attack power in Forever, and Thunder Clap now works in Defensive Stance.",
      [["Click", "Sunder Armor"], ["Shift", "Thunder Clap"], ["Ctrl", "Rend"]],
      "#showtooltip\n/startattack\n/cast [mod:shift] Thunder Clap; [mod:ctrl] Rend; Sunder Armor"),

    # Tanking
    m("taunt", "Taunt (stance dance)", "Tanking", ["PvE"],
      "Taunts in Defensive Stance; switches there first if needed. Shift taunts the mob on your focus.",
      [["Defensive", "Taunt"], ["Otherwise", "Defensive Stance"], ["Shift", "At focus"]],
      f"#showtooltip Taunt\n/cast [stance:2,{FOCUS_HARM}][stance:2] Taunt; Defensive Stance", note=STANCE_NOTE),
    m("revenge", "Revenge / Shield Slam + Heroic Strike", "Tanking", ["PvE"],
      "Tank threat: queues Heroic Strike and casts Revenge. Ctrl casts Shield Slam (talent) instead.",
      [["Click", "Heroic Strike + Revenge"], ["Ctrl", "Heroic Strike + Shield Slam"]],
      "#showtooltip\n/startattack\n/cast Heroic Strike\n/cast [mod:ctrl] Shield Slam; Revenge", name="Revenge"),
    m("shield", "Shield Block / Shield Wall", "Tanking", ["PvE", "PvP"],
      "Shield Block for steady damage, Shield Wall for emergencies. Shield Wall no longer shares a cooldown with Recklessness or Retaliation.",
      [["Click", "Shield Block"], ["Shift", "Shield Wall"]],
      "#showtooltip\n/cast [mod:shift] Shield Wall; Shield Block"),
    m("disarm", "Disarm (stance dance)", "Tanking", ["PvP", "PvE"],
      "Disarms in Defensive Stance; switches there first if needed. Shift disarms your focus.",
      [["Defensive", "Disarm"], ["Otherwise", "Defensive Stance"], ["Shift", "At focus"]],
      f"#showtooltip Disarm\n/cast [stance:2,{FOCUS_HARM}][stance:2] Disarm; Defensive Stance", note=STANCE_NOTE),
    m("challenging", "Challenging Shout", "Tanking", ["PvE"],
      "Area taunt for when a pack gets loose.", [["Click", "Challenging Shout"]], "#showtooltip\n/cast Challenging Shout"),

    # Cooldowns & shouts
    m("berserker-rage", "Berserker Rage (stance dance)", "Cooldowns & shouts", ["PvP", "PvE"],
      "Breaks and prevents fear. Switches to Berserker Stance first if needed.",
      [["Berserker", "Berserker Rage"], ["Otherwise", "Berserker Stance"]],
      "#showtooltip Berserker Rage\n/cast [stance:3] Berserker Rage; Berserker Stance", note=STANCE_NOTE, name="Berserker Rage"),
    m("bloodrage", "Bloodrage", "Cooldowns & shouts", ["PvP", "PvE"],
      "Rage for health, to open with a Charge or a shout.", [["Click", "Bloodrage"]], "#showtooltip\n/cast Bloodrage"),
    m("big-cds", "Retaliation / Recklessness / Death Wish", "Cooldowns & shouts", ["PvP", "PvE"],
      "Big cooldowns on one key. In Forever they no longer share a cooldown.",
      [["Click", "Retaliation"], ["Shift", "Recklessness"], ["Ctrl", "Death Wish"]],
      "#showtooltip\n/cast [mod:shift] Recklessness; [mod:ctrl] Death Wish; Retaliation",
      "verify", "Recklessness wasn't in the Forever ability list the research found. Death Wish is a Fury talent.", name="Big Cooldowns"),
    m("shouts", "Battle Shout / Demoralizing Shout", "Cooldowns & shouts", ["PvE", "PvP"],
      "Shouts on one key.", [["Click", "Battle Shout"], ["Shift", "Demoralizing Shout"]],
      "#showtooltip\n/cast [mod:shift] Demoralizing Shout; Battle Shout"),
    trinket("Cooldowns & shouts"),
] + racials(["Orc", "Undead", "Tauren", "Troll"], ["Bloodthirst", "Execute"], melee=True)

SPELLS = {
    "Battle Stance", "Defensive Stance", "Berserker Stance", "Charge", "Intercept", "Pummel", "Shield Bash",
    "Hamstring", "Intimidating Shout", "Heroic Strike", "Cleave", "Bloodthirst", "Overpower", "Whirlwind",
    "Execute", "Victory Rush", "Thunder Clap", "Rend", "Sunder Armor", "Taunt", "Revenge", "Shield Slam",
    "Shield Block", "Shield Wall", "Disarm", "Challenging Shout", "Berserker Rage", "Bloodrage", "Retaliation",
    "Death Wish", "Battle Shout", "Demoralizing Shout", "Mortal Strike", "Recklessness",
}
UNSURE = {"Mortal Strike", "Recklessness"}
