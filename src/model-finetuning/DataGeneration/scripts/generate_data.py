import json
import random

SYSTEM_PROMPT = "You are a helpful assistant."

# All creatures data extracted from the character sheets
creatures = {
    "Gnoll Butcher of Yeenoghu": {
        "type": "Large fiend (gnoll, demon), chaotic evil",
        "ac": "18 (abyssal chitin, natural armor)",
        "hp": "184 (16d10 + 96)",
        "speed": "40 ft.",
        "str": "22 (+6)", "dex": "14 (+2)", "con": "22 (+6)", "int": "10 (+0)", "wis": "16 (+3)", "cha": "16 (+3)",
        "saving_throws": "Str +10, Con +10, Wis +7, Cha +7",
        "skills": "Athletics +10, Intimidation +7, Perception +7, Survival +7",
        "damage_resistances": "cold, lightning; bludgeoning, piercing, and slashing from nonmagical attacks",
        "damage_immunities": "fire, poison",
        "condition_immunities": "charmed, frightened, poisoned",
        "senses": "darkvision 120 ft., truesight 30 ft., passive Perception 17",
        "languages": "Gnoll, Abyssal, telepathy 60 ft.",
        "cr": "12 (8,400 XP)",
        "proficiency_bonus": "+4",
        "traits": {
            "Rampage": "When the Butcher reduces a creature to 0 hit points with a melee attack on its turn, it can take a bonus action to move up to half its speed and make a bite attack.",
            "Legendary Resistance (3/Day)": "If the Butcher fails a saving throw, it can choose to succeed instead.",
            "Yeenoghu's Chosen": "The Butcher has been physically reshaped by Yeenoghu's power. It is Large, its attacks are magical, and it counts as both a fiend and a gnoll. It has advantage on saving throws against being banished. If the Butcher kills a humanoid, there is a 25% chance that a maw demon spawns from the remains.",
            "Aura of the Charnel Pit (30 ft.)": "Each hostile creature that starts its turn within the aura must succeed on a DC 17 Constitution saving throw or take 7 (2d6) necrotic damage and be unable to regain hit points until the start of its next turn.",
            "Unending Hunger": "The Butcher regains 10 hit points at the start of each of its turns if it has at least 1 hit point. If the Butcher takes radiant damage, this trait doesn't function at the start of its next turn."
        },
        "actions": {
            "Multiattack": "The Butcher makes three attacks: two with the Flail of the Abyss and one with its Bite. It can replace one Flail attack with Rending Howl.",
            "Flail of the Abyss": "+10 to hit, reach 10 ft., 15 (2d8 + 6) bludgeoning damage plus 9 (2d8) necrotic damage. Target must succeed on DC 18 Strength saving throw or be knocked prone.",
            "Bite": "+10 to hit, reach 5 ft., 11 (1d10 + 6) piercing damage plus 9 (2d8) necrotic damage. Regains hit points equal to necrotic damage dealt.",
            "Rending Howl": "Target within 60 ft must succeed DC 17 Wisdom save or take 18 (4d8) psychic damage and be stunned until end of next turn.",
            "Jaws of the Abyss (Recharge 5-6)": "20-foot-radius, DC 18 Dex save, 36 (8d8) necrotic damage. Killed creatures rise as gnoll witherlings."
        },
        "bonus_actions": {
            "Slaughter Command": "Commands up to three allied gnolls or fiends within 60 feet. Each can use reaction to move and make one melee attack."
        },
        "reactions": {
            "Abyssal Backlash": "When taking damage from a spell, forces caster DC 17 Con save. Failure: 14 (4d6) necrotic damage and concentration broken."
        },
        "legendary_actions": ["Move (half speed, no OA)", "Feast (2 actions, Bite attack with extra healing)", "Carrion Call (2 actions, summon 1d4 hyenas or 1 witherling)", "Apocalyptic Roar (3 actions, DC 17 Wis save or frightened, heals allied gnolls)"],
        "lair": "Flayed Hollow",
        "lair_actions": ["The Ground Hungers (spectral teeth, restrain)", "Carrion Swarm (biting flies, necrotic)", "Abyssal Rift (summon demons)", "Feast of the Fallen (consume corpses, heal)"],
        "vulnerability": "Radiant damage shuts down Unending Hunger for a round.",
        "personality": "An abyssal horror wearing a gnoll's skin. Speaks through telepathy in fragmented images of slaughter. Laughs constantly, a low hyena cackle that never stops.",
        "lore": "A Butcher of Yeenoghu is not merely a gnoll champion — it is an incursion event. When enough death and suffering have been offered in Yeenoghu's name, the demon lord reshapes his most devoted follower into a living gate between the Abyss and the Material Plane."
    },
    "Gnoll Fang of Ruin": {
        "type": "Medium humanoid (gnoll), chaotic evil",
        "ac": "16 (demon-scarred breastplate)",
        "hp": "105 (14d8 + 42)",
        "speed": "30 ft.",
        "str": "20 (+5)", "dex": "14 (+2)", "con": "16 (+3)", "int": "8 (-1)", "wis": "14 (+2)", "cha": "14 (+2)",
        "saving_throws": "Str +8, Con +6, Wis +5",
        "skills": "Athletics +8, Intimidation +5, Perception +5, Survival +5",
        "damage_resistances": "fire, poison",
        "condition_immunities": "frightened",
        "senses": "darkvision 60 ft., passive Perception 15",
        "languages": "Gnoll, Abyssal",
        "cr": "7 (2,900 XP)",
        "proficiency_bonus": "+3",
        "traits": {
            "Rampage": "When the gnoll reduces a creature to 0 hit points with a melee attack, it can take a bonus action to move up to half its speed and make a bite attack.",
            "Abyssal Fury": "Weapon attacks are magical. Extra 2d6 necrotic damage on melee hits. If below half HP, extra 3d6 necrotic instead.",
            "Relentless Hunger": "If reduced to 0 HP, instead reduced to 1 HP. Advantage on all attack rolls until end of next turn. Recharges after a short or long rest.",
            "Aura of Butchery": "Hostile creatures starting turn within 10 ft must DC 13 Wisdom save or be frightened until start of next turn."
        },
        "actions": {
            "Multiattack": "Three attacks: two with Ruinous Glaive and one with Bite.",
            "Ruinous Glaive": "+8 to hit, reach 10 ft., 10 (1d10 + 5) slashing plus 7 (2d6) necrotic damage.",
            "Bite": "+8 to hit, reach 5 ft., 7 (1d4 + 5) piercing plus 7 (2d6) necrotic. Regains HP equal to necrotic dealt.",
            "Feast of Carnage (Recharge 5-6)": "One Ruinous Glaive attack against each creature within 10 ft. Hit targets DC 16 Str save or knocked prone."
        },
        "bonus_actions": {
            "Demonic Surge": "Dash action. Opportunity attacks against it are made with disadvantage until end of turn."
        },
        "reactions": {
            "Savage Retaliation": "When a creature within 10 ft deals damage to it, it can make one Bite attack against that creature."
        },
        "legendary_resistance": "1/Day",
        "personality": "Not truly sapient. Speaks in Abyssal in short prophetic fragments like 'The Jaw opens,' 'All meat,' 'He hungers.' Does not negotiate.",
        "lore": "Fangs of Ruin are created, not born. When a gnoll warband's slaughter reaches a critical threshold, Yeenoghu's power infuses the most savage warrior."
    },
    "Gnoll Packmaster": {
        "type": "Medium humanoid (gnoll), chaotic evil",
        "ac": "14 (hide armor, bone pauldrons)",
        "hp": "52 (8d8 + 16)",
        "speed": "30 ft.",
        "str": "16 (+3)", "dex": "14 (+2)", "con": "14 (+2)", "int": "8 (-1)", "wis": "12 (+1)", "cha": "12 (+1)",
        "saving_throws": "Str +5, Con +4",
        "skills": "Animal Handling +3, Intimidation +3, Perception +3, Survival +3",
        "senses": "darkvision 60 ft., passive Perception 13",
        "languages": "Gnoll, understands Abyssal",
        "cr": "3 (700 XP)",
        "proficiency_bonus": "+2",
        "traits": {
            "Rampage": "When the gnoll reduces a creature to 0 HP with a melee attack, bonus action to move half speed and make a bite attack.",
            "Alpha of the Pack": "Allied gnolls and hyenas within 30 ft deal extra 2 (1d4) damage with melee attacks. When Packmaster hits, allied hyenas within 30 ft can use reaction to move toward target.",
            "Blood Frenzy": "Advantage on melee attack rolls against any creature that doesn't have all its hit points."
        },
        "actions": {
            "Multiattack": "Two attacks: one Flail of Teeth and one Bite.",
            "Flail of Teeth": "+5 to hit, reach 5 ft., 7 (1d8 + 3) bludgeoning plus 3 (1d6) piercing from embedded teeth and bone shards.",
            "Bite": "+5 to hit, reach 5 ft., 5 (1d4 + 3) piercing. DC 13 Con save or contract a disease reducing HP maximum.",
            "War Howl (Recharge 6)": "Audible 300 ft. Allied gnolls/hyenas can repeat saves vs charm/fright. All allied gnolls/hyenas within 60 ft gain advantage on attacks until start of next turn."
        },
        "reactions": {
            "Punish the Weak": "When an allied gnoll or hyena within 5 ft drops to 0 HP, Packmaster can attack the creature that dealt the killing blow."
        },
        "personality": "More cunning than a Scavenger but still brutish. Communicates through violence and dominance displays. Maintains control by maiming challengers.",
        "companions": "Typically accompanied by 2-4 hyenas and 2-4 Gnoll Scavengers."
    },
    "Gnoll Scavenger": {
        "type": "Medium humanoid (gnoll), chaotic evil",
        "ac": "12 (hide scraps)",
        "hp": "16 (3d8 + 3)",
        "speed": "30 ft.",
        "str": "14 (+2)", "dex": "12 (+1)", "con": "12 (+1)", "int": "6 (-2)", "wis": "10 (+0)", "cha": "6 (-2)",
        "skills": "Perception +2, Survival +2",
        "senses": "darkvision 60 ft., passive Perception 12",
        "languages": "Gnoll",
        "cr": "1/4 (50 XP)",
        "proficiency_bonus": "+2",
        "traits": {
            "Rampage": "When the gnoll reduces a creature to 0 HP with a melee attack, bonus action to move half speed and make a bite attack.",
            "Carrion Sense": "Advantage on Perception and Survival checks that rely on smell. Can detect the scent of blood or decay within 1 mile.",
            "Hunger-Driven": "Advantage on melee attack rolls against creatures at or below half hit points."
        },
        "actions": {
            "Bone Club": "+4 to hit, reach 5 ft., 5 (1d6 + 2) bludgeoning damage.",
            "Bite": "+4 to hit, reach 5 ft., 4 (1d4 + 2) piercing damage.",
            "Javelin": "+4 to hit, range 30/120 ft., 5 (1d6 + 2) piercing damage."
        },
        "personality": "Barely sapient — more feral animal than person. Communicates in barks, cackles, and crude Gnoll. No concept of negotiation or mercy."
    },
    "Goblin Hexblade Stalker": {
        "type": "Small humanoid (goblinoid), lawful evil",
        "ac": "17 (shadow-woven leather, Charisma modifier)",
        "hp": "97 (15d6 + 45)",
        "speed": "30 ft., climb 20 ft.",
        "str": "10 (+0)", "dex": "18 (+4)", "con": "16 (+3)", "int": "14 (+2)", "wis": "13 (+1)", "cha": "18 (+4)",
        "saving_throws": "Dex +7, Wis +4, Cha +7",
        "skills": "Arcana +5, Deception +7, Perception +4, Stealth +10",
        "damage_resistances": "necrotic",
        "senses": "darkvision 120 ft., passive Perception 14",
        "languages": "Common, Goblin, Sylvan",
        "cr": "7 (2,900 XP)",
        "proficiency_bonus": "+3",
        "traits": {
            "Nimble Escape": "Can take Disengage or Hide as a bonus action on each of its turns.",
            "Shadow Patron's Gift": "Weapon attacks are magical and deal extra 2d6 necrotic damage. Advantage on Stealth in dim light or darkness, can hide when only lightly obscured.",
            "Hexblade's Curse": "+3 damage against cursed target, crits on 19-20, regains 15 HP if cursed target dies. Recharges after short or long rest.",
            "Evasion": "No damage on successful Dex save for half damage effects; half damage on failure."
        },
        "actions": {
            "Multiattack": "Three attacks: two Pact Blade and one Eldritch Blast.",
            "Pact Blade (Shadow Glaive Form)": "+7 to hit, reach 10 ft., 8 (1d8 + 4) slashing plus 7 (2d6) necrotic.",
            "Eldritch Blast": "+7 to hit, range 120 ft., 9 (1d10 + 4) force damage, target pushed 10 feet.",
            "Shadow Step (Recharge 5-6)": "Teleports up to 60 ft to dim light or darkness. Advantage on first melee attack after teleporting."
        },
        "spellcasting": "7th-level warlock. Charisma-based (DC 15, +7). Cantrips: minor illusion, prestidigitation. 2 4th-level slots: darkness, fear, shadow of moil, wrathful smite.",
        "reactions": {
            "Spectral Riposte": "When a creature within 10 ft misses with a melee attack, makes one Pact Blade attack against it."
        },
        "legendary_resistance": "1/Day",
        "personality": "Cold, patient, eerily polite. Speaks in whispers, refers to patron as 'the Voice in the Dark.' Views combat as a sacred ritual. Collects small bones from kills.",
        "lore": "Once a common goblin runt, chosen by a shadow entity dwelling in the Feydark. Now serves as assassin and envoy between goblin tribes."
    },
    "Goblin Raider Captain": {
        "type": "Small humanoid (goblinoid), neutral evil",
        "ac": "16 (chain shirt, shield)",
        "hp": "55 (10d6 + 20)",
        "speed": "30 ft.",
        "str": "12 (+1)", "dex": "16 (+3)", "con": "14 (+2)", "int": "13 (+1)", "wis": "12 (+1)", "cha": "14 (+2)",
        "saving_throws": "Dex +5, Cha +4",
        "skills": "Intimidation +4, Stealth +5, Perception +3",
        "senses": "darkvision 60 ft., passive Perception 13",
        "languages": "Common, Goblin",
        "cr": "3 (700 XP)",
        "proficiency_bonus": "+2",
        "traits": {
            "Nimble Escape": "Can take Disengage or Hide as a bonus action.",
            "Rally the Warband (1/Day)": "Bonus action war cry. Allied goblinoids within 30 ft gain 5 temp HP and advantage on next attack.",
            "Cunning Ambusher": "The captain and allied goblinoids within 30 ft gain +3 bonus to initiative rolls."
        },
        "actions": {
            "Multiattack": "Two melee attacks.",
            "Jagged Scimitar": "+5 to hit, reach 5 ft., 6 (1d6 + 3) slashing plus 3 (1d6) poison damage (cave-spider venom).",
            "Barbed Net": "+5 to hit, range 10/30 ft., target restrained. DC 13 Str check to free. 5 slashing damage to net (AC 10) also frees."
        },
        "reactions": {
            "Redirect Attack": "When targeted by an attack, swaps places with an allied goblinoid within 5 ft who becomes the target instead."
        },
        "personality": "Cruel and calculating. Rules through fear and grudging respect. Wears trophies from past raids. Speaks broken Common with mocking confidence."
    },
    "Goblin Skirmisher": {
        "type": "Small humanoid (goblinoid), neutral evil",
        "ac": "13 (leather armor)",
        "hp": "10 (3d6)",
        "speed": "30 ft.",
        "str": "8 (-1)", "dex": "14 (+2)", "con": "10 (+0)", "int": "10 (+0)", "wis": "8 (-1)", "cha": "8 (-1)",
        "skills": "Stealth +6",
        "senses": "darkvision 60 ft., passive Perception 9",
        "languages": "Common, Goblin",
        "cr": "1/4 (50 XP)",
        "proficiency_bonus": "+2",
        "traits": {
            "Nimble Escape": "Can take Disengage or Hide as a bonus action.",
            "Pack Rat": "Advantage on Survival checks to forage or scavenge for supplies."
        },
        "actions": {
            "Rusty Scimitar": "+4 to hit, reach 5 ft., 5 (1d6 + 2) slashing damage.",
            "Shortbow": "+4 to hit, range 80/320 ft., 5 (1d6 + 2) piercing damage.",
            "Mud Toss (Recharge 6)": "15 ft range. DC 10 Dex save or blinded until end of next turn."
        },
        "personality": "Cowardly alone, emboldened in groups. Chatter constantly, taunt enemies, bicker with allies. Hoard small shiny objects."
    },
    "Goblin Warlord Ascendant": {
        "type": "Small humanoid (goblinoid), lawful evil",
        "ac": "19 (mithral half plate, ring of protection)",
        "hp": "170 (20d6 + 100)",
        "speed": "30 ft.",
        "str": "16 (+3)", "dex": "20 (+5)", "con": "18 (+4)", "int": "17 (+3)", "wis": "15 (+2)", "cha": "18 (+4)",
        "saving_throws": "Str +7, Dex +9, Con +8, Wis +6",
        "skills": "Athletics +7, Deception +8, Insight +6, Intimidation +8, Perception +6, Stealth +9",
        "damage_resistances": "poison; bludgeoning, piercing, and slashing from nonmagical attacks",
        "condition_immunities": "charmed, frightened",
        "senses": "darkvision 120 ft., truesight 30 ft., passive Perception 16",
        "languages": "Common, Goblin, Orc, Sylvan, Undercommon",
        "cr": "12 (8,400 XP)",
        "proficiency_bonus": "+4",
        "traits": {
            "Nimble Escape": "Can take Disengage or Hide as a bonus action.",
            "Legendary Resistance (3/Day)": "If the Warlord fails a saving throw, it can choose to succeed instead.",
            "Warlord's Presence": "Allied creatures within 30 ft have advantage on saves vs charmed/frightened and deal extra 1d4 damage with weapon attacks.",
            "Crowned in Conquest": "Wears a crown forged from broken weapons of rival chieftains. Grants truesight 30 ft and cannot be surprised.",
            "Uncanny Dodge": "When hit by an attacker it can see, halves the attack's damage as a reaction."
        },
        "actions": {
            "Multiattack": "Three attacks: two Conqueror's Fang and one Crown's Command.",
            "Conqueror's Fang": "+9 to hit, reach 5 ft., 12 (2d6 + 5) piercing plus 7 (2d6) psychic. On crit, DC 16 Wis save or frightened.",
            "Crown's Command": "Target within 60 ft, DC 16 Cha save or compelled to move half speed in Warlord's chosen direction. Provokes opportunity attacks.",
            "Warcry of the Ascendant (Recharge 5-6)": "30 ft radius, DC 16 Con save, 28 (8d6) thunder damage and deafened 1 minute on failure. Allies healed 10 HP and can move."
        },
        "bonus_actions": {
            "Deploy the Warband": "Commands up to three allied goblinoids within 60 ft. Each can use reaction for one attack or full speed movement."
        },
        "reactions": {
            "Uncanny Dodge": "Halves damage from an attack it can see.",
            "Retributive Strike": "When hit by melee attack, commands one allied goblinoid within 5 ft of attacker to make a melee attack."
        },
        "legendary_actions": ["Move (half speed, no OA)", "Strike (2 actions, Conqueror's Fang attack)", "Tyrant's Gaze (2 actions, DC 16 Wis save or stunned)", "Rally the Horde (3 actions, stabilize and heal downed goblinoids)"],
        "lair": "war-camp or throne cavern",
        "lair_actions": ["Trap Sprung (pit trap, DC 15 Dex)", "Goblin Reinforcements (1d4 Skirmishers)", "Choking Smoke (heavily obscured 20 ft radius)"],
        "personality": "Terrifyingly competent. Speaks all languages fluently. Treats combat as chess and parley as a weapon. Utterly pragmatic.",
        "lore": "Once a nameless runt, united fractured goblin tribes through assassination, strategic alliances, and single combat against a bugbear warchief. Commands hundreds of goblinoids."
    },
    "Kobold Dragon Herald": {
        "type": "Small humanoid (kobold), lawful evil",
        "ac": "16 (dragon-scale vestments)",
        "hp": "91 (14d6 + 42)",
        "speed": "30 ft., fly 30 ft. (gifted wings, fragile)",
        "str": "8 (-1)", "dex": "16 (+3)", "con": "16 (+3)", "int": "18 (+4)", "wis": "14 (+2)", "cha": "16 (+3)",
        "saving_throws": "Con +6, Int +7, Wis +5",
        "skills": "Arcana +7, History +7, Perception +5, Religion +7",
        "damage_resistances": "fire (or patron dragon's breath type)",
        "senses": "darkvision 120 ft., blindsight 10 ft., passive Perception 15",
        "languages": "Common, Draconic, Infernal, Sylvan",
        "cr": "7 (2,900 XP)",
        "proficiency_bonus": "+3",
        "traits": {
            "Pack Tactics": "Advantage on attacks when an ally is within 5 ft of the target.",
            "Sunlight Sensitivity": "Disadvantage on attacks and sight-based Perception in sunlight.",
            "Dragon's Chosen": "Immune to frightful presence of dragons. Extra 1d6 damage when casting patron dragon's damage type spell.",
            "Fragile Wings": "If takes 15+ damage in one turn while flying, DC 15 Con save or lose flying speed until end of next turn.",
            "Draconic Conduit": "On death, explodes in 10 ft burst. DC 15 Dex save, 14 (4d6) patron dragon's damage type."
        },
        "actions": {
            "Multiattack": "Two Draconic Bolt attacks, or one Draconic Bolt and one Breath Siphon.",
            "Draconic Bolt": "+7 to hit, range 120 ft., 13 (2d8 + 4) patron dragon's damage type.",
            "Wyrm Staff": "+6 to hit, reach 5 ft., 6 (1d6 + 3) bludgeoning plus 7 (2d6) patron dragon's damage type.",
            "Breath Siphon (Recharge 5-6)": "30-foot cone, DC 15 Dex save, 28 (8d6) patron dragon's damage type."
        },
        "spellcasting": "7th-level caster. Int-based (DC 15, +7). Cantrips: fire bolt, mending, prestidigitation. 1st (4): absorb elements, shield, chromatic orb. 2nd (3): dragon's breath, scorching ray. 3rd (3): fireball, fly. 4th (1): wall of fire.",
        "bonus_actions": {
            "Draconic Command": "Allied kobold within 30 ft can use reaction to move half speed and make one attack with advantage."
        },
        "legendary_resistance": "1/Day",
        "personality": "Imperious and deeply devout. Considers itself the literal voice of dragonkind. Refers to non-kobolds as 'unscaled.' Treats goblins with open contempt.",
        "lore": "Rare kobolds born with faint draconic lineage, awakened through ritual and patron blessing. Serve as high priests, advisors, and generals within kobold warrens."
    },
    "Kobold Trapmaster": {
        "type": "Small humanoid (kobold), lawful evil",
        "ac": "15 (studded leather, trap-rigged shield)",
        "hp": "49 (9d6 + 18)",
        "speed": "30 ft., burrow 10 ft.",
        "str": "8 (-1)", "dex": "16 (+3)", "con": "14 (+2)", "int": "16 (+3)", "wis": "12 (+1)", "cha": "10 (+0)",
        "saving_throws": "Dex +5, Int +5",
        "skills": "Investigation +5, Perception +3, Stealth +5, Thieves' Tools +7",
        "senses": "darkvision 60 ft., passive Perception 13",
        "languages": "Common, Draconic, Gnomish",
        "cr": "3 (700 XP)",
        "proficiency_bonus": "+2",
        "traits": {
            "Pack Tactics": "Advantage on attacks when an ally is within 5 ft of the target.",
            "Sunlight Sensitivity": "Disadvantage on attacks and sight-based Perception in sunlight.",
            "Master Engineer": "Bonus action to arm or disarm a trap within 5 ft. Advantage on Investigation to detect traps and checks to disarm them.",
            "Trap Sense": "Trapmaster and allied kobolds within 30 ft have advantage on saves against traps the Trapmaster has placed."
        },
        "actions": {
            "Multiattack": "Two attacks with Pick-Axe Blade.",
            "Pick-Axe Blade": "+5 to hit, reach 5 ft., 6 (1d6 + 3) piercing damage.",
            "Alchemist's Fire Flask": "+5 to hit, range 20/60 ft., 7 (2d6) fire damage, target catches fire for 3 (1d6) fire per turn.",
            "Deploy Trap (3/Day)": "Deploys Spike Snare (DC 13 Dex, 2d6 piercing + speed 0), Flashpowder Charge (DC 13 Con, blinded), or Glue Bomb (DC 13 Str, restrained). Hidden, DC 15 Investigation to detect."
        },
        "reactions": {
            "Trigger Happy": "When a creature moves within 5 ft of a deployed trap, can trigger it immediately as a reaction."
        },
        "personality": "Intensely proud of its work. Names each trap design. Speaks slowly and precisely in Common from stolen engineering manuals. Considers direct fighting 'embarrassingly primitive.'"
    },
    "Kobold Tunneler": {
        "type": "Small humanoid (kobold), lawful evil",
        "ac": "12 (natural armor)",
        "hp": "7 (3d6 - 3)",
        "speed": "30 ft., burrow 10 ft.",
        "str": "7 (-2)", "dex": "15 (+2)", "con": "9 (-1)", "int": "10 (+0)", "wis": "10 (+0)", "cha": "8 (-1)",
        "skills": "Perception +2, Stealth +4",
        "senses": "darkvision 60 ft., passive Perception 12",
        "languages": "Common, Draconic",
        "cr": "1/4 (50 XP)",
        "proficiency_bonus": "+2",
        "traits": {
            "Pack Tactics": "Advantage on attacks when an ally is within 5 ft of the target.",
            "Sunlight Sensitivity": "Disadvantage on attacks and sight-based Perception in sunlight.",
            "Tunnel Rat": "Can move through spaces as narrow as 1 foot wide without squeezing. Advantage on Stealth checks made underground."
        },
        "actions": {
            "Shiv": "+4 to hit, reach 5 ft., 4 (1d4 + 2) piercing damage.",
            "Sling": "+4 to hit, range 30/120 ft., 4 (1d4 + 2) bludgeoning damage.",
            "Set Caltrop Line": "5-foot square within 5 ft. DC 12 Dex save or stop moving and take 1 piercing, speed reduced by 10 ft."
        },
        "personality": "Nervous, skittish, fanatically loyal to whoever they perceive as strongest. Speak in rapid-fire Draconic. Consider themselves 'chosen of dragons' and look down on goblins."
    },
    "Kobold Wyrmspeaker Sovereign": {
        "type": "Small humanoid (kobold), lawful evil",
        "ac": "19 (enchanted dragon-scale plate, ring of warding)",
        "hp": "153 (18d6 + 90)",
        "speed": "30 ft., fly 40 ft. (draconic wings)",
        "str": "10 (+0)", "dex": "18 (+4)", "con": "20 (+5)", "int": "20 (+5)", "wis": "16 (+3)", "cha": "18 (+4)",
        "saving_throws": "Dex +8, Con +9, Int +9, Wis +7",
        "skills": "Arcana +9, Deception +8, History +9, Insight +7, Perception +7",
        "damage_resistances": "fire; bludgeoning, piercing, and slashing from nonmagical attacks",
        "damage_immunities": "one type matching patron dragon's breath weapon",
        "condition_immunities": "charmed, frightened, paralyzed",
        "senses": "darkvision 120 ft., blindsight 30 ft., truesight 15 ft., passive Perception 17",
        "languages": "Common, Draconic, Dwarvish, Infernal, Undercommon",
        "cr": "12 (8,400 XP)",
        "proficiency_bonus": "+4",
        "traits": {
            "Pack Tactics": "Advantage on attacks when an ally is within 5 ft of the target.",
            "Legendary Resistance (3/Day)": "If the Sovereign fails a saving throw, it can choose to succeed instead.",
            "Voice of the Wyrm": "Allied kobolds within 60 ft immune to charmed and frightened. Verbal commands give advantage on next check or save.",
            "Draconic Apotheosis": "Has true draconic wings, hardened scales, counts as both kobold and dragon for spells and effects.",
            "Magic Resistance": "Advantage on saving throws against spells and other magical effects."
        },
        "actions": {
            "Multiattack": "Three attacks: two Wyrm Scepter and one Sovereign's Decree.",
            "Wyrm Scepter": "+9 to hit, reach 5 ft or range 60 ft., 11 (2d6 + 4) bludgeoning/force plus 10 (3d6) patron dragon's damage type.",
            "Sovereign's Decree": "Target within 90 ft, DC 17 Wis save. Kneel (prone + speed 0), Flee (move full speed away), or Turn (melee attack ally).",
            "Cataclysm Breath (Recharge 5-6)": "60-foot cone, DC 17 Dex save, 45 (10d8) patron dragon's damage type. Failure also pushed 15 ft and knocked prone."
        },
        "bonus_actions": {
            "Sovereign's Will": "Commands up to four allied kobolds within 60 ft. Each can use reaction to Attack, Dash, or Dodge."
        },
        "reactions": {
            "Dragon's Rebuke": "When damaged by creature within 60 ft, forces DC 17 Con save, 14 (4d6) patron dragon's damage type on failure."
        },
        "legendary_actions": ["Reposition (fly half speed, no OA)", "Wyrm Bolt (2 actions, ranged attack vs 3 targets in 15 ft radius)", "Draconic Barrier (2 actions, 30 ft wall dealing 3d6 dragon damage)", "Awaken the Blood (3 actions, buff allied kobold to Medium with extra damage)"],
        "lair": "Dragon's Sanctum",
        "lair_actions": ["Tremor (30 ft radius, prone + difficult terrain)", "Dragon's Eye (truesight 30 ft for all allies)", "Reinforcements from Below (1d4 Tunnelers)", "Breath Vents (3d6 dragon damage + poisoned)"],
        "personality": "Speaks with measured authority in perfect Common and Draconic. Does not grovel — treats dragons as revered equals. Philosopher-king building a civilization.",
        "lore": "A once-in-a-generation figure whose dormant draconic bloodline has been fully awakened through decades of ritual, study, and communion with ancient dragon spirits."
    }
}

