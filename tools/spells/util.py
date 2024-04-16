




def map_spell_to_enum(level: int) -> str:
    return {
        0: '0-level',
        1: '1-level',
        2: '2-level',
        3: '3-level',
        4: '4-level',
        5: '5-level',
        6: '6-level',
        7: '7-level',
        8: '8-level',
        9: '9-level'
    }[level]


def map_spell_school_to_enum(school: str) -> str:
    return {
        'A': 'Abjuration',
        'C': 'Conjuration',
        'D': 'Divination',
        'E': 'Enchantment',
        'V': 'Evocation',
        'I': 'Illusion',
        'N': 'Necromancy',
        'T': 'Transmutation'
    }[school]




def update(entity: dict) -> str:

    return f"""name: {entity['name']} 
spell_level: {map_spell_to_enum(entity['level'])}
casting_time: '1 action'
range: '12 sq.'
components: 'V, S, M'
materials: 'a diamond worth at least 5,000 gp'
duration: 'Concentration, up to 1 minute'
school: Conjuration
attack: ''
effect: ''
higher_levels: ''
classes: 'Cleric, Sorcerer, Wizard'
spell_description: "You conjure a portal linking an unoccupied space you can see within range to a precise location on a different plane of existence. The portal is a circular opening, which you can make 1.5m to 6m in diameter. You can orient the portal in any direction you choose. The portal lasts for the duration. The portal has a front and a back on each plane where it appears. Travel through the portal is possible only by moving through its front. Anything that does so is instantly transported to the other plane, appearing in the unoccupied space nearest to the portal. Deities and other planar rulers can prevent portals created by this spell from opening in their presence or anywhere within their domains.\r\n\r\nWhen you cast this spell, you can speak the name of a specific creature (a pseudonym, title, or nickname doesn’t work). If that creature is on a plane other than the one you are on, the portal opens in the named creature’s immediate vicinity and draws the creature through it to the nearest unoccupied space on your side of the portal. You gain no special power over the creature, and it is free to act as the DM deems appropriate. It might leave, attack you, or help you."
source: 'Basic Rules, pg. 244'
"""


def map_spell_level_to_folder(level: int) -> str:
    return {
        0: 'Spells - Cantrips',
        1: 'Spells - 1st Level',
        2: 'Spells - 2nd Level',
        3: 'Spells - 3rd Level',
        4: 'Spells - 4th Level',
        5: 'Spells - 5th Level',
        6: 'Spells - 6th Level',
        7: 'Spells - 7th Level',
        8: 'Spells - 8th Level',
        9: 'Spells - 9th Level'
    }[level]

