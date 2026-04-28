# Statblock Quick Reference Guide

*A beginner-friendly guide to reading NPC and monster statblocks in tabletop RPGs. Every section is explained with examples drawn from the goblin, kobold, and gnoll character sheets in this collection.*

---

## Table of Contents

1. [Creature Type, Size & Alignment](#creature-type-size--alignment)
2. [Armor Class (AC)](#armor-class-ac)
3. [Hit Points (HP)](#hit-points-hp)
4. [Speed](#speed)
5. [Ability Scores](#ability-scores)
   - [Strength (STR)](#strength-str)
   - [Dexterity (DEX)](#dexterity-dex)
   - [Constitution (CON)](#constitution-con)
   - [Intelligence (INT)](#intelligence-int)
   - [Wisdom (WIS)](#wisdom-wis)
   - [Charisma (CHA)](#charisma-cha)
6. [Ability Modifiers](#ability-modifiers)
7. [Saving Throws](#saving-throws)
8. [Skills](#skills)
9. [Proficiency Bonus](#proficiency-bonus)
10. [Damage Resistances & Immunities](#damage-resistances--immunities)
11. [Condition Immunities](#condition-immunities)
12. [Senses](#senses)
13. [Languages](#languages)
14. [Challenge Rating (CR) & XP](#challenge-rating-cr--xp)
15. [Traits](#traits)
16. [Actions](#actions)
    - [Attack Rolls](#attack-rolls)
    - [Damage Rolls](#damage-rolls)
    - [Saving Throw DCs (Difficulty Class)](#saving-throw-dcs-difficulty-class)
    - [Multiattack](#multiattack)
    - [Recharge Abilities](#recharge-abilities)
17. [Bonus Actions](#bonus-actions)
18. [Reactions](#reactions)
19. [Legendary Actions](#legendary-actions)
20. [Legendary Resistance](#legendary-resistance)
21. [Lair Actions](#lair-actions)
22. [Spellcasting](#spellcasting)
23. [Putting It All Together: Reading a Full Statblock](#putting-it-all-together-reading-a-full-statblock)
24. [Common Conditions Reference](#common-conditions-reference)
25. [Damage Types Reference](#damage-types-reference)

---

## Creature Type, Size & Alignment

The very first line of a statblock tells you three things about the creature.

**Example:** *Small humanoid (kobold), lawful evil*

- **Size** determines how much space the creature takes up on a battle map and which weapons/grapple rules apply. Sizes from smallest to largest: Tiny, Small, Medium, Large, Huge, Gargantuan. Most player characters are Medium. All the goblins and kobolds in this collection are Small. The Gnoll Butcher of Yeenoghu is Large — meaning it takes up a 10×10-foot space on the map.
- **Creature Type** tells you what category the creature belongs to (humanoid, fiend, undead, beast, etc.). This matters because some spells and abilities only affect certain types. For example, *hold person* only works on humanoids — so it works on a Gnoll Packmaster (humanoid) but not on the Gnoll Butcher of Yeenoghu (fiend).
- **Alignment** is a two-axis shorthand for the creature's moral compass:
  - **Law vs. Chaos:** Lawful creatures follow rules and hierarchy. Chaotic creatures act on impulse and reject authority.
  - **Good vs. Evil:** Good creatures protect others. Evil creatures are selfish, cruel, or destructive.
  - Kobolds are typically **lawful evil** (organized and hierarchical, but selfish). Gnolls are typically **chaotic evil** (destructive and unpredictable).

> **When you use it:** Alignment guides how you roleplay the NPC. A lawful evil Kobold Trapmaster might honor a deal if it benefits the warren. A chaotic evil Gnoll Scavenger will betray you the moment it gets hungry.

---

## Armor Class (AC)

**What it is:** Armor Class is how hard the creature is to hit with an attack. It's the number an attacker must meet or beat on their attack roll to land a hit.

**Example:** The Goblin Skirmisher has AC 13 (leather armor). The Kobold Wyrmspeaker Sovereign has AC 19 (enchanted dragon-scale plate, ring of warding).

- A low AC (10–12) means the creature is easy to hit — it's unarmored or lightly protected.
- A moderate AC (13–16) means basic to good armor and/or decent Dexterity.
- A high AC (17–20) means heavy armor, magical protection, or very high Dexterity.

The parenthetical note tells you *why* the AC is that number — what armor or natural protection creates it.

> **When you use it:** Every time someone attacks this creature. The attacker rolls a d20, adds their attack bonus, and compares the total to the target's AC. If the total equals or exceeds the AC, the attack hits.

---

## Hit Points (HP)

**What it is:** Hit Points represent how much damage a creature can take before it drops to 0 HP and is defeated (killed or knocked unconscious).

**Example:** The Kobold Tunneler has 7 HP (3d6 − 3). The Gnoll Butcher of Yeenoghu has 184 HP (16d10 + 96).

- The first number (7, 184) is the **average** — use this for simplicity.
- The dice formula in parentheses (3d6 − 3) is for rolling if you want randomized HP. It breaks down as:
  - **3d6** = roll three six-sided dice (the number of dice is based on the creature's Hit Dice, and the die size is based on its Size category: d6 for Small, d8 for Medium, d10 for Large)
  - **− 3** = the Constitution modifier × number of Hit Dice. The Tunneler has −1 CON modifier × 3 Hit Dice = −3.

> **When you use it:** Track HP during combat. When a creature takes damage, subtract it from their current HP. At 0 HP, the creature is dead (for monsters/NPCs) or dying (for player characters).

> **DM Tip:** Low-CR creatures with low HP (like the 7 HP Kobold Tunneler) will often die in a single hit. This is intentional — they're meant to appear in large groups.

---

## Speed

**What it is:** How far the creature can move on its turn, measured in feet. One square on a battle map = 5 feet.

**Example:** The Gnoll Butcher of Yeenoghu has a speed of 40 ft. The Kobold Wyrmspeaker Sovereign has 30 ft. speed and 40 ft. fly speed.

Common speed types:
- **Walking speed** (listed as just a number, e.g., "30 ft.") — standard ground movement
- **Burrow speed** — the creature can dig through earth or loose stone (e.g., the Kobold Tunneler has burrow 10 ft.)
- **Climb speed** — the creature can climb without needing to make ability checks (e.g., the Goblin Hexblade Stalker has climb 20 ft.)
- **Fly speed** — the creature can fly. Some fly speeds note limitations like "fragile wings"
- **Swim speed** — the creature can swim without penalty

> **When you use it:** On each of the creature's turns, it can move up to its speed. It can break up movement before and after actions. A creature with 30 ft. speed can move 6 squares on a grid.

---

## Ability Scores

Every creature has six core abilities, rated on a scale. A score of 10–11 is average for a human. The scores power almost everything the creature does.

### Strength (STR)

**What it measures:** Raw physical power — how hard you hit, how much you can carry, how well you can grapple or shove.

**Example:** The Gnoll Butcher of Yeenoghu has STR 22 (+6) — supernaturally strong. The Kobold Tunneler has STR 7 (−2) — physically weak.

> **When you use it:**
> - **Melee weapon attacks** (swords, axes, flails) usually add the STR modifier to attack and damage rolls
> - **Athletics checks** — climbing, swimming, jumping, grappling, shoving
> - **Strength saving throws** — resisting being pushed, grappled, or physically restrained (e.g., the Trapmaster's Glue Bomb requires a STR save to escape)
> - **Carry capacity and encumbrance**

---

### Dexterity (DEX)

**What it measures:** Agility, reflexes, and hand-eye coordination — how nimble the creature is.

**Example:** The Goblin Hexblade Stalker has DEX 18 (+4) — extremely agile. The Gnoll Scavenger has DEX 12 (+1) — slightly above average.

> **When you use it:**
> - **Ranged weapon attacks** (bows, slings, thrown weapons) usually add the DEX modifier
> - **Finesse melee weapons** (daggers, rapiers, shortswords) can use DEX instead of STR
> - **Armor Class** — if wearing light armor or no armor, DEX modifier is added to AC
> - **Initiative** — DEX modifier determines turn order at the start of combat
> - **Dexterity saving throws** — dodging fireballs, traps, breath weapons, area effects (e.g., the Dragon Herald's Breath Siphon requires a DEX save)
> - **Stealth, Acrobatics, and Sleight of Hand checks**

---

### Constitution (CON)

**What it measures:** Endurance, stamina, and physical resilience — how tough the creature is.

**Example:** The Gnoll Butcher of Yeenoghu has CON 22 (+6) — nearly unkillable stamina. The Kobold Tunneler has CON 9 (−1) — fragile.

> **When you use it:**
> - **Hit Points** — CON modifier × number of Hit Dice is added to (or subtracted from) total HP. This is why high-CON creatures have huge HP pools.
> - **Constitution saving throws** — resisting poison, disease, exhaustion, and concentration-breaking effects (e.g., the Packmaster's diseased Bite requires a CON save)
> - **Concentration checks** — if a spellcaster takes damage while concentrating on a spell, they make a CON save to maintain it
> - **You never make CON-based skill checks** — CON is purely a passive resilience stat

---

### Intelligence (INT)

**What it measures:** Reasoning, memory, logic, and learning — book smarts and analytical thinking.

**Example:** The Kobold Wyrmspeaker Sovereign has INT 20 (+5) — genius-level intellect. The Gnoll Scavenger has INT 6 (−2) — barely sapient.

> **When you use it:**
> - **Arcana, History, Investigation, Nature, and Religion checks** — recalling lore, analyzing clues, understanding magical phenomena
> - **Intelligence saving throws** — resisting certain psychic attacks and illusions
> - **Spellcasting** — some creatures (like the Kobold Dragon Herald) use INT as their spellcasting ability, meaning their spell save DCs and attack bonuses are based on INT
> - **Trap detection** — the Investigation skill (INT-based) is used to find hidden traps like those deployed by the Kobold Trapmaster (DC 15 Investigation to detect)

---

### Wisdom (WIS)

**What it measures:** Perception, intuition, willpower, and common sense — awareness of the world and inner resolve.

**Example:** The Goblin Warlord Ascendant has WIS 15 (+2) — perceptive and hard to fool. The Kobold Tunneler has WIS 10 (+0) — average awareness.

> **When you use it:**
> - **Perception checks** — noticing hidden enemies, spotting traps, hearing distant sounds. This is one of the most-rolled skills in the game.
> - **Passive Perception** — a creature's "always-on" awareness score (10 + Perception modifier). If a sneaking creature's Stealth roll is lower than the target's passive Perception, they're spotted automatically without a roll.
> - **Wisdom saving throws** — resisting charm, fear, mind control, and psychic domination. This is one of the most important saves in the game. (e.g., the Goblin Warlord's Tyrant's Gaze requires a WIS save to avoid being stunned)
> - **Insight, Medicine, Survival, and Animal Handling checks**

---

### Charisma (CHA)

**What it measures:** Force of personality, leadership, social influence, and inner fire — not necessarily physical attractiveness.

**Example:** The Goblin Hexblade Stalker has CHA 18 (+4) — magnetically compelling. The Kobold Tunneler has CHA 8 (−1) — meek and unimposing.

> **When you use it:**
> - **Intimidation, Deception, Persuasion, and Performance checks** — social encounters, negotiations, lying, commanding respect
> - **Charisma saving throws** — resisting banishment, certain divine effects, and some possession abilities (e.g., the Goblin Warlord's Crown's Command requires a CHA save)
> - **Spellcasting** — warlocks and some other casters (like the Goblin Hexblade Stalker) use CHA as their spellcasting ability
> - **Leadership abilities** — many leader-type NPCs key their command abilities off CHA

---

## Ability Modifiers

Every ability score has a **modifier** — this is the number you actually add to dice rolls. The modifier is shown in parentheses next to the score.

| Score | Modifier | Score | Modifier |
|:-----:|:--------:|:-----:|:--------:|
| 1 | −5 | 12–13 | +1 |
| 2–3 | −4 | 14–15 | +2 |
| 4–5 | −3 | 16–17 | +3 |
| 6–7 | −2 | 18–19 | +4 |
| 8–9 | −1 | 20–21 | +5 |
| 10–11 | +0 | 22–23 | +6 |

**Formula:** (Score − 10) ÷ 2, rounded down.

> **When you use it:** Almost every roll in the game. Attack rolls, damage rolls, saving throws, skill checks — they all add the relevant ability modifier.

---

## Saving Throws

**What they are:** When a statblock lists specific saving throws (e.g., "Saving Throws Dex +5, Cha +4"), it means the creature is *proficient* in those saves and adds its proficiency bonus on top of the ability modifier.

**Example:** The Goblin Raider Captain has "Saving Throws Dex +5, Cha +4." Its DEX modifier is +3 and proficiency bonus is +2, so its DEX save is 3 + 2 = +5.

If a saving throw **isn't listed**, the creature just uses the raw ability modifier. For the same Raider Captain, a Wisdom saving throw would just be +1 (its WIS modifier), with no proficiency added.

> **When you use it:** When a spell, trap, or ability forces the creature to make a saving throw. Roll a d20, add the relevant save bonus, and compare to the DC (Difficulty Class). Meet or beat the DC = success.

---

## Skills

**What they are:** Skills represent areas of training or natural talent. When a skill is listed (e.g., "Skills Stealth +6, Perception +2"), the creature adds that bonus when making checks with that skill.

**Example:** The Goblin Skirmisher has "Skills Stealth +6." Its DEX modifier is +2 and proficiency bonus is +2, giving +4 — but it has +6, which means it has **expertise** (double proficiency) in Stealth, making it exceptionally sneaky.

Common skills and their associated abilities:
- **STR:** Athletics
- **DEX:** Acrobatics, Sleight of Hand, Stealth
- **INT:** Arcana, History, Investigation, Nature, Religion
- **WIS:** Animal Handling, Insight, Medicine, Perception, Survival
- **CHA:** Deception, Intimidation, Performance, Persuasion

> **When you use it:** Whenever the creature attempts something that falls under a skill. The DM calls for a check, you roll d20 + the listed skill bonus. If the skill isn't listed, you just use the raw ability modifier.

---

## Proficiency Bonus

**What it is:** A flat bonus that scales with the creature's power level (tied to Challenge Rating). It's added to attack rolls, saving throws the creature is proficient in, skill checks it's trained in, and spell save DCs.

| CR | Proficiency Bonus |
|:--:|:-----------------:|
| 0–4 | +2 |
| 5–8 | +3 |
| 9–12 | +4 |
| 13–16 | +5 |
| 17–20 | +6 |
| 21–24 | +7 |
| 25–28 | +8 |
| 29–30 | +9 |

> **When you use it:** You usually don't need to reference this directly — it's already baked into the creature's listed attack bonuses, save bonuses, and skill bonuses. But it's useful for understanding *why* numbers are what they are, and for improvising if you need to add a new skill or save to a creature on the fly.

---

## Damage Resistances & Immunities

**What they are:** Some creatures take reduced or zero damage from certain damage types.

- **Resistance** = take **half damage** from that type (rounded down)
- **Immunity** = take **zero damage** from that type

**Example:** The Gnoll Fang of Ruin has "Damage Resistances fire, poison" — it takes half damage from fire and poison attacks. The Gnoll Butcher of Yeenoghu has "Damage Immunities fire, poison" — fire and poison do nothing to it at all.

A common resistance is "bludgeoning, piercing, and slashing from nonmagical attacks" — meaning ordinary weapons (swords, arrows, clubs) deal half damage, but magical weapons deal full damage.

> **When you use it:** After calculating damage, check if the target has resistance or immunity to that damage type. If resistant, halve the damage. If immune, it takes 0. This is why the Gnoll Butcher's stat sheet notes that its attacks are magical — so its own attacks bypass other creatures' nonmagical resistance.

---

## Condition Immunities

**What they are:** Conditions are status effects (frightened, charmed, poisoned, stunned, etc.). If a creature is immune to a condition, that effect simply doesn't work on it.

**Example:** The Goblin Warlord Ascendant has "Condition Immunities charmed, frightened" — no spell or ability can charm or frighten it.

> **When you use it:** Before applying a condition effect to a creature, check its immunities. If it's immune, the effect automatically fails — no saving throw needed. This is particularly important for spellcasters choosing which spells to use.

---

## Senses

**What they are:** Special sensory capabilities beyond normal sight.

- **Darkvision (X ft.)** — can see in darkness as if it were dim light, and in dim light as if it were bright light, out to the listed range. Colors appear as shades of gray. Most goblins, kobolds, and gnolls have darkvision 60 ft., which is why they love fighting underground or at night.
- **Blindsight (X ft.)** — can perceive surroundings without relying on sight at all (echolocation, tremorsense, etc.). Not fooled by invisibility or darkness.
- **Truesight (X ft.)** — sees through illusions, invisibility, magical darkness, and shapechanging. Also sees into the Ethereal Plane. Extremely powerful and rare. The Goblin Warlord Ascendant has truesight 30 ft.
- **Passive Perception (X)** — the creature's baseline awareness (10 + Perception modifier + any bonuses). Used to determine whether hidden creatures or traps are automatically noticed.

> **When you use it:**
> - **Darkvision:** Determines whether the creature can fight effectively in darkness. A creature without darkvision attacking in total darkness has disadvantage on attacks and can't see targets.
> - **Passive Perception:** Compare this to a sneaking creature's Stealth roll. If the Stealth roll is lower, the creature is spotted without any active check needed.
> - **Blindsight/Truesight:** These counter specific tactics. An invisible attacker gains no advantage against a creature with blindsight or truesight.

---

## Languages

**What they are:** Which languages the creature can speak and understand.

**Example:** The Kobold Dragon Herald speaks "Common, Draconic, Infernal, Sylvan" — it can communicate with a wide range of creatures. The Gnoll Scavenger only speaks "Gnoll" — good luck negotiating.

> **When you use it:** Determines whether NPCs and players can communicate. If no one in the party speaks Gnoll, they can't negotiate with Gnoll Scavengers. Some entries say "understands X but can't speak" — the creature comprehends commands but can't hold a conversation.

---

## Challenge Rating (CR) & XP

**What it is:** Challenge Rating is a rough estimate of how dangerous the creature is relative to a group of four adventurers.

- **CR 1/4** (50 XP) — a minor threat. Four of these are a fair fight for a level 1 party.
- **CR 3** (700 XP) — a moderate threat. Fair fight for a level 3 party.
- **CR 7** (2,900 XP) — a serious threat. Fair fight for a level 7 party.
- **CR 12** (8,400 XP) — a deadly boss. Fair fight for a level 12 party.

**XP (Experience Points)** is the reward for defeating the creature, used to track character advancement.

> **When you use it:**
> - **Encounter building:** Compare the party's level to the CR to gauge difficulty. A CR 7 creature is a fair solo fight for four level-7 characters, but deadly for four level-3 characters.
> - **XP tracking:** Award the listed XP when the creature is defeated (killed, captured, or driven off).
> - **General power gauge:** Higher CR = better stats, more HP, nastier abilities across the board.

> **Important:** CR is a guideline, not a guarantee. A CR 3 Kobold Trapmaster in a trapped lair will punch far above its weight. A CR 7 Fang of Ruin caught in the open without minions is easier than the number suggests. Terrain, preparation, and allies all shift effective difficulty.

---

## Traits

**What they are:** Passive abilities that are always active or trigger automatically under certain conditions. Traits appear in the statblock before the Actions section.

**Examples from this collection:**
- **Nimble Escape** (Goblins) — can Disengage or Hide as a bonus action every turn. This is what makes goblins so slippery.
- **Pack Tactics** (Kobolds) — advantage on attacks when an ally is adjacent to the target. This is why kobolds fight in swarms.
- **Rampage** (Gnolls) — free bonus movement + bite attack after downing a creature. This creates chain reactions in combat.
- **Sunlight Sensitivity** (Kobolds) — disadvantage on attacks and Perception in sunlight. This is a deliberate weakness that shapes how and where you encounter them.

> **When you use it:** Traits are always relevant — read them before combat starts so you know the creature's built-in advantages and weaknesses. Many traits fundamentally change how the creature fights.

---

## Actions

Actions are things the creature can do **on its turn**. Each creature gets one action per turn (unless they have Multiattack or special rules).

### Attack Rolls

**What they are:** When a creature makes an attack, it rolls a d20 and adds its attack bonus.

**Format:** *Melee Weapon Attack:* +5 to hit, reach 5 ft., one target.

- **+5 to hit** = roll d20 + 5. Compare to the target's AC. Equal or higher = hit.
- **Reach 5 ft.** = the attack reaches targets within 5 feet (adjacent on a grid). Some weapons have 10 ft. reach (like the Fang of Ruin's Ruinous Glaive).
- **Melee vs. Ranged:** Melee = close combat. Ranged = from a distance. Ranged attacks list two numbers (e.g., "range 80/320 ft.") — the first is normal range, the second is maximum range (attacks at long range have disadvantage).

**Attack bonus formula:** Ability modifier + proficiency bonus. For melee, usually STR. For ranged, usually DEX. Some creatures use other abilities (the Dragon Herald uses INT for spell attacks).

### Damage Rolls

**What they are:** When an attack hits, you roll damage dice.

**Format:** *Hit:* 10 (1d10 + 5) slashing damage plus 7 (2d6) necrotic damage.

- **10** = the average damage (use this for quick play)
- **(1d10 + 5)** = the roll formula: one ten-sided die + 5
- **Slashing/necrotic** = the damage type (relevant for resistances and immunities)
- **"Plus"** = additional damage on top — add both values together for total damage

**Damage bonus formula:** Usually the same ability modifier used for the attack roll (STR for melee, DEX for ranged). Damage dice (1d10, 2d6, etc.) depend on the weapon or ability.

### Saving Throw DCs (Difficulty Class)

**What they are:** Some abilities don't use attack rolls — instead, the *target* makes a saving throw against a DC.

**Format:** "must succeed on a DC 15 Dexterity saving throw or take 28 (8d6) fire damage"

- **DC 15** = the number the target must meet or beat on their saving throw roll
- **Dexterity** = the ability used for the save (d20 + DEX save bonus)
- The text after "or" describes what happens on a failure
- Many abilities also specify what happens on a success (often half damage)

**DC formula:** 8 + proficiency bonus + ability modifier of the creature forcing the save.

> **Example:** The Kobold Dragon Herald has DC 15 on its Breath Siphon. Its proficiency is +3 and its INT modifier is +4. So: 8 + 3 + 4 = 15.

### Multiattack

**What it is:** A special action that lets the creature make multiple attacks in a single action. Without Multiattack, a creature can only make one attack per action.

**Example:** "The Fang of Ruin makes three attacks: two with its Ruinous Glaive and one with its Bite."

> **When you use it:** On the creature's turn, instead of choosing one attack, it makes all the attacks listed in Multiattack. This is why higher-CR creatures deal so much more damage per turn.

### Recharge Abilities

**What they are:** Powerful abilities that can't be used every turn. The parenthetical tells you how they recharge.

- **Recharge 5–6:** At the start of each turn, roll a d6. On a 5 or 6, the ability recharges and can be used again.
- **Recharge 6:** Only recharges on a roll of 6 (less likely).
- **Recharges after a Short or Long Rest:** Can only be used once per rest period.
- **X/Day:** Can be used a fixed number of times per day.

**Example:** The Gnoll Butcher's "Jaws of the Abyss (Recharge 5–6)" — after using it, the DM rolls a d6 at the start of each of the Butcher's turns. On a 5 or 6, it can use Jaws of the Abyss again.

> **When you use it:** Track whether rechargeable abilities are available. Roll to recharge at the start of each turn. This adds uncertainty and tension — players never know when a devastating ability will come back online.

---

## Bonus Actions

**What they are:** Quick additional things a creature can do on its turn, *in addition to* its regular action and movement. A creature can only take a bonus action if it has a specific ability that grants one.

**Example:** The Goblin Warlord Ascendant has "Deploy the Warband" as a bonus action — it can command up to three allied goblinoids to attack or move, all while still taking its own Multiattack action on the same turn.

> **When you use it:** After (or before) the creature takes its main action, check if it has a bonus action available. Bonus actions are powerful because they don't cost the creature its main action. Nimble Escape (Goblins) is a bonus action — meaning a goblin can attack AND disengage on the same turn.

---

## Reactions

**What they are:** Actions that trigger in response to a specific event, typically on someone else's turn. Each creature gets **one reaction per round** (it recharges at the start of the creature's turn).

**Example:** The Goblin Raider Captain has "Redirect Attack" — when targeted by an attack, it can swap places with an adjacent ally, making the ally take the hit instead. The Gnoll Fang of Ruin has "Savage Retaliation" — when damaged by a nearby creature, it can bite back immediately.

> **When you use it:** Watch for the triggering condition during combat. When it happens, you can choose to use the reaction. Remember: only one reaction per round, so choose wisely. Opportunity attacks (attacking a creature that moves away from you without Disengaging) also cost your reaction.

---

## Legendary Actions

**What they are:** Extra actions that powerful creatures (typically CR 10+) can take *at the end of other creatures' turns*. This makes boss monsters feel like bosses — they act multiple times per round instead of just once.

**Key rules:**
- The creature gets a set number of legendary actions per round (usually 3)
- It can only use **one** legendary action at the end of another creature's turn
- Spent legendary actions recharge at the start of the creature's own turn
- Some options cost more than 1 legendary action (e.g., "Costs 2 Actions")

**Example:** The Goblin Warlord Ascendant has these options:
- **Move** (1 action) — repositions without provoking opportunity attacks
- **Strike** (2 actions) — makes a weapon attack
- **Tyrant's Gaze** (2 actions) — stuns a target
- **Rally the Horde** (3 actions) — stabilizes dying allies

> **When you use it:** After each non-legendary creature finishes its turn, decide whether the boss uses a legendary action and which one. This keeps the boss active throughout the entire round, not just on its own turn. It also means the party can't simply "wait out" the boss's turn.

---

## Legendary Resistance

**What it is:** An ability that lets a powerful creature automatically succeed on a saving throw it would otherwise fail. It has a limited number of uses per day (typically 3).

**Example:** "Legendary Resistance (3/Day): If the Warlord fails a saving throw, it can choose to succeed instead."

> **When you use it:** When the creature fails a saving throw against a spell or ability, you can burn one use of Legendary Resistance to succeed instead. This prevents a single *hold person* or *banishment* spell from ending the boss fight in one round.

> **Tactical note:** Track uses carefully. Smart players will try to "burn" Legendary Resistances with lower-value spells before hitting the boss with their best shot. The DM must decide whether each failed save is worth spending a charge on.

---

## Lair Actions

**What they are:** Environmental effects that trigger on initiative count 20 when the creature is fought inside its home territory (its "lair"). These represent the creature's control over its environment.

**Key rules:**
- Happen on initiative count 20 (losing ties)
- The creature can choose one effect from a list
- Can't repeat the same effect two rounds in a row
- Only apply when fighting in the lair — the same creature fought elsewhere doesn't get lair actions

**Example:** The Kobold Wyrmspeaker Sovereign in its Dragon's Sanctum can cause tremors, reveal hidden enemies, summon reinforcements, or activate breath weapon vents — every single round, in addition to its normal turn.

> **When you use it:** Before the fight, decide whether the encounter takes place in the creature's lair. If so, add initiative count 20 to your initiative tracker. On that count each round, choose a lair action. Lair actions are what turn a hard fight into a deadly one — the environment itself becomes an enemy.

---

## Spellcasting

**What it is:** Some creatures can cast spells, just like player-character spellcasters. The statblock tells you everything you need:

- **Caster level** — determines spell slots and maximum spell level
- **Spellcasting ability** — the ability score used (INT, WIS, or CHA)
- **Spell save DC** — the DC targets must beat when the creature casts a spell requiring a save
- **Spell attack bonus** — added to d20 when the creature casts a spell requiring an attack roll
- **Spell list** — organized by level, with the number of available slots

**Example:** The Kobold Dragon Herald is a 7th-level spellcaster using Intelligence (DC 15, +7 to hit). It has cantrips (unlimited use) and leveled spells (limited by spell slots — once a slot is spent, it's gone until a rest).

> **When you use it:** On the creature's turn, it can cast a spell instead of (or sometimes in addition to) making attacks. Track spell slots — once spent, they don't come back until the creature rests.

> **For beginners:** If spellcasting feels overwhelming, just read what each spell does right before you need it. You don't need to memorize all the spells — look them up as they come up.

---

## Putting It All Together: Reading a Full Statblock

Here's how to read a statblock from top to bottom, using the **Gnoll Packmaster (CR 3)** as an example:

1. **Header:** Medium humanoid, chaotic evil — it's person-sized, savage, and unreasonable
2. **AC 14, HP 52, Speed 30 ft.** — moderately tough, average mobility
3. **Ability scores:** Strong (STR 16), decent DEX and CON, low INT, average WIS and CHA — a physical brute
4. **Skills:** Perception +3, Survival +3 — decent tracker and scout
5. **Senses:** Darkvision 60 ft. — fights well in the dark
6. **CR 3 (700 XP)** — appropriate challenge for a level 3 party
7. **Traits:** Rampage (chain kills), Alpha of the Pack (buffs allies), Blood Frenzy (advantage vs. wounded) — gets more dangerous as the fight goes on
8. **Actions:** Multiattack (Flail + Bite), Diseased Bite, War Howl (ally buff) — hits hard and empowers allies
9. **Reactions:** Punish the Weak — retaliates when an ally dies

**The story this tells:** The Packmaster is a mid-tier gnoll leader that makes every gnoll around it more dangerous. It charges wounded enemies, its allies hit harder in its presence, and killing its packmates provokes an immediate counterattack. The party should prioritize killing the Packmaster first to remove the aura, but doing so means weathering its Blood Frenzy damage.

---

## Common Conditions Reference

These status effects appear frequently in the statblocks:

| Condition | Effect |
|-----------|--------|
| **Blinded** | Can't see. Auto-fails sight-based checks. Attack rolls against it have advantage; its attacks have disadvantage. |
| **Charmed** | Can't attack the charmer or target them with harmful abilities. The charmer has advantage on social checks against it. |
| **Deafened** | Can't hear. Auto-fails hearing-based checks. |
| **Frightened** | Disadvantage on ability checks and attacks while it can see the source of fear. Can't willingly move closer to the source. |
| **Grappled** | Speed becomes 0. Ends if the grappler is incapacitated or the creature is moved out of reach. |
| **Incapacitated** | Can't take actions or reactions. |
| **Invisible** | Impossible to see without special senses. Attacks against it have disadvantage; its attacks have advantage. |
| **Paralyzed** | Incapacitated, can't move or speak. Auto-fails STR and DEX saves. Attacks have advantage; hits from within 5 ft. are auto-crits. |
| **Poisoned** | Disadvantage on attack rolls and ability checks. |
| **Prone** | Can only crawl (half speed) or stand up (costs half movement). Melee attacks against it have advantage; ranged attacks have disadvantage. |
| **Restrained** | Speed becomes 0. Attacks against it have advantage; its attacks have disadvantage. Disadvantage on DEX saves. |
| **Stunned** | Incapacitated, can't move, can only speak falteringly. Auto-fails STR and DEX saves. Attacks against it have advantage. |

---

## Damage Types Reference

These are the types of damage that appear throughout the statblocks:

| Type | Description | Common Sources |
|------|-------------|----------------|
| **Bludgeoning** | Blunt force impact | Clubs, flails, falling, slams |
| **Piercing** | Puncturing or stabbing | Arrows, spears, bites, daggers |
| **Slashing** | Cutting or cleaving | Swords, axes, claws, glaives |
| **Fire** | Heat and flame | Alchemist's fire, dragon breath, fireball |
| **Cold** | Freezing and frost | Frost breath, ice spells |
| **Lightning** | Electrical energy | Lightning bolt, shock attacks |
| **Thunder** | Concussive sonic force | Warcry of the Ascendant, thunderwave |
| **Poison** | Toxins and venom | Poisoned blades, venomous bites |
| **Acid** | Corrosive substances | Acid breath, acid splash |
| **Necrotic** | Life-draining dark energy | Undead attacks, abyssal corruption, the Fang of Ruin's glaive |
| **Radiant** | Holy or divine energy | Divine smite, sacred flame — the Butcher of Yeenoghu's weakness |
| **Force** | Pure magical energy | Eldritch blast, magic missile — almost never resisted |
| **Psychic** | Mental assault | Rending Howl, psychic scream, mind attacks |

---

## Final Tips for New DMs

1. **You don't need to memorize everything.** Read the statblock once before the encounter, then reference it during play.
2. **Average damage speeds up play.** Use the first number (e.g., "10" from "10 [1d10 + 5]") instead of rolling every time — or roll for dramatic moments.
3. **Traits matter more than stats.** A creature's special traits are what make it unique. A Goblin Skirmisher without Nimble Escape is just a weak fighter. With it, it's a guerrilla nightmare.
4. **Don't forget reactions.** They're easy to miss but can change a fight. Keep a note next to each creature tracking whether its reaction has been used this round.
5. **Legendary actions keep bosses scary.** Without them, a boss with one turn vs. four player turns feels underwhelming. Legendary actions solve this.
6. **Read the Tactics section.** Each NPC sheet in this collection includes combat tactics — use them to run the creature intelligently without needing to improvise.