def make_entry(question, correct_answer, incorrect_answer):
    return json.dumps({
        "input": {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ]
        },
        "preferred_output": [
            {"role": "assistant", "content": correct_answer}
        ],
        "non_preferred_output": [
            {"role": "assistant", "content": incorrect_answer}
        ]
    }, ensure_ascii=False)

def generate_entries():
    entries = []
    all_names = list(creatures.keys())
    
    # Helper for picking a wrong creature name
    def other_creature(name):
        others = [n for n in all_names if n != name]
        return random.choice(others)
    
    # Helper for wrong stat values
    def wrong_number(correct, low=1, high=30):
        wrong = correct
        while wrong == correct:
            wrong = random.randint(low, high)
        return wrong
    
    # Categorize by race
    gnolls = [n for n in all_names if "Gnoll" in n]
    goblins = [n for n in all_names if "Goblin" in n]
    kobolds = [n for n in all_names if "Kobold" in n]
    
    cr_map = {"Gnoll Scavenger": "1/4", "Gnoll Packmaster": "3", "Gnoll Fang of Ruin": "7", "Gnoll Butcher of Yeenoghu": "12",
              "Goblin Skirmisher": "1/4", "Goblin Raider Captain": "3", "Goblin Hexblade Stalker": "7", "Goblin Warlord Ascendant": "12",
              "Kobold Tunneler": "1/4", "Kobold Trapmaster": "3", "Kobold Dragon Herald": "7", "Kobold Wyrmspeaker Sovereign": "12"}
    
    for name, data in creatures.items():
        oc = other_creature(name)
        oc_data = creatures[oc]
        
        # === BASIC STAT QUESTIONS ===
        
        # 1. Type/alignment
        entries.append(make_entry(
            f"What is the creature type and alignment of the {name}?",
            f"The {name} is a {data['type']}.",
            f"The {name} is a {oc_data['type']}."
        ))
        
        # 2. AC
        entries.append(make_entry(
            f"What is the Armor Class of the {name}?",
            f"The {name} has an AC of {data['ac']}.",
            f"The {name} has an AC of {oc_data['ac']}."
        ))
        
        # 3. HP
        entries.append(make_entry(
            f"How many hit points does the {name} have?",
            f"The {name} has {data['hp']} hit points.",
            f"The {name} has {oc_data['hp']} hit points."
        ))
        
        # 4. Speed
        entries.append(make_entry(
            f"What is the speed of the {name}?",
            f"The {name} has a speed of {data['speed']}.",
            f"The {name} has a speed of {oc_data['speed']}."
        ))
        
        # 5. CR
        entries.append(make_entry(
            f"What is the Challenge Rating of the {name}?",
            f"The {name} has a Challenge Rating of {data['cr']}.",
            f"The {name} has a Challenge Rating of {oc_data['cr']}."
        ))
        
        # 6. Languages
        entries.append(make_entry(
            f"What languages does the {name} speak?",
            f"The {name} speaks {data['languages']}.",
            f"The {name} speaks {oc_data['languages']}."
        ))
        
        # 7. Senses
        entries.append(make_entry(
            f"What senses does the {name} have?",
            f"The {name} has {data['senses']}.",
            f"The {name} has {oc_data['senses']}."
        ))
        
        # 8. Proficiency bonus
        entries.append(make_entry(
            f"What is the proficiency bonus of the {name}?",
            f"The {name} has a proficiency bonus of {data['proficiency_bonus']}.",
            f"The {name} has a proficiency bonus of {oc_data['proficiency_bonus']}."
        ))
        
        # 9-14. Individual ability scores
        for ability in ["str", "dex", "con", "int", "wis", "cha"]:
            ability_name = {"str": "Strength", "dex": "Dexterity", "con": "Constitution", "int": "Intelligence", "wis": "Wisdom", "cha": "Charisma"}[ability]
            entries.append(make_entry(
                f"What is the {ability_name} score of the {name}?",
                f"The {name} has a {ability_name} of {data[ability]}.",
                f"The {name} has a {ability_name} of {oc_data[ability]}."
            ))
        
        # 15. Skills
        if "skills" in data:
            entries.append(make_entry(
                f"What skills does the {name} have?",
                f"The {name} has the following skills: {data['skills']}.",
                f"The {name} has the following skills: {oc_data.get('skills', 'Athletics +5, Stealth +3')}."
            ))
        
        # 16. Saving throws (if present)
        if "saving_throws" in data:
            entries.append(make_entry(
                f"What are the saving throw proficiencies of the {name}?",
                f"The {name} has saving throw proficiencies in {data['saving_throws']}.",
                f"The {name} has saving throw proficiencies in {oc_data.get('saving_throws', 'Dex +3, Con +2')}."
            ))
        
        # 17. Damage resistances (if present)
        if "damage_resistances" in data:
            entries.append(make_entry(
                f"What damage resistances does the {name} have?",
                f"The {name} has resistance to {data['damage_resistances']}.",
                f"The {name} has no damage resistances."
            ))
        
        # 18. Damage immunities (if present)
        if "damage_immunities" in data:
            entries.append(make_entry(
                f"What damage immunities does the {name} have?",
                f"The {name} is immune to {data['damage_immunities']}.",
                f"The {name} has no damage immunities."
            ))
        
        # 19. Condition immunities (if present)
        if "condition_immunities" in data:
            entries.append(make_entry(
                f"What condition immunities does the {name} have?",
                f"The {name} is immune to the {data['condition_immunities']} conditions.",
                f"The {name} has no condition immunities."
            ))
        
        # === TRAIT QUESTIONS ===
        for trait_name, trait_desc in data["traits"].items():
            entries.append(make_entry(
                f"What does the {name}'s {trait_name} trait do?",
                f"{trait_desc}",
                f"The {name} does not have a {trait_name} trait."
            ))
        
        # Does creature have specific trait?
        for trait_name in data["traits"]:
            entries.append(make_entry(
                f"Does the {name} have the {trait_name} trait?",
                f"Yes, the {name} has the {trait_name} trait.",
                f"No, the {name} does not have the {trait_name} trait."
            ))
        
        # === ACTION QUESTIONS ===
        for action_name, action_desc in data["actions"].items():
            entries.append(make_entry(
                f"Describe the {name}'s {action_name} action.",
                f"{action_desc}",
                f"The {name} does not have a {action_name} action."
            ))
        
        # === BONUS ACTIONS ===
        if "bonus_actions" in data:
            for ba_name, ba_desc in data["bonus_actions"].items():
                entries.append(make_entry(
                    f"What bonus action does the {name} have called {ba_name}?",
                    f"{ba_desc}",
                    f"The {name} does not have any bonus actions."
                ))
        
        # === REACTIONS ===
        if "reactions" in data:
            for r_name, r_desc in data["reactions"].items():
                entries.append(make_entry(
                    f"What is the {name}'s {r_name} reaction?",
                    f"{r_desc}",
                    f"The {name} does not have a {r_name} reaction."
                ))
        
        # === LEGENDARY ACTIONS ===
        if "legendary_actions" in data:
            la_list = ", ".join(data["legendary_actions"])
            entries.append(make_entry(
                f"What legendary actions can the {name} take?",
                f"The {name} can take 3 legendary actions, choosing from: {la_list}.",
                f"The {name} does not have any legendary actions."
            ))
        
        # === LAIR ACTIONS ===
        if "lair_actions" in data:
            la_str = ", ".join(data["lair_actions"])
            entries.append(make_entry(
                f"What lair actions does the {name} have?",
                f"In its {data['lair']}, the {name} can use the following lair actions on initiative count 20: {la_str}.",
                f"The {name} does not have any lair actions."
            ))
            
            entries.append(make_entry(
                f"Where is the {name}'s lair?",
                f"The {name}'s lair is the {data['lair']}.",
                f"The {name} does not have a lair."
            ))
        
        # === PERSONALITY ===
        if "personality" in data:
            entries.append(make_entry(
                f"How would you describe the {name}'s personality?",
                f"{data['personality']}",
                f"The {name} is friendly and cooperative, always willing to negotiate peacefully."
            ))
        
        # === LORE ===
        if "lore" in data:
            entries.append(make_entry(
                f"What is the lore behind the {name}?",
                f"{data['lore']}",
                f"The {name} is a common creature found in most taverns throughout the realm."
            ))
        
        # === SPELLCASTING ===
        if "spellcasting" in data:
            entries.append(make_entry(
                f"What spellcasting abilities does the {name} have?",
                f"{data['spellcasting']}",
                f"The {name} has no spellcasting abilities."
            ))
        
        # === LEGENDARY RESISTANCE ===
        if "legendary_resistance" in data:
            entries.append(make_entry(
                f"How many times per day can the {name} use Legendary Resistance?",
                f"The {name} can use Legendary Resistance {data['legendary_resistance']}.",
                f"The {name} does not have Legendary Resistance."
            ))
        
        # === VULNERABILITY ===
        if "vulnerability" in data:
            entries.append(make_entry(
                f"What is the key vulnerability of the {name}?",
                f"{data['vulnerability']}",
                f"The {name} has no particular vulnerabilities."
            ))
        
        # === COMPANIONS ===
        if "companions" in data:
            entries.append(make_entry(
                f"What creatures typically accompany the {name}?",
                f"{data['companions']}",
                f"The {name} always fights alone."
            ))
    
    # === CROSS-CREATURE COMPARISON QUESTIONS ===
    
    # Which creature has the highest/lowest HP?
    entries.append(make_entry(
        "Which creature in the collection has the highest hit points?",
        "The Gnoll Butcher of Yeenoghu has the highest hit points at 184 (16d10 + 96).",
        "The Goblin Warlord Ascendant has the highest hit points."
    ))
    entries.append(make_entry(
        "Which creature in the collection has the lowest hit points?",
        "The Kobold Tunneler has the lowest hit points at 7 (3d6 - 3).",
        "The Goblin Skirmisher has the lowest hit points."
    ))
    
    # Highest AC
    entries.append(make_entry(
        "Which creatures have the highest Armor Class?",
        "The Goblin Warlord Ascendant and Kobold Wyrmspeaker Sovereign both have the highest AC of 19.",
        "The Gnoll Butcher of Yeenoghu has the highest AC of 20."
    ))
    
    # Race-specific traits
    entries.append(make_entry(
        "What trait do all gnolls share?",
        "All gnolls share the Rampage trait, which allows them to move up to half their speed and make a bite attack as a bonus action when they reduce a creature to 0 hit points with a melee attack.",
        "All gnolls share the Pack Tactics trait."
    ))
    entries.append(make_entry(
        "What trait do all kobolds share?",
        "All kobolds share the Pack Tactics trait, which gives them advantage on attack rolls when an ally is within 5 feet of the target, and Sunlight Sensitivity, which gives them disadvantage on attacks and Perception checks in sunlight.",
        "All kobolds share the Rampage trait."
    ))
    entries.append(make_entry(
        "What trait do all goblins share?",
        "All goblins share the Nimble Escape trait, which allows them to take the Disengage or Hide action as a bonus action on each of their turns.",
        "All goblins share the Pack Tactics trait."
    ))
    
    # CR comparisons
    for race_name, race_list in [("gnoll", gnolls), ("goblin", goblins), ("kobold", kobolds)]:
        entries.append(make_entry(
            f"Which {race_name} creature has the highest Challenge Rating?",
            f"The {race_list[-1] if race_name != 'gnoll' else 'Gnoll Butcher of Yeenoghu'} has the highest CR among {race_name}s at CR 12.",
            f"The {race_list[0]} has the highest CR among {race_name}s."
        ))
    
    # Alignment questions
    entries.append(make_entry(
        "What alignment are most goblins in this collection?",
        "Most goblins are neutral evil (Goblin Skirmisher and Raider Captain), while the Goblin Hexblade Stalker and Goblin Warlord Ascendant are lawful evil.",
        "All goblins are chaotic evil."
    ))
    entries.append(make_entry(
        "What alignment are all gnolls in this collection?",
        "All gnolls in this collection are chaotic evil.",
        "All gnolls are neutral evil."
    ))
    entries.append(make_entry(
        "What alignment are all kobolds in this collection?",
        "All kobolds in this collection are lawful evil.",
        "All kobolds are chaotic neutral."
    ))
    
    # Size questions
    entries.append(make_entry(
        "Which creature in the collection is Large?",
        "The Gnoll Butcher of Yeenoghu is the only Large creature in the collection. It is a Large fiend (gnoll, demon).",
        "The Goblin Warlord Ascendant is the only Large creature."
    ))
    entries.append(make_entry(
        "Which creatures in the collection are Small?",
        "All goblins (Goblin Skirmisher, Raider Captain, Hexblade Stalker, Warlord Ascendant) and all kobolds (Kobold Tunneler, Trapmaster, Dragon Herald, Wyrmspeaker Sovereign) are Small.",
        "Only the kobolds are Small; goblins are Medium."
    ))
    
    # Flying creatures
    entries.append(make_entry(
        "Which creatures can fly?",
        "The Kobold Dragon Herald (fly 30 ft. with fragile gifted wings), the Kobold Wyrmspeaker Sovereign (fly 40 ft. with draconic wings), and the Goblin Hexblade Stalker (has climb 20 ft. but not flight).",
        "Only the Gnoll Butcher of Yeenoghu can fly."
    ))
    
    # Burrowing creatures
    entries.append(make_entry(
        "Which creatures have a burrow speed?",
        "The Kobold Tunneler (burrow 10 ft.) and the Kobold Trapmaster (burrow 10 ft.) have burrow speeds.",
        "All gnolls have a burrow speed of 20 ft."
    ))
    
    # Creatures with spellcasting
    entries.append(make_entry(
        "Which creatures have spellcasting abilities?",
        "The Goblin Hexblade Stalker (7th-level warlock, Charisma-based) and the Kobold Dragon Herald (7th-level caster, Intelligence-based) have spellcasting abilities.",
        "The Gnoll Butcher of Yeenoghu and Goblin Warlord Ascendant have spellcasting abilities."
    ))
    
    # Legendary actions
    entries.append(make_entry(
        "Which creatures have legendary actions?",
        "The Gnoll Butcher of Yeenoghu, the Goblin Warlord Ascendant, and the Kobold Wyrmspeaker Sovereign have legendary actions. All three are CR 12.",
        "Only the Gnoll Butcher of Yeenoghu has legendary actions."
    ))
    
    # Lair actions
    entries.append(make_entry(
        "Which creatures have lair actions?",
        "The Gnoll Butcher of Yeenoghu (in the Flayed Hollow), the Goblin Warlord Ascendant (in its war-camp or throne cavern), and the Kobold Wyrmspeaker Sovereign (in the Dragon's Sanctum) have lair actions.",
        "No creatures in the collection have lair actions."
    ))
    
    # === MORE VARIED QUESTION FORMATS ===
    
    for name, data in creatures.items():
        oc = other_creature(name)
        oc_data = creatures[oc]
        
        # "Who is X?" identity questions
        entries.append(make_entry(
            f"Who is the {name}?",
            f"The {name} is a {data['type']} with a Challenge Rating of {data['cr']}. It has {data['hp']} hit points and an AC of {data['ac']}.",
            f"The {name} is a {oc_data['type']} with a Challenge Rating of {oc_data['cr']}."
        ))
        
        # "How dangerous is X?" 
        entries.append(make_entry(
            f"How dangerous is the {name}?",
            f"The {name} has a Challenge Rating of {data['cr']}, making it {('a minor threat suitable for low-level parties' if '1/4' in data['cr'] else 'a moderate threat' if '3' in data['cr'] else 'a serious threat' if '7' in data['cr'] else 'a deadly boss encounter')}.",
            f"The {name} is not dangerous at all and poses no real threat to adventurers."
        ))
        
        # Can it do X?
        if "Multiattack" in data["actions"]:
            entries.append(make_entry(
                f"Can the {name} make multiple attacks in a turn?",
                f"Yes, the {name} has Multiattack: {data['actions']['Multiattack']}",
                f"No, the {name} can only make one attack per turn."
            ))
        
        # What happens when...
        if "Rampage" in data["traits"]:
            entries.append(make_entry(
                f"What happens when the {name} kills a creature in melee?",
                f"Thanks to Rampage, when the {name} reduces a creature to 0 HP with a melee attack, it can take a bonus action to move up to half its speed and make a bite attack.",
                f"Nothing special happens when the {name} kills a creature."
            ))
        
        if "Nimble Escape" in data["traits"]:
            entries.append(make_entry(
                f"How does the {name} escape from danger?",
                f"The {name} has Nimble Escape, allowing it to take the Disengage or Hide action as a bonus action on each of its turns.",
                f"The {name} has no special escape abilities and must use its action to Disengage."
            ))
        
        if "Pack Tactics" in data["traits"]:
            entries.append(make_entry(
                f"How does the {name} benefit from fighting alongside allies?",
                f"The {name} has Pack Tactics, gaining advantage on attack rolls against a creature if at least one ally is within 5 feet of the target and the ally isn't incapacitated.",
                f"The {name} gains no special benefit from fighting alongside allies."
            ))
        
        if "Sunlight Sensitivity" in data["traits"]:
            entries.append(make_entry(
                f"Does the {name} have any weakness in sunlight?",
                f"Yes, the {name} has Sunlight Sensitivity, giving it disadvantage on attack rolls and on Wisdom (Perception) checks that rely on sight while in sunlight.",
                f"No, the {name} has no weakness in sunlight."
            ))

    # === TACTICAL QUESTIONS ===
    tactical_qs = [
        ("How should the Gnoll Butcher of Yeenoghu be fought?",
         "The Butcher's key vulnerability is radiant damage, which shuts down its Unending Hunger regeneration for a round. Clerics and paladins are its priority targets for this reason. It opens with Jaws of the Abyss for AoE damage and raises witherlings from the dead.",
         "The Butcher should be fought with fire damage, as it is vulnerable to fire."),
        ("What is the Gnoll Fang of Ruin's combat strategy?",
         "The Fang uses Demonic Surge to close distance rapidly, then wades into groups relying on Aura of Butchery to frighten and Feast of Carnage to cleave. Its Bite provides sustain, and Abyssal Fury makes it more dangerous when bloodied.",
         "The Fang stays at range and uses spells to attack from a distance."),
        ("How does the Gnoll Packmaster fight?",
         "The Packmaster leads from the front, surrounded by its hyena pack. It opens with War Howl to empower allies, then charges the most wounded enemy to exploit Blood Frenzy. Alpha of the Pack ensures hyenas swarm whatever it attacks.",
         "The Packmaster hides behind its minions and avoids direct combat."),
        ("What tactics do Gnoll Scavengers use?",
         "Gnoll Scavengers charge the weakest-looking target, trying to down it quickly so Rampage chains into another attack. Hunger-Driven makes them more dangerous as enemies take wounds. They only retreat from fire or overwhelming force.",
         "Gnoll Scavengers use sophisticated flanking tactics and coordinate attacks with precision."),
        ("How does the Goblin Hexblade Stalker fight?",
         "The Stalker opens by casting darkness centered on itself, applies Hexblade's Curse to the highest-value target, uses Shadow Step to close distance, delivers Pact Blade strikes, and retreats using Nimble Escape. It uses fear against clustered enemies.",
         "The Stalker charges directly at enemies and relies on brute strength."),
        ("What is the Goblin Raider Captain's combat approach?",
         "The Captain opens with Rally the Warband, targets the most dangerous opponent with Barbed Net, then closes with Jagged Scimitar. It positions behind minions, uses Redirect Attack to stay alive, and orders focus fire on restrained targets.",
         "The Captain fights alone without using any of its leadership abilities."),
        ("How do Goblin Skirmishers fight?",
         "Skirmishers fight dirty and flee quickly. They attack from hiding with shortbows, close in with scimitars only when outnumbering foes, and use Nimble Escape to disengage the moment they take damage, retreating to re-hide.",
         "Skirmishers are brave frontline fighters who never retreat."),
        ("What is the Goblin Warlord Ascendant's battle strategy?",
         "The Warlord opens with Warcry of the Ascendant, uses Deploy the Warband for focus fire, stays behind its frontline using Crown's Command to drag isolated enemies into troops. It uses Tyrant's Gaze to neutralize dangerous combatants.",
         "The Warlord fights solo without any minions or tactical planning."),
        ("How does the Kobold Dragon Herald fight?",
         "The Herald stays at range, opening with Breath Siphon and following with Draconic Bolt or fireball. It uses shield for defense, fly for altitude advantage, and wall of fire to split the battlefield. Its Draconic Conduit makes it dangerous to kill in melee.",
         "The Herald fights in melee exclusively, using its Wyrm Staff."),
        ("What tactics does the Kobold Trapmaster use?",
         "The Trapmaster never engages without preparation. It opens with Alchemist's Fire, falls back through pre-mapped corridors deploying traps behind it, uses Trigger Happy to catch pursuers, and lets Tunneler minions swarm trapped enemies.",
         "The Trapmaster charges directly into combat and fights with its bare hands."),
        ("How do Kobold Tunnelers fight?",
         "Tunnelers cluster in groups of four or more to exploit Pack Tactics, swarming single targets with shivs while others sling stones from cover. They scatter caltrops in chokepoints and retreat through narrow tunnels. At half strength, they flee deeper.",
         "Tunnelers fight independently, each choosing different targets."),
        ("How does the Kobold Wyrmspeaker Sovereign fight?",
         "The Sovereign opens with Cataclysm Breath, uses Sovereign's Decree to neutralize threats (forcing fighters to flee, spellcasters to kneel), commands minions with Sovereign's Will, stays airborne, and uses Awaken the Blood to buff key minions.",
         "The Sovereign prefers peaceful negotiation and never initiates combat."),
    ]
    entries.extend([make_entry(q, a, w) for q, a, w in tactical_qs])
    
    # === ADDITIONAL VARIED QUESTIONS TO REACH 1000 ===
    
    extra_questions = [
        # Gnoll Butcher extras
        ("What type of damage does the Gnoll Butcher of Yeenoghu's Flail of the Abyss deal?",
         "The Flail of the Abyss deals 15 (2d8 + 6) bludgeoning damage plus 9 (2d8) necrotic damage.",
         "The Flail of the Abyss deals 15 (2d8 + 6) slashing damage plus 9 (2d8) fire damage."),
        ("What is the DC of the Gnoll Butcher's Aura of the Charnel Pit?",
         "The DC is 17 Constitution saving throw. On failure, creatures take 7 (2d6) necrotic damage and cannot regain hit points until the start of their next turn.",
         "The DC is 12 Dexterity saving throw."),
        ("How does the Gnoll Butcher's Unending Hunger work?",
         "The Butcher regains 10 hit points at the start of each of its turns if it has at least 1 hit point. If the Butcher takes radiant damage, this trait doesn't function at the start of its next turn.",
         "The Butcher regains 5 hit points at the end of each turn regardless of damage taken."),
        ("What happens when the Gnoll Butcher kills a humanoid?",
         "Due to Yeenoghu's Chosen, there is a 25% chance that a maw demon or a hyena that transforms into a gnoll at the next dawn spawns from the remains at the start of the Butcher's next turn.",
         "Nothing special happens when the Butcher kills a humanoid."),
        ("What is the reach of the Gnoll Butcher's Flail of the Abyss?",
         "The Flail of the Abyss has a reach of 10 feet.",
         "The Flail of the Abyss has a reach of 5 feet."),
        ("What is the area of effect of Jaws of the Abyss?",
         "Jaws of the Abyss affects a 20-foot-radius circle at a point within 60 feet.",
         "Jaws of the Abyss affects a 10-foot-radius circle at a point within 30 feet."),
        ("How does the Butcher's Abyssal Backlash reaction work?",
         "When the Butcher takes damage from a spell, it forces the caster to make a DC 17 Constitution saving throw. On failure, the caster takes 14 (4d6) necrotic damage and its concentration is broken. On success, half damage and concentration maintained.",
         "Abyssal Backlash triggers when the Butcher takes melee damage and reflects it back."),
        ("What is the Butcher's Carrion Call legendary action?",
         "Carrion Call costs 2 legendary actions and summons 1d4 hyenas or 1 gnoll witherling (zombie statistics with 30 ft. speed and Rampage) in unoccupied spaces within 30 feet. They act on initiative count 10.",
         "Carrion Call costs 1 legendary action and summons 2d6 gnolls."),
        ("What is the Butcher's Apocalyptic Roar legendary action?",
         "Apocalyptic Roar costs 3 legendary actions. Each creature within 30 feet must succeed on a DC 17 Wisdom saving throw or be frightened until the end of its next turn. Allied gnolls within 60 feet are healed for 10 HP and can move half speed without provoking.",
         "Apocalyptic Roar costs 1 legendary action and deals thunder damage."),
        
        # Gnoll Fang of Ruin extras
        ("How does the Gnoll Fang of Ruin's Abyssal Fury trait change when bloodied?",
         "Normally, Abyssal Fury deals extra 2d6 necrotic damage on melee weapon attacks. When below half hit points, it deals extra 3d6 necrotic damage instead.",
         "Abyssal Fury does not change based on the Fang's hit points."),
        ("What is the Gnoll Fang of Ruin's Relentless Hunger?",
         "If the Fang takes damage that would reduce it to 0 hit points, it is instead reduced to 1 hit point. Its eyes blaze with abyssal fire and it has advantage on all attack rolls until the end of its next turn. Recharges after a short or long rest.",
         "Relentless Hunger allows the Fang to automatically heal 20 hit points when it drops to 0 HP."),
        ("What is the DC for the Fang of Ruin's Aura of Butchery?",
         "The DC is 13 Wisdom saving throw. Hostile creatures starting their turn within 10 feet must succeed or be frightened until the start of their next turn.",
         "The DC is 17 Constitution saving throw within 30 feet."),
        ("What weapon does the Gnoll Fang of Ruin use?",
         "The Fang of Ruin wields a Ruinous Glaive, a magical weapon with +8 to hit, reach 10 ft., dealing 10 (1d10 + 5) slashing damage plus 7 (2d6) necrotic damage.",
         "The Fang of Ruin wields a Bone Club dealing 5 (1d6 + 2) bludgeoning damage."),
        ("How does Feast of Carnage work?",
         "Feast of Carnage (Recharge 5-6) lets the Fang make one Ruinous Glaive attack against each creature of its choice within 10 feet. Each creature hit must also succeed on a DC 16 Strength saving throw or be knocked prone.",
         "Feast of Carnage heals the Fang for all damage dealt."),
        ("Does the Gnoll Fang of Ruin have Demonic Surge?",
         "Yes, Demonic Surge is a bonus action that lets the Fang take the Dash action. Until the end of the turn, opportunity attacks against the Fang are made with disadvantage.",
         "No, the Gnoll Fang of Ruin does not have any bonus actions."),
        
        # Gnoll Packmaster extras
        ("How does the Gnoll Packmaster's Blood Frenzy work?",
         "Blood Frenzy gives the Packmaster advantage on melee attack rolls against any creature that doesn't have all its hit points.",
         "Blood Frenzy doubles the Packmaster's damage against bloodied creatures."),
        ("What does the Packmaster's Alpha of the Pack trait do for allies?",
         "Allied gnolls and hyenas within 30 feet deal an extra 2 (1d4) damage with melee attacks. When the Packmaster hits a creature, allied hyenas within 30 ft can use their reaction to move toward the target.",
         "Alpha of the Pack gives allied gnolls advantage on all saving throws."),
        ("Can the Packmaster's Bite cause disease?",
         "Yes, if the target is a creature, it must succeed on a DC 13 Constitution saving throw or contract a disease. The disease causes disadvantage on Constitution saves and reduces hit point maximum by 3 (1d6) for each 24 hours.",
         "No, the Packmaster's Bite only deals piercing damage."),
        ("How far can the Packmaster's War Howl be heard?",
         "The Packmaster's War Howl is audible up to 300 feet away. It allows allied gnolls and hyenas within 60 feet to repeat saves against charm/fright and gives advantage on attack rolls.",
         "The War Howl can only be heard within 30 feet."),
        ("What is the Packmaster's Punish the Weak reaction?",
         "When an allied gnoll or hyena within 5 feet of the Packmaster is reduced to 0 hit points, the Packmaster can make one Flail of Teeth attack against the creature that dealt the killing blow, if within reach.",
         "Punish the Weak allows the Packmaster to heal an ally that drops to 0 HP."),
        
        # Gnoll Scavenger extras
        ("How far can the Gnoll Scavenger detect the scent of blood?",
         "The Gnoll Scavenger can detect the scent of blood or decay within 1 mile thanks to its Carrion Sense trait.",
         "The Gnoll Scavenger can detect blood within 100 feet."),
        ("What is the Gnoll Scavenger's Javelin range?",
         "The Gnoll Scavenger's Javelin has a range of 30/120 ft. and deals 5 (1d6 + 2) piercing damage.",
         "The Gnoll Scavenger's Javelin has a range of 60/240 ft."),
        ("How does the Gnoll Scavenger's Hunger-Driven trait work?",
         "Hunger-Driven gives the Gnoll Scavenger advantage on melee attack rolls against creatures that are at or below half hit points (bloodied).",
         "Hunger-Driven lets the Scavenger make an extra attack each turn when hungry."),
        ("Does the Gnoll Scavenger have any saving throw proficiencies?",
         "No, the Gnoll Scavenger does not have any saving throw proficiencies listed. It relies on its raw ability modifiers.",
         "Yes, the Gnoll Scavenger has proficiency in Strength and Constitution saving throws."),
        ("What is the Intelligence score of the Gnoll Scavenger?",
         "The Gnoll Scavenger has an Intelligence of 6 (-2), making it barely sapient — more feral animal than person.",
         "The Gnoll Scavenger has an Intelligence of 14 (+2) and is quite clever."),
        
        # Goblin Hexblade Stalker extras
        ("What is the Goblin Hexblade Stalker's patron?",
         "The Stalker's patron is a shadow entity dwelling in the Feydark. The Stalker refers to it as 'the Voice in the Dark.'",
         "The Stalker's patron is Yeenoghu, the demon lord of gnolls."),
        ("How does the Hexblade Stalker's Shadow Step work?",
         "Shadow Step (Recharge 5-6) allows the Stalker to teleport up to 60 feet to an unoccupied space in dim light or darkness. After teleporting, it has advantage on the first melee attack before the end of its turn.",
         "Shadow Step lets the Stalker become invisible for 1 minute."),
        ("What spells does the Goblin Hexblade Stalker know?",
         "Cantrips: minor illusion, prestidigitation. Spells (2 4th-level slots): darkness, fear, shadow of moil, wrathful smite.",
         "The Stalker knows fireball, lightning bolt, and shield."),
        ("How does the Hexblade's Curse work?",
         "As a bonus action, the Stalker curses one creature within 30 feet for 1 minute. It gains +3 damage, crits on 19-20 against the target, and regains 15 HP if the cursed target dies. Recharges after a short or long rest.",
         "Hexblade's Curse deals 2d6 necrotic damage to all creatures within 30 feet."),
        ("What is the Goblin Hexblade Stalker's Stealth bonus?",
         "The Goblin Hexblade Stalker has a +10 bonus to Stealth checks. It also has advantage on Stealth checks in dim light or darkness due to Shadow Patron's Gift.",
         "The Goblin Hexblade Stalker has a +4 bonus to Stealth checks."),
        ("Can the Goblin Hexblade Stalker climb?",
         "Yes, the Goblin Hexblade Stalker has a climb speed of 20 ft.",
         "No, the Goblin Hexblade Stalker has no special movement modes beyond walking."),
        ("What does the Hexblade Stalker's Evasion trait do?",
         "When subjected to an effect requiring a Dexterity saving throw for half damage, the Stalker takes no damage on a success and half damage on a failure.",
         "Evasion gives the Stalker advantage on all Dexterity saving throws."),
        
        # Goblin Raider Captain extras
        ("What poison does the Goblin Raider Captain's scimitar use?",
         "The Jagged Scimitar is coated in cave-spider venom, dealing an additional 3 (1d6) poison damage on a hit.",
         "The scimitar uses basilisk venom that petrifies targets."),
        ("How does the Goblin Raider Captain's Redirect Attack work?",
         "When targeted by an attack, the Captain can choose an allied goblinoid within 5 feet. The two swap places, and the ally becomes the target of the attack instead.",
         "Redirect Attack allows the Captain to redirect a spell back at the caster."),
        ("What does Rally the Warband do?",
         "As a bonus action (1/Day), allied goblinoids within 30 feet gain 5 temporary hit points and have advantage on their next attack roll.",
         "Rally the Warband summons 1d6 additional goblins to join the fight."),
        ("How does the Goblin Raider Captain's Barbed Net work?",
         "Ranged weapon attack, +5 to hit, range 10/30 ft. The target is restrained. A creature can make a DC 13 Strength check to free itself, or deal 5 slashing damage to the net (AC 10) to free without harming it.",
         "The Barbed Net deals 2d6 piercing damage and poisons the target."),
        ("What does Cunning Ambusher do?",
         "Cunning Ambusher gives the Captain and allied goblinoids within 30 feet a +3 bonus to initiative rolls while the Captain is conscious.",
         "Cunning Ambusher gives the Captain advantage on attacks made from hiding."),
        
        # Goblin Skirmisher extras
        ("What is the range of the Goblin Skirmisher's Shortbow?",
         "The Goblin Skirmisher's Shortbow has a range of 80/320 ft. and deals 5 (1d6 + 2) piercing damage.",
         "The Shortbow has a range of 30/120 ft."),
        ("How does the Goblin Skirmisher's Mud Toss work?",
         "Mud Toss (Recharge 6) targets a creature within 15 feet. The target must succeed on a DC 10 Dexterity saving throw or be blinded until the end of its next turn.",
         "Mud Toss deals 2d6 bludgeoning damage to all creatures in a 10-foot radius."),
        ("Does the Goblin Skirmisher have expertise in Stealth?",
         "Yes, the Goblin Skirmisher has Stealth +6, which is higher than its DEX modifier +2 plus proficiency +2 would give (+4), indicating it has expertise (double proficiency) in Stealth.",
         "No, the Goblin Skirmisher has only a +2 to Stealth."),
        ("What is the Goblin Skirmisher's Pack Rat trait?",
         "Pack Rat gives the Goblin Skirmisher advantage on Wisdom (Survival) checks made to forage or scavenge for supplies.",
         "Pack Rat allows the Skirmisher to carry twice as much weight as normal."),
        
        # Goblin Warlord Ascendant extras
        ("What is the Goblin Warlord Ascendant's crown?",
         "The Warlord wears a crown forged from the broken weapons of rival chieftains. The Crowned in Conquest trait grants truesight out to 30 feet and prevents the Warlord from being surprised.",
         "The crown is a purely decorative piece with no magical properties."),
        ("How does Crown's Command work?",
         "Crown's Command targets one creature within 60 feet. The target must succeed on a DC 16 Charisma saving throw or be compelled to use its reaction to move up to half its speed in a direction the Warlord chooses. This movement provokes opportunity attacks.",
         "Crown's Command forces all creatures within 30 feet to kneel."),
        ("What is the Warlord's Warcry of the Ascendant?",
         "Warcry of the Ascendant (Recharge 5-6) forces hostile creatures within 30 feet to make a DC 16 Constitution save, taking 28 (8d6) thunder damage and being deafened for 1 minute on failure, half on success. Allied goblinoids within 30 feet regain 10 HP and can move.",
         "Warcry of the Ascendant gives all allies within 60 feet advantage on all rolls for 1 minute."),
        ("What is the Goblin Warlord Ascendant's Tyrant's Gaze?",
         "Tyrant's Gaze is a legendary action costing 2 actions. The Warlord fixes its gaze on one creature within 30 feet, which must succeed on a DC 16 Wisdom saving throw or be stunned until the end of its next turn. Success grants immunity for 24 hours.",
         "Tyrant's Gaze deals 4d6 psychic damage to all creatures that can see the Warlord."),
        ("What does Rally the Horde do?",
         "Rally the Horde costs 3 legendary actions. Each allied goblinoid within 60 feet that has 0 HP but hasn't failed three death saving throws is stabilized and regains 1 hit point.",
         "Rally the Horde summons 2d6 goblin reinforcements."),
        ("How many languages does the Goblin Warlord Ascendant speak?",
         "The Goblin Warlord Ascendant speaks five languages: Common, Goblin, Orc, Sylvan, and Undercommon.",
         "The Goblin Warlord Ascendant only speaks Goblin."),
        ("What is the Goblin Warlord Ascendant's Dexterity score?",
         "The Goblin Warlord Ascendant has a Dexterity of 20 (+5), the highest in the collection.",
         "The Goblin Warlord Ascendant has a Dexterity of 12 (+1)."),
        
        # Kobold Dragon Herald extras
        ("What happens when the Kobold Dragon Herald dies?",
         "Due to Draconic Conduit, when the Herald is reduced to 0 hit points, it explodes in a burst of draconic energy. Each creature within 10 feet must make a DC 15 Dexterity saving throw, taking 14 (4d6) damage of the patron dragon's type on failure, half on success.",
         "Nothing special happens when the Herald dies."),
        ("What are the Kobold Dragon Herald's Fragile Wings?",
         "The Herald has vestigial wings enhanced by draconic magic. If it takes 15 or more damage in a single turn while flying, it must succeed on a DC 15 Constitution saving throw or lose its flying speed until the end of its next turn.",
         "Fragile Wings grant permanent, unrestricted flight with no drawbacks."),
        ("What is the Dragon Herald's Breath Siphon?",
         "Breath Siphon (Recharge 5-6) channels a fragment of the patron's breath weapon in a 30-foot cone. Each creature must make a DC 15 Dexterity saving throw, taking 28 (8d6) damage of the patron dragon's type on failure, half on success.",
         "Breath Siphon is a single-target attack dealing 4d6 damage."),
        ("What spells can the Kobold Dragon Herald cast?",
         "Cantrips: fire bolt, mending, prestidigitation. 1st level (4 slots): absorb elements, shield, chromatic orb. 2nd level (3 slots): dragon's breath, scorching ray. 3rd level (3 slots): fireball, fly. 4th level (1 slot): wall of fire.",
         "The Dragon Herald can only cast cantrips and has no spell slots."),
        ("What does the Dragon Herald's Draconic Command do?",
         "As a bonus action, the Herald targets one allied kobold within 30 feet. The target can use its reaction to move up to half its speed and make one weapon attack with advantage.",
         "Draconic Command forces an enemy to obey the Herald's orders."),
        ("What is the Dragon Herald's spellcasting ability?",
         "The Dragon Herald's spellcasting ability is Intelligence (spell save DC 15, +7 to hit with spell attacks). It is a 7th-level spellcaster.",
         "The Dragon Herald uses Charisma for spellcasting with a DC of 12."),
        
        # Kobold Trapmaster extras
        ("What types of traps can the Kobold Trapmaster deploy?",
         "The Trapmaster can deploy three types of traps (3/Day): Spike Snare (DC 13 Dex, 2d6 piercing + speed 0), Flashpowder Charge (DC 13 Con, blinded), and Glue Bomb (DC 13 Str, restrained). All traps require DC 15 Investigation to detect.",
         "The Trapmaster can only deploy pit traps."),
        ("What does the Kobold Trapmaster's Master Engineer trait do?",
         "Master Engineer allows the Trapmaster to use a bonus action to arm or disarm a trap within 5 feet. It has advantage on Intelligence (Investigation) checks to detect traps and on ability checks made to disarm them.",
         "Master Engineer gives the Trapmaster proficiency with all artisan's tools."),
        ("How does the Trapmaster's Alchemist's Fire Flask work?",
         "Ranged weapon attack, +5 to hit, range 20/60 ft. It deals 7 (2d6) fire damage, and the target catches fire, taking 3 (1d6) fire damage at the start of each turn until extinguished.",
         "The flask deals cold damage and freezes the target in place."),
        ("What is the Kobold Trapmaster's Trigger Happy reaction?",
         "When a creature the Trapmaster can see moves within 5 feet of one of its deployed traps, the Trapmaster can use its reaction to trigger the trap immediately, even if the creature hasn't entered the trap's space.",
         "Trigger Happy allows the Trapmaster to throw two Alchemist's Fire Flasks as a reaction."),
        ("What languages does the Kobold Trapmaster speak?",
         "The Kobold Trapmaster speaks Common, Draconic, and Gnomish. It learned Common from stolen engineering manuals.",
         "The Kobold Trapmaster only speaks Draconic."),
        ("Does the Kobold Trapmaster have a burrow speed?",
         "Yes, the Kobold Trapmaster has a burrow speed of 10 ft.",
         "No, the Kobold Trapmaster can only walk."),
        
        # Kobold Tunneler extras
        ("What is the Kobold Tunneler's Tunnel Rat trait?",
         "Tunnel Rat allows the Kobold Tunneler to move through spaces as narrow as 1 foot wide without squeezing. It also has advantage on Dexterity (Stealth) checks made while underground.",
         "Tunnel Rat gives the Tunneler tremorsense out to 30 feet."),
        ("How does the Kobold Tunneler's Set Caltrop Line work?",
         "The Tunneler scatters caltrops in a 5-foot square within 5 feet. Any creature entering the area must succeed on a DC 12 Dexterity saving throw or stop moving and take 1 piercing damage, with walking speed reduced by 10 feet until healed.",
         "Set Caltrop Line creates a wall of caltrops 20 feet long."),
        ("What is the Kobold Tunneler's hit die size?",
         "The Kobold Tunneler uses d6 hit dice (Small creature), with 3d6 - 3 giving an average of 7 HP.",
         "The Kobold Tunneler uses d8 hit dice with an average of 15 HP."),
        ("How do Kobold Tunnelers view goblins?",
         "Kobold Tunnelers consider themselves the 'chosen of dragons' and look down on goblins.",
         "Kobold Tunnelers consider goblins to be their superiors and natural leaders."),
        
        # Kobold Wyrmspeaker Sovereign extras
        ("What is the Kobold Wyrmspeaker Sovereign's Draconic Apotheosis?",
         "The Sovereign has undergone a partial draconic transformation with true draconic wings, hardened scales, and draconic power. It counts as both a kobold and a dragon for the purposes of spells and effects.",
         "Draconic Apotheosis means the Sovereign has fully transformed into an adult dragon."),
        ("How does the Sovereign's Cataclysm Breath work?",
         "Cataclysm Breath (Recharge 5-6) affects a 60-foot cone. Each creature must make a DC 17 Dexterity save, taking 45 (10d8) damage of the patron dragon's type on failure, half on success. Failing creatures are also pushed 15 feet and knocked prone.",
         "Cataclysm Breath is a 30-foot line dealing 4d6 damage."),
        ("What is the Sovereign's Decree action?",
         "The Sovereign targets one creature within 90 feet. On a failed DC 17 Wisdom save, the target suffers Kneel (prone + speed 0), Flee (move full speed away), or Turn (attack an ally) — Sovereign's choice.",
         "Sovereign's Decree simply deals 3d6 psychic damage."),
        ("What is the Kobold Wyrmspeaker Sovereign's Magic Resistance?",
         "Magic Resistance gives the Sovereign advantage on saving throws against spells and other magical effects.",
         "Magic Resistance makes the Sovereign immune to all spells of 3rd level or lower."),
        ("What does Awaken the Blood do?",
         "Awaken the Blood costs 3 legendary actions. The Sovereign targets an allied kobold within 30 feet. Until the end of its next turn, it grows temporary draconic features: Medium size, 15 temp HP, extra 2d6 patron damage on weapon attacks, and advantage on all attack rolls.",
         "Awaken the Blood permanently transforms an allied kobold into a half-dragon."),
        ("What is the Sovereign's blindsight range?",
         "The Kobold Wyrmspeaker Sovereign has blindsight out to 30 feet.",
         "The Sovereign has blindsight out to 120 feet."),
        ("Does the Kobold Wyrmspeaker Sovereign have truesight?",
         "Yes, the Sovereign has truesight out to 15 feet.",
         "Yes, the Sovereign has truesight out to 120 feet."),
        ("How many languages does the Kobold Wyrmspeaker Sovereign speak?",
         "The Sovereign speaks five languages: Common, Draconic, Dwarvish, Infernal, and Undercommon.",
         "The Sovereign only speaks Draconic and Common."),
        ("What is the Sovereign's Voice of the Wyrm trait?",
         "Allied kobolds within 60 feet are immune to the charmed and frightened conditions while the Sovereign is conscious. When it gives a verbal command to an allied kobold, that kobold has advantage on its next ability check or saving throw.",
         "Voice of the Wyrm allows the Sovereign to speak to dragons telepathically across any distance."),
        ("What is the Sovereign's Dragon's Rebuke reaction?",
         "When the Sovereign takes damage from a creature within 60 feet, it can force that creature to make a DC 17 Constitution saving throw, taking 14 (4d6) damage of the patron dragon's type on failure, half on success.",
         "Dragon's Rebuke reflects all damage back to the attacker."),
        ("How does the Draconic Barrier legendary action work?",
         "Draconic Barrier costs 2 legendary actions. The Sovereign creates a wall of draconic energy 30 feet long, 10 feet high, and 1 foot thick within 60 feet. Creatures entering or starting their turn in the wall take 10 (3d6) patron dragon damage. Lasts until start of Sovereign's next turn.",
         "Draconic Barrier creates a permanent force field around the Sovereign."),
        
        # Cross-creature questions
        ("Which CR 1/4 creature has the most hit points?",
         "The Gnoll Scavenger has the most HP among CR 1/4 creatures at 16 (3d8 + 3), compared to the Goblin Skirmisher at 10 (3d6) and the Kobold Tunneler at 7 (3d6 - 3).",
         "The Kobold Tunneler has the most HP among CR 1/4 creatures."),
        ("Which CR 3 creature has the highest AC?",
         "The Goblin Raider Captain has the highest AC among CR 3 creatures at 16 (chain shirt, shield), followed by the Kobold Trapmaster at 15 and the Gnoll Packmaster at 14.",
         "The Gnoll Packmaster has the highest AC at 18."),
        ("Which CR 7 creature has the most hit points?",
         "The Gnoll Fang of Ruin has the most HP among CR 7 creatures at 105 (14d8 + 42), compared to the Goblin Hexblade Stalker at 97 and the Kobold Dragon Herald at 91.",
         "The Kobold Dragon Herald has the most HP at 150."),
        ("Which CR 12 creature is a fiend?",
         "The Gnoll Butcher of Yeenoghu is a Large fiend (gnoll, demon). The other CR 12 creatures (Goblin Warlord Ascendant and Kobold Wyrmspeaker Sovereign) are humanoids.",
         "The Goblin Warlord Ascendant is classified as a fiend."),
        ("Which creatures have the Rampage trait?",
         "All gnolls have Rampage: the Gnoll Scavenger, Gnoll Packmaster, Gnoll Fang of Ruin, and Gnoll Butcher of Yeenoghu.",
         "All creatures in the collection have the Rampage trait."),
        ("Which creatures have Nimble Escape?",
         "All goblins have Nimble Escape: the Goblin Skirmisher, Goblin Raider Captain, Goblin Hexblade Stalker, and Goblin Warlord Ascendant.",
         "All creatures in the collection have Nimble Escape."),
        ("Which creatures have Pack Tactics?",
         "All kobolds have Pack Tactics: the Kobold Tunneler, Kobold Trapmaster, Kobold Dragon Herald, and Kobold Wyrmspeaker Sovereign.",
         "Only the Kobold Tunneler has Pack Tactics."),
        ("Which creatures have Legendary Resistance 3/Day?",
         "The Gnoll Butcher of Yeenoghu, Goblin Warlord Ascendant, and Kobold Wyrmspeaker Sovereign all have Legendary Resistance 3/Day. These are the three CR 12 creatures.",
         "Only the Gnoll Butcher of Yeenoghu has Legendary Resistance 3/Day."),
        ("Which creatures have Legendary Resistance 1/Day?",
         "The Gnoll Fang of Ruin, Goblin Hexblade Stalker, and Kobold Dragon Herald all have Legendary Resistance 1/Day. These are the three CR 7 creatures.",
         "No creatures in the collection have Legendary Resistance 1/Day."),
        ("Which creature has the highest Strength score?",
         "The Gnoll Butcher of Yeenoghu has the highest Strength at 22 (+6).",
         "The Goblin Warlord Ascendant has the highest Strength at 24 (+7)."),
        ("Which creature has the highest Intelligence score?",
         "The Kobold Wyrmspeaker Sovereign has the highest Intelligence at 20 (+5).",
         "The Gnoll Butcher of Yeenoghu has the highest Intelligence at 18 (+4)."),
        ("Which creature has the highest Dexterity score?",
         "The Goblin Warlord Ascendant has the highest Dexterity at 20 (+5).",
         "The Gnoll Fang of Ruin has the highest Dexterity at 20 (+5)."),
        ("Which creature has the highest Constitution score?",
         "The Gnoll Butcher of Yeenoghu has the highest Constitution at 22 (+6), tied for highest ability score in the collection.",
         "The Kobold Wyrmspeaker Sovereign has the highest Constitution at 22 (+6)."),
        ("What is the difference between the Gnoll Scavenger and the Gnoll Packmaster?",
         "The Gnoll Scavenger (CR 1/4) is a basic foot soldier with 16 HP, Carrion Sense, and Hunger-Driven. The Gnoll Packmaster (CR 3) is a leader with 52 HP, Alpha of the Pack (buffs allies), Blood Frenzy, War Howl, and disease-carrying Bite. The Packmaster commands packs of Scavengers and hyenas.",
         "There is no difference; they are the same creature with different names."),
        ("What is the difference between the Goblin Skirmisher and the Goblin Raider Captain?",
         "The Goblin Skirmisher (CR 1/4) is a basic ranged combatant with 10 HP and Stealth expertise. The Raider Captain (CR 3) is a leader with 55 HP, poison scimitar, Barbed Net, Rally the Warband, Cunning Ambusher, and Redirect Attack. The Captain commands squads of Skirmishers.",
         "The Skirmisher is stronger than the Raider Captain."),
        ("What is the difference between the Kobold Tunneler and the Kobold Trapmaster?",
         "The Kobold Tunneler (CR 1/4) is a basic melee fighter with 7 HP, Tunnel Rat, and caltrops. The Trapmaster (CR 3) is an engineer with 49 HP, Master Engineer, deployable traps (Spike Snare, Flashpowder, Glue Bomb), Alchemist's Fire, and Trigger Happy reaction. The Trapmaster commands groups of Tunnelers.",
         "The Tunneler is the evolved form of the Trapmaster."),
        ("How do gnolls differ from goblins in combat style?",
         "Gnolls are aggressive melee berserkers driven by hunger, using Rampage to chain kills. Goblins are sneaky and tactical, using Nimble Escape to hit-and-run, with leaders providing buffs and coordination. Gnolls fight to the death; goblins retreat when outmatched.",
         "Gnolls and goblins fight identically, both preferring ranged attacks and stealth."),
        ("How do kobolds differ from goblins in combat style?",
         "Kobolds rely on Pack Tactics and overwhelming numbers, using traps and terrain to equalize against stronger foes. They have Sunlight Sensitivity but excel underground. Goblins use Nimble Escape for hit-and-run tactics, are more individually capable, and operate effectively on the surface.",
         "Kobolds and goblins are interchangeable and fight with identical strategies."),
        ("Which creature would be hardest to sneak past?",
         "The Gnoll Butcher of Yeenoghu and Kobold Wyrmspeaker Sovereign both have passive Perception 17, the highest in the collection. The Butcher also has darkvision 120 ft. and truesight 30 ft., while the Sovereign has darkvision 120 ft., blindsight 30 ft., and truesight 15 ft.",
         "The Goblin Skirmisher with passive Perception 9 would be hardest to sneak past."),
        ("Which creature has the lowest passive Perception?",
         "The Goblin Skirmisher has the lowest passive Perception at 9.",
         "The Gnoll Scavenger has the lowest passive Perception."),
        ("Which creatures have truesight?",
         "The Gnoll Butcher of Yeenoghu (truesight 30 ft.), the Goblin Warlord Ascendant (truesight 30 ft. from Crowned in Conquest), and the Kobold Wyrmspeaker Sovereign (truesight 15 ft.) have truesight.",
         "Only the Kobold Wyrmspeaker Sovereign has truesight."),
        ("Which creatures have telepathy?",
         "Only the Gnoll Butcher of Yeenoghu has telepathy (60 ft.), using it to transmit fragmented images of slaughter as psychological warfare.",
         "All CR 12 creatures have telepathy."),
        ("Which creature is the only one with a climb speed?",
         "The Goblin Hexblade Stalker is the only creature with a climb speed at 20 ft.",
         "The Kobold Tunneler has a climb speed of 15 ft."),
        ("What CR creature is the Gnoll Packmaster?",
         "The Gnoll Packmaster is CR 3 (700 XP).",
         "The Gnoll Packmaster is CR 7 (2,900 XP)."),
        ("What CR creature is the Goblin Raider Captain?",
         "The Goblin Raider Captain is CR 3 (700 XP).",
         "The Goblin Raider Captain is CR 5 (1,800 XP)."),
        ("What CR creature is the Kobold Trapmaster?",
         "The Kobold Trapmaster is CR 3 (700 XP).",
         "The Kobold Trapmaster is CR 1 (200 XP)."),
        ("Is hold person effective against the Gnoll Butcher of Yeenoghu?",
         "No, hold person only works on humanoids, and the Gnoll Butcher of Yeenoghu is a fiend (gnoll, demon), not a humanoid. It would not be affected.",
         "Yes, hold person works on the Butcher because it is part gnoll."),
        ("What is the highest damage single attack in the collection?",
         "The Kobold Wyrmspeaker Sovereign's Cataclysm Breath deals the highest damage at 45 (10d8) in a 60-foot cone, with targets also pushed 15 feet and knocked prone on a failed save.",
         "The Gnoll Butcher's Flail of the Abyss deals the highest damage."),
        ("Which creatures can regain hit points during combat through their own abilities?",
         "The Gnoll Butcher of Yeenoghu (Unending Hunger, Bite healing), the Gnoll Fang of Ruin (Bite healing), and the Goblin Hexblade Stalker (Hexblade's Curse kill healing) can all self-heal.",
         "Only the Gnoll Butcher of Yeenoghu can regain hit points during combat."),
        ("What size category are gnoll creatures?",
         "Most gnolls are Medium humanoids, except for the Gnoll Butcher of Yeenoghu which is Large (fiend).",
         "All gnolls are Large creatures."),
        ("Which creatures can summon reinforcements?",
         "The Gnoll Butcher of Yeenoghu (Carrion Call, Jaws of the Abyss raising dead), Goblin Warlord Ascendant (Goblin Reinforcements lair action), and Kobold Wyrmspeaker Sovereign (Reinforcements from Below lair action) can all summon reinforcements.",
         "Only the Kobold Wyrmspeaker Sovereign can summon reinforcements."),
        ("Which creatures have condition immunity to frightened?",
         "The Gnoll Fang of Ruin, Gnoll Butcher of Yeenoghu, Goblin Warlord Ascendant, and Kobold Wyrmspeaker Sovereign are all immune to the frightened condition.",
         "Only the Gnoll Butcher of Yeenoghu is immune to frightened."),
        ("What is the Gnoll Butcher's Feast legendary action?",
         "Feast costs 2 legendary actions. The Butcher makes one Bite attack, and if it hits, it regains additional hit points equal to the total damage dealt (both piercing and necrotic).",
         "Feast costs 1 legendary action and heals the Butcher for 20 HP."),
        ("How fast is the Gnoll Butcher of Yeenoghu?",
         "The Gnoll Butcher of Yeenoghu has a speed of 40 ft., faster than most creatures in the collection which have 30 ft.",
         "The Gnoll Butcher has a speed of 30 ft., the same as all other creatures."),
        ("Which creatures deal psychic damage?",
         "The Gnoll Butcher of Yeenoghu (Rending Howl, 4d8 psychic) and the Goblin Warlord Ascendant (Conqueror's Fang, 2d6 psychic) deal psychic damage.",
         "Only the Goblin Hexblade Stalker deals psychic damage."),
        ("Which creatures deal necrotic damage?",
         "The Gnoll Butcher of Yeenoghu (Flail, Bite, Aura, Jaws), the Gnoll Fang of Ruin (Ruinous Glaive, Bite via Abyssal Fury), and the Goblin Hexblade Stalker (Pact Blade via Shadow Patron's Gift) deal necrotic damage.",
         "Only the Gnoll Butcher deals necrotic damage."),
        ("Which creatures deal thunder damage?",
         "The Goblin Warlord Ascendant's Warcry of the Ascendant deals 28 (8d6) thunder damage in a 30-foot radius. It is the only creature in the collection that deals thunder damage.",
         "The Gnoll Butcher of Yeenoghu deals thunder damage with its roar."),
        ("Which creatures deal poison damage?",
         "The Goblin Raider Captain's Jagged Scimitar deals 3 (1d6) poison damage from cave-spider venom. It is the only creature that directly deals poison damage.",
         "All gnolls deal poison damage with their bite attacks."),
        ("Which creatures deal force damage?",
         "The Goblin Hexblade Stalker's Eldritch Blast deals 9 (1d10 + 4) force damage. It is the only creature dealing force damage. The Kobold Wyrmspeaker Sovereign's Wyrm Scepter also deals force damage at range.",
         "No creatures in the collection deal force damage."),
        ("Which creature has the most saving throw proficiencies?",
         "The Goblin Warlord Ascendant has the most saving throw proficiencies with four: Str +7, Dex +9, Con +8, Wis +6. The Kobold Wyrmspeaker Sovereign also has four: Dex +8, Con +9, Int +9, Wis +7.",
         "The Gnoll Scavenger has the most saving throw proficiencies."),
        ("Which creatures have damage immunity?",
         "The Gnoll Butcher of Yeenoghu is immune to fire and poison damage. The Kobold Wyrmspeaker Sovereign is immune to one damage type matching its patron dragon's breath weapon.",
         "No creatures in the collection have damage immunity."),
        ("How does the Gnoll Packmaster's Flail of Teeth differ from a normal flail?",
         "The Flail of Teeth deals 7 (1d8 + 3) bludgeoning damage plus 3 (1d6) piercing damage from embedded teeth and bone shards, combining two damage types in one attack.",
         "The Flail of Teeth is identical to a normal flail dealing only bludgeoning damage."),
    ]
    entries.extend([make_entry(q, a, w) for q, a, w in extra_questions])
    
    # Ensure we have exactly 1000 entries, pad with more cross-referencing questions if needed
    # Generate additional varied phrasing questions
    additional = []
    
    phrasings = [
        ("Tell me about the {name}.", "The {name} is a {type} creature with CR {cr}. It has {hp} HP, AC {ac}, and a speed of {speed}. It speaks {languages}.", "The {name} is a celestial creature that serves as a guardian of the heavens."),
        ("What armor does the {name} wear?", "The {name} has an AC of {ac}.", "The {name} wears plate armor giving it an AC of 20."),
        ("How tough is the {name}?", "The {name} has {hp} hit points and an AC of {ac}.", "The {name} has 500 hit points and is nearly invulnerable."),
        ("What size is the {name}?", "The {name} is {size}.", "The {name} is Gargantuan."),
        ("Is the {name} evil?", "Yes, the {name} is {alignment}.", "No, the {name} is true neutral and doesn't take sides."),
        ("How fast can the {name} move?", "The {name} has a speed of {speed}.", "The {name} has a speed of 60 ft."),
    ]
    
    size_map = {
        "Gnoll Butcher of Yeenoghu": "Large", "Gnoll Fang of Ruin": "Medium",
        "Gnoll Packmaster": "Medium", "Gnoll Scavenger": "Medium",
        "Goblin Hexblade Stalker": "Small", "Goblin Raider Captain": "Small",
        "Goblin Skirmisher": "Small", "Goblin Warlord Ascendant": "Small",
        "Kobold Dragon Herald": "Small", "Kobold Trapmaster": "Small",
        "Kobold Tunneler": "Small", "Kobold Wyrmspeaker Sovereign": "Small"
    }
    
    alignment_map = {
        "Gnoll Butcher of Yeenoghu": "chaotic evil", "Gnoll Fang of Ruin": "chaotic evil",
        "Gnoll Packmaster": "chaotic evil", "Gnoll Scavenger": "chaotic evil",
        "Goblin Hexblade Stalker": "lawful evil", "Goblin Raider Captain": "neutral evil",
        "Goblin Skirmisher": "neutral evil", "Goblin Warlord Ascendant": "lawful evil",
        "Kobold Dragon Herald": "lawful evil", "Kobold Trapmaster": "lawful evil",
        "Kobold Tunneler": "lawful evil", "Kobold Wyrmspeaker Sovereign": "lawful evil"
    }
    
    for name, data in creatures.items():
        for q_template, a_template, w in phrasings:
            q = q_template.format(name=name)
            a = a_template.format(
                name=name, type=data["type"], cr=data["cr"],
                hp=data["hp"], ac=data["ac"], speed=data["speed"],
                languages=data["languages"],
                size=size_map[name], alignment=alignment_map[name]
            )
            additional.append(make_entry(q, a, w))
    
    entries.extend(additional)
    
    # More questions to pad to 1000
    more_extras = [
        ("What is darkvision?", "Darkvision allows a creature to see in darkness as if it were dim light, and in dim light as if bright light, out to a specified range. Colors appear as shades of gray. Most goblins, kobolds, and gnolls have darkvision 60 ft.", "Darkvision allows a creature to see in complete darkness with full color perception."),
        ("What is blindsight?", "Blindsight allows a creature to perceive its surroundings without relying on sight, such as through echolocation or tremorsense. It is not fooled by invisibility or darkness.", "Blindsight means the creature is blind but has enhanced hearing."),
        ("What is truesight?", "Truesight allows a creature to see through illusions, invisibility, magical darkness, and shapechanging. It also allows seeing into the Ethereal Plane. It is extremely powerful and rare.", "Truesight simply means the creature has perfect 20/20 vision."),
        ("What is Pack Tactics?", "Pack Tactics gives a creature advantage on attack rolls against a target if at least one of the creature's allies is within 5 feet of the target and the ally isn't incapacitated. All kobolds in this collection have Pack Tactics.", "Pack Tactics allows a creature to attack twice per turn when near allies."),
        ("What is Rampage?", "Rampage allows a gnoll to take a bonus action to move up to half its speed and make a bite attack when it reduces a creature to 0 HP with a melee attack on its turn. All gnolls in this collection have Rampage.", "Rampage gives the creature advantage on all attacks for the rest of combat after killing an enemy."),
        ("What is Nimble Escape?", "Nimble Escape allows a goblin to take the Disengage or Hide action as a bonus action on each of its turns, making goblins very slippery and hard to pin down. All goblins in this collection have it.", "Nimble Escape allows the creature to teleport 30 feet as a bonus action."),
        ("What is Sunlight Sensitivity?", "Sunlight Sensitivity gives a creature disadvantage on attack rolls and on Wisdom (Perception) checks that rely on sight while in sunlight. All kobolds in this collection have this weakness.", "Sunlight Sensitivity causes the creature to take 1d6 radiant damage each round in sunlight."),
        ("What is Legendary Resistance?", "Legendary Resistance allows a creature to choose to succeed on a saving throw it would otherwise fail, a limited number of times per day. CR 7 creatures in this collection have it 1/Day, while CR 12 creatures have it 3/Day.", "Legendary Resistance makes a creature immune to all spells."),
        ("What are legendary actions?", "Legendary actions are special actions that powerful creatures can take at the end of other creatures' turns, outside of their own turn. A creature typically has 3 legendary actions per round. In this collection, the three CR 12 creatures have legendary actions.", "Legendary actions are simply normal actions that deal more damage."),
        ("What are lair actions?", "Lair actions are special effects that occur on initiative count 20 when a creature is in its lair. They represent the environment itself working in the creature's favor. The three CR 12 creatures in this collection have lair actions.", "Lair actions are traps that the creature sets before combat begins."),
        ("What is Challenge Rating?", "Challenge Rating (CR) is a rough estimate of how dangerous a creature is. A creature's CR corresponds to the level of a party of four adventurers for whom the creature would be a fair fight. This collection has creatures at CR 1/4, 3, 7, and 12.", "Challenge Rating is the number of hit dice a creature has."),
        ("What is a proficiency bonus?", "A proficiency bonus is a flat bonus that scales with power level, added to attack rolls, proficient saving throws, trained skill checks, and spell save DCs. CR 1/4-3 creatures have +2, CR 7 creatures have +3, and CR 12 creatures have +4.", "A proficiency bonus is the creature's Dexterity modifier."),
        ("How many creatures are in this collection?", "There are 12 creatures in this collection: 4 gnolls (Scavenger, Packmaster, Fang of Ruin, Butcher of Yeenoghu), 4 goblins (Skirmisher, Raider Captain, Hexblade Stalker, Warlord Ascendant), and 4 kobolds (Tunneler, Trapmaster, Dragon Herald, Wyrmspeaker Sovereign).", "There are 6 creatures in this collection."),
        ("What are the four CR tiers in this collection?", "The four CR tiers are: CR 1/4 (50 XP) with Gnoll Scavenger, Goblin Skirmisher, and Kobold Tunneler; CR 3 (700 XP) with Gnoll Packmaster, Goblin Raider Captain, and Kobold Trapmaster; CR 7 (2,900 XP) with Gnoll Fang of Ruin, Goblin Hexblade Stalker, and Kobold Dragon Herald; and CR 12 (8,400 XP) with Gnoll Butcher of Yeenoghu, Goblin Warlord Ascendant, and Kobold Wyrmspeaker Sovereign.", "The four CR tiers are CR 1, CR 5, CR 10, and CR 15."),
        ("What three races are represented in this collection?", "The three races are gnolls (chaotic evil, savage, hunger-driven), goblins (typically evil, sneaky, tactical), and kobolds (lawful evil, pack-oriented, trap-using). Each race has four creatures at CR 1/4, 3, 7, and 12.", "The three races are orcs, trolls, and ogres."),
        ("What is the Gnoll Scavenger's Bone Club attack?", "The Bone Club is a melee weapon attack: +4 to hit, reach 5 ft., dealing 5 (1d6 + 2) bludgeoning damage.", "The Bone Club deals 10 (2d6 + 3) slashing damage."),
        ("What is the Goblin Skirmisher's Rusty Scimitar attack?", "The Rusty Scimitar is a melee weapon attack: +4 to hit, reach 5 ft., dealing 5 (1d6 + 2) slashing damage.", "The Rusty Scimitar deals 8 (1d8 + 4) slashing damage and poisons the target."),
        ("What is the Kobold Tunneler's Shiv attack?", "The Shiv is a melee weapon attack: +4 to hit, reach 5 ft., dealing 4 (1d4 + 2) piercing damage.", "The Shiv deals 7 (1d10 + 2) piercing damage."),
        ("What is the Kobold Tunneler's Sling attack?", "The Sling is a ranged weapon attack: +4 to hit, range 30/120 ft., dealing 4 (1d4 + 2) bludgeoning damage.", "The Sling deals 8 (2d6 + 1) bludgeoning damage with a range of 80/320 ft."),
    ]
    entries.extend([make_entry(q, a, w) for q, a, w in more_extras])
    
    # Shuffle and trim/pad to exactly 1000
    random.seed(42)
    random.shuffle(entries)
    
    if len(entries) > 1000:
        entries = entries[:1000]
    elif len(entries) < 1000:
        # Duplicate with slight rephrasing
        deficit = 1000 - len(entries)
        rephrase_prefixes = [
            "Can you tell me, ", "I'd like to know, ", "Please explain, ",
            "Could you describe ", "What can you tell me about ", "I'm curious, "
        ]
        extra = []
        idx = 0
        while len(extra) < deficit:
            original = json.loads(entries[idx % len(entries)])
            prefix = rephrase_prefixes[idx % len(rephrase_prefixes)]
            original_q = original["input"]["messages"][1]["content"]
            # Make it lowercase after prefix
            new_q = prefix + original_q[0].lower() + original_q[1:]
            original["input"]["messages"][1]["content"] = new_q
            extra.append(json.dumps(original, ensure_ascii=False))
            idx += 1
        entries.extend(extra)
    
    return entries[:1000]

if __name__ == "__main__":
    entries = generate_entries()
    output_path = r"C:\Users\nirovins\eclipse-workspace\dnd-npc-agent\model-finetuning\DataGeneration\scripts\dnd_npc_data.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(entry + "\n")
    print(f"Generated {len(entries)} entries to {output_path}")
