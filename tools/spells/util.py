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


expected_list_keys = [
    'name',
    'level',
    'srd',
    'basicRules',
    'duration',
    'time',
    'range',
    'school',
    'components',
    'source',
    'page',
    'entries'
]


def update(entity: dict) -> str:
    has_unexpected_keys = False
    for key in entity:
        if key not in expected_list_keys:
            print(f"Unexpected key: {key} in entity: {entity['name']}")
            has_unexpected_keys = True
    if has_unexpected_keys:
        raise Exception("Unexpected keys found in entity")
    components = entity['components']
    material = ''
    value_components = list()
    if 'v' in components:
        value_components.append('V')
    if 's' in components:
        value_components.append('S')
    if 'm' in components:
        value_components.append('M')
        material = components['m']['text']

    duration_source = entity['duration']
    if len(duration_source) > 1:
        raise Exception("Multiple durations found")
    else:
        duration_source = duration_source[0]
        if duration_source['type'] == 'instant':
            duration = 'Instantaneous'
        elif duration_source['type'] == 'timed':
            duration = f"{duration_source['duration']['number']} {duration_source['duration']['unit']}"
        else:
            raise Exception(f"Unexpected duration type: {duration_source['type']} found in entity: {entity['name']}")

    range_source = entity['range']
    if range_source['type'] == 'radius':
        if range_source['distance']['type'] == 'feet':
            range = f"{range_source['distance']['amount'] // 5} sq."
        else:
            raise Exception(
                f"Unexpected range distance type: {range_source['distance']['type']} found in entity: {entity['name']}")
    else:
        raise Exception(f"Unexpected range type: {range_source['type']} found in entity: {entity['name']}")

    spell_classes = list()
    classes = entity['classes']
    for cl in classes['fromClassList']:
        spell_classes.append(cl['name'])

    return f"""name: "{entity['name']}"
spell_level: {map_spell_to_enum(entity['level'])}
casting_time: '{entity['duration'][0]['number']} {entity['duration'][0]['unit']}'
range: '{range}'
components: '{', '.join(value_components)}'
materials: '{material}'
duration: '{duration}'
school: {map_spell_school_to_enum(entity['school'])}
attack: ''
effect: ''
higher_levels: ''
classes: '{', '.join(spell_classes)}'
spell_description: "{'\\n\\n'.join(entity['entries'])}"
source: '{entity['source']}, p. {entity['page']}'
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
