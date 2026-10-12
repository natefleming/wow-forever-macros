"""Hunter macros for WoW: Forever (Horde races: Orc, Tauren, Troll)."""
from common import HARM, M_HARM, h, m, racials, trinket

TRAP_NOTE = "Traps work in combat in Forever and are placed at your feet. There's no trap launcher."

MACROS = [
    # Shots
    m("arcane-multi", "Arcane Shot / Multi-Shot", "Shots", ["PvP", "PvE"],
      "Keeps Auto Shot running and fires Arcane Shot. Ctrl fires Multi-Shot. In Forever Arcane Shot no longer shares a cooldown with Aimed Shot.",
      [["Click", "Arcane Shot"], ["Ctrl", "Multi-Shot"], ["Shift", "At focus"]],
      "#showtooltip\n/cast !Auto Shot\n/cast [mod:ctrl] Multi-Shot; [@focus,mod:shift,harm,nodead][] Arcane Shot",
      name="Arcane Multi"),
    m("aimed", "Aimed Shot", "Shots", ["PvE", "PvP"],
      "Baseline at level 20 in Forever. Shares a 6-second cooldown with Multi-Shot.",
      M_HARM, "#showtooltip\n/cast !Auto Shot\n/cast [@focus,mod:shift,harm,nodead][@mouseover,harm,nodead][] Aimed Shot"),
    m("hunters-mark", "Hunter's Mark + pet attack", "Shots", ["PvP", "PvE"],
      "Marks your target and sends the pet in. Shift marks and attacks your focus.",
      M_HARM, f"#showtooltip Hunter's Mark\n/cast {HARM} Hunter's Mark\n/petattack [@focus,mod:shift,harm,nodead][]",
      name="Mark Attack"),
    m("serpent", "Serpent Sting", "Shots", ["PvP", "PvE"],
      "DoT your focus or mouseover.", M_HARM, h("Serpent Sting")),
    m("viper", "Viper Sting", "Shots", ["PvP"],
      "Drain the enemy healer's mana from focus.", M_HARM, h("Viper Sting")),
    m("scorpid", "Scorpid Sting", "Shots", ["PvP", "PvE"],
      "In Forever it lowers the target's hit chance by 2%. Put it on the melee hitting you.", M_HARM, h("Scorpid Sting")),
    m("sniper", "Sniper Shot", "Shots", ["PvE", "PvP", "Talent"],
      "Marksmanship 31-point talent: long-range 2.5-second shot.", M_HARM, h("Sniper Shot"),
      "verify", "New in Forever. Name and cooldown taken from the beta talent tree."),
    m("rapid-fire", "Rapid Fire", "Shots", ["PvE"],
      "Ranged haste cooldown. Keeps Auto Shot running.", [["Click", "Rapid Fire"]],
      "#showtooltip Rapid Fire\n/cast !Auto Shot\n/cast Rapid Fire"),

    # Control
    m("concussive", "Concussive Shot", "Control", ["PvP", "PvE"],
      "Slow your focus or mouseover while you shoot something else.", M_HARM, h("Concussive Shot")),
    m("scatter", "Scatter Shot", "Control", ["PvP"],
      "Short disorient. Shift scatters your focus. Follow it with a Freezing Trap.", M_HARM, h("Scatter Shot")),
    m("scare-beast", "Scare Beast", "Control", ["PvP", "PvE"],
      "Fear a beast: hunter pets, or druids in cat and bear form.", M_HARM, h("Scare Beast")),
    m("traps", "Traps", "Control", ["PvP", "PvE"],
      "Stops shooting and drops a trap at your feet.",
      [["Click", "Freezing Trap"], ["Shift", "Frost Trap"], ["Ctrl", "Explosive Trap"], ["Alt", "Immolation Trap"]],
      "#showtooltip\n/stopattack\n/cast [mod:shift] Frost Trap; [mod:ctrl] Explosive Trap; [mod:alt] Immolation Trap; Freezing Trap",
      note=TRAP_NOTE),
    m("flare", "Flare", "Control", ["PvP"],
      "Reveals rogues and druids in the area.", [["Click", "Flare"]], "#showtooltip\n/cast Flare"),

    # Melee & defensive
    m("melee", "Raptor Strike / Mongoose Bite / Wing Clip", "Melee & defensive", ["PvP", "PvE"],
      "Melee on one key.", [["Click", "Raptor Strike"], ["Shift", "Wing Clip"], ["Ctrl", "Mongoose Bite"]],
      "#showtooltip\n/startattack\n/cast [mod:shift] Wing Clip; [mod:ctrl] Mongoose Bite; Raptor Strike", name="Melee"),
    m("feign", "Feign Death", "Melee & defensive", ["PvP", "PvE"],
      "Stops attacking, calls the pet back and feigns. Off the global cooldown. Damage can still break it.",
      [["Click", "Feign Death"]], "#showtooltip\n/stopattack\n/petfollow\n/cast Feign Death"),
    m("disengage", "Disengage / Deterrence", "Melee & defensive", ["PvP", "PvE"],
      "Disengage drops threat (off the global cooldown). Shift casts Deterrence.",
      [["Click", "Disengage"], ["Shift", "Deterrence"]], "#showtooltip\n/cast [mod:shift] Deterrence; Disengage"),
    m("aspects", "Aspects", "Melee & defensive", ["PvP", "PvE"],
      "Aspects on one key. The ! stops a second press from turning the aspect off.",
      [["Click", "Hawk"], ["Shift", "Cheetah"], ["Ctrl", "Monkey"], ["Alt", "Pack"]],
      "#showtooltip\n/cast [mod:shift] !Aspect of the Cheetah; [mod:ctrl] !Aspect of the Monkey; [mod:alt] !Aspect of the Pack; !Aspect of the Hawk"),
    trinket("Melee & defensive"),

    # Pet
    m("pet-attack", "Pet attack / follow / passive", "Pet", ["PvP", "PvE"],
      "Sends the pet in. Shift sends it at your focus.",
      [["Click", "Attack target"], ["Shift", "Attack focus"], ["Ctrl", "Follow"], ["Alt", "Passive"]],
      "/petfollow [mod:ctrl]\n/petpassive [mod:alt]\n/stopmacro [mod:ctrl][mod:alt]\n/petattack [@focus,mod:shift,harm,nodead][]"),
    m("pet-care", "Mend / Revive / Call Pet", "Pet", ["PvE", "PvP"],
      "One pet button: revives a dead pet, calls a missing one, otherwise heals it with Mend Pet.",
      [["Pet dead", "Revive Pet"], ["No pet", "Call Pet"], ["Otherwise", "Mend Pet"]],
      "#showtooltip\n/cast [@pet,dead] Revive Pet; [nopet] Call Pet; Mend Pet", name="Pet Care"),
    m("bm-cds", "Intimidation / Bestial Wrath", "Pet", ["PvP", "PvE", "Talent"],
      "Beast Mastery cooldowns.", [["Click", "Intimidation"], ["Shift", "Bestial Wrath"]],
      "#showtooltip\n/cast [mod:shift] Bestial Wrath; Intimidation", name="BM Cooldowns"),
    m("summon-hawk", "Summon Hawk", "Pet", ["PvE", "PvP", "Talent"],
      "Beast Mastery 16-point talent: a hawk joins the fight for about 30 seconds.", [["Click", "Summon Hawk"]],
      "#showtooltip\n/cast Summon Hawk", "verify", "New in Forever. Name taken from the beta talent tree."),
] + racials(["Orc", "Tauren", "Troll"], ["Aimed Shot", "Arcane Shot"])

SPELLS = {
    "Auto Shot", "Multi-Shot", "Arcane Shot", "Aimed Shot", "Hunter's Mark", "Serpent Sting", "Viper Sting",
    "Scorpid Sting", "Sniper Shot", "Rapid Fire", "Concussive Shot", "Scatter Shot", "Scare Beast",
    "Freezing Trap", "Frost Trap", "Explosive Trap", "Immolation Trap", "Flare", "Raptor Strike",
    "Mongoose Bite", "Wing Clip", "Feign Death", "Disengage", "Deterrence", "Aspect of the Cheetah",
    "Aspect of the Monkey", "Aspect of the Pack", "Aspect of the Hawk", "Revive Pet", "Call Pet", "Mend Pet",
    "Intimidation", "Bestial Wrath", "Summon Hawk",
}
UNSURE = {"Sniper Shot", "Summon Hawk"}
