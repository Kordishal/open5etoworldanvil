import re
from typing import List, Any


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


def map_saving_throw_to_enum(saving_throw: str) -> str:
    return {
        'strength': 'STR Save',
        'dexterity': 'DEX Save',
        'constitution': 'CON Save',
        'intelligence': 'INT Save',
        'wisdom': 'WIS Save',
        'charisma': 'CHA Save',
    }[saving_throw]


def map_saving_throws_to_texts(saving_throw: List[str]) -> List[str]:
    return [map_saving_throw_to_enum(s) for s in saving_throw]


def map_spell_attack_to_enum(attack: str) -> str:
    return {
        'R': 'Ranged',
        'M': 'Melee',
    }[attack]


def transform_entry(entry: str) -> str:

    def get_roll(match: re.Match[str]):
        if match:
            return f"[roll:{match.group(1)}]"
        else:
            raise Exception(f"No roll found in entry: {entry}")

    def get_condition(match: re.Match[str]):
        if match:
            return f"{match.group(1)}"
        else:
            raise Exception(f"No condition found in entry: {entry}")

    def get_item_name(match: re.Match[str]):
        if match:
            return f"{match.group(1).capitalize()}"
        else:
            raise Exception(f"No item name found in entry: {entry}")

    def get_skill_name(match: re.Match[str]):
        if match:
            return f"{match.group(1)}"
        else:
            raise Exception(f"No skill name found in entry: {entry}")

    def get_quick_ref(match: re.Match[str]):
        if match:
            return f"{match.group(1)}"
        else:
            raise Exception(f"No quick ref found in entry: {entry}")

    def get_status(match: re.Match[str]):
        if match:
            return f"{match.group(1)}"
        else:
            raise Exception(f"No status found in entry: {entry}")

    def get_spell(match: re.Match[str]):
        if match:
            return f"{match.group(1)}"
        else:
            raise Exception(f"No spell found in entry: {entry}")

    def get_sense(match: re.Match[str]):
        if match:
            return f"{match.group(1)}"
        else:
            raise Exception(f"No sense found in entry: {entry}")

    def get_chance(match: re.Match[str]):
        if match:
            return f"[roll:1d100<={match.group(1)}]"
        else:
            raise Exception(f"No chance found in entry: {entry}")

    def get_filter(match: re.Match[str]):
        if match:
            return f"{match.group(1)}"
        else:
            raise Exception(f"No filter found in entry: {entry}")

    def get_action(match: re.Match[str]):
        if match:
            return f"{match.group(1)}"
        else:
            raise Exception(f"No action found in entry: {entry}")

    def make_italics(match: re.Match[str]):
        if match:
            return f"[i]{match.group(1)}[/i]"
        else:
            raise Exception(f"No source found in entry: {entry}")

    def get_adventure(match: re.Match[str]):
        if match:
            return f"{match.group(1)}"
        else:
            raise Exception(f"No adventure found in entry: {entry}")

    def get_class_feature(match: re.Match[str]):
        if match:
            return f"{match.group(1)}"
        else:
            raise Exception(f"No class feature found in entry: {entry}")

    def get_d20(match: re.Match[str]):
        if match:
            return f"[roll:1d20+{match.group(1)}]"
        else:
            raise Exception(f"No d20 found in entry: {entry}")

    entry = re.sub(r'\{@chance (\d+)\|\|\|.+?\|.+?}', get_chance, entry)
    entry = re.sub(r'\{@condition (.+?)}', get_condition, entry)
    entry = re.sub(r'\{@damage (.+?)}', get_roll, entry)
    entry = re.sub(r'\{@dice (.+?)}', get_roll, entry)
    entry = re.sub(r'\{@d20 (\d+)}', get_d20, entry)
    entry = re.sub(r'\{@scaledamage .+?\|.+?\|(.+?)}', get_roll, entry)
    entry = re.sub(r'\{@scaledice .+?\|.+?\|(.+?)}', get_roll, entry)
    entry = re.sub(r'\{@item (.+?)\|.+?}', get_item_name, entry)
    entry = re.sub(r'\{@skill (.+?)}', get_skill_name, entry)
    entry = re.sub(r'\{@quickref .+?\|.+?|\d+\|\|(.+?)}', get_quick_ref, entry)
    entry = re.sub(r'\{@quickref (.+?)\|\|\d+}', get_quick_ref, entry)
    entry = re.sub(r'\{@status (.+?)(\|\|(.+?))?}', get_status, entry)
    entry = re.sub(r'\{@spell (.+?)}', get_spell, entry)
    entry = re.sub(r'\{@sense (.+?)}', get_sense, entry)
    entry = re.sub(r'\{@filter (.+?)(\|.+?)?}', get_filter, entry)
    entry = re.sub(r'\{@creature (.+?)(\|.+?)?}', get_filter, entry)
    entry = re.sub(r'\{@book school of magic\|PHB\|10\|The Schools of Magic}', 'school of magic', entry)
    entry = re.sub(r'\{@book jump distance\|phb\|8\|Jumping}', 'jump distance', entry)
    entry = re.sub(r'\{@action (.+?)}', get_action, entry)
    entry = re.sub(r'\{@note Additional \{@filter animal form choices\|bestiary\|Miscellaneous=Familiar} may be available at the DM\'s discretion\.}', 'Additional animal form choices may be available at the DM\'s discretion.', entry)
    entry = re.sub(r'\{@note Additional animal form choices may be available at the DM\'s discretion\.}', 'Additional animal form choices may be available at the DM\'s discretion.', entry)
    entry = re.sub(r'\{@i (.+?)}', make_italics, entry)
    entry = re.sub(r'\{@adventure (.+?)\|.+?\|.+?}', get_adventure, entry)
    entry = re.sub(r'\{@classFeature (.+?)\|Paladin\|PHB\|1}', get_class_feature, entry)


    if '@' in entry:
        raise Exception(f"Entry with '@': {entry}")
    return entry


def transform_entry_list(entries: List[Any]) -> str:
    complete = ''
    for entry in entries:
        if isinstance(entry, str):
            complete += transform_entry(entry)
        elif isinstance(entry, dict):
            if entry['type'] == 'list':
                complete += "[ul]\\n"
                if 'style' in entry:
                    if entry['style'] == 'list-hang-notitle':
                        complete += "[li]"
                        for item in entry['items']:
                            complete += f"[b]{item['name']}.[/b] {transform_entry_list(item['entries'])}\\n"
                        complete += "[/li]"
                    else:
                        raise Exception(f"Unexpected list style: {entry['style']}")
                else:
                    for item in entry['items']:
                        complete += f"[li]{transform_entry(item)}[/li]\\n"
                complete += "[/ul]\\n"
            elif entry['type'] == 'inset':
                complete += f"[small][b]{entry['name']}.[/b] {transform_entry_list(entry['entries'])}[/small]\\n"
            elif entry['type'] == 'entries':
                complete += f"[b]{entry['name']}.[/b] {transform_entry_list(entry['entries'])}\\n"
            elif entry['type'] == 'table':
                complete += "[table]\\n"
                complete += "[tr]"
                for col in entry['colLabels']:
                    complete += f"[th]{col}[/th]"
                complete += "[/tr]\\n"
                for row in entry['rows']:
                    complete += "[tr]"
                    for cell in row:
                        if isinstance(cell, dict):
                            if 'roll' in cell:
                                if 'min' in cell['roll'] and 'max' in cell['roll']:
                                    complete += f"[td]{cell['roll']['min']}-{cell['roll']['max']}[/td]"
                                elif 'exact' in cell['roll']:
                                    complete += f"[td]{cell['roll']['exact']}[/td]"
                                else:
                                    raise Exception(f"Unexpected roll type: {cell['roll']}")
                            else:
                                raise Exception(f"Unexpected cell type: {cell}")
                        elif isinstance(cell, str):
                            complete += f"[td]{cell}[/td]"
                        else:
                            raise Exception(f"Unexpected cell type: {type(cell)}")
                    complete += "[/tr]\\n"
                complete += "[/table]\\n\\n"
            elif entry['type'] == 'quote':
                complete += f"[quote]{transform_entry_list(entry['entries'])}|{entry['by']}[/quote]\\n"
            else:
                raise Exception(f"Unexpected entry type: {entry['type']}")
        else:
            raise Exception(f"Unexpected entry type: {type(entry)}")
    return complete.strip()


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
    'entries',
    'damageInflict',
    'conditionInflict',
    'classes',
    'savingThrow',
    'scalingLevelDice',
    'spellAttack',
    'entriesHigherLevel',
    'meta',
    # Unused keys
    'miscTags',
    'areaTags',
    'races',
    'optionalfeatures',
    'backgrounds',
    'feats',
    'otherSources',
    'additionalSources',
    'affectsCreatureType',
    'damageResist',
    'hasFluffImages',
    'abilityCheck',
    'hasFluff',
    'conditionImmune',
    'damageVulnerable',
    'damageImmune',
]


def update(entity: dict) -> str:
    has_unexpected_keys = False
    for key in entity:
        if key not in expected_list_keys and not key.startswith('_'):
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
        if isinstance(components['m'], dict):
            material = components['m']['text']
        elif isinstance(components['m'], str):
            material = components['m']
        else:
            raise Exception(f"Unexpected material type: {type(components['m'])} found in entity: {entity['name']}")

    duration_source = entity['duration']

    durations = list()
    for d in duration_source:
        if d['type'] == 'instant':
            durations.append('Instantaneous')
        elif d['type'] == 'timed':
            tmp = f"{d['duration']['amount']} {d['duration']['type']}"
            if 'concentration' in d:
                tmp = f"Concentration, {tmp}"
            durations.append(tmp)
        elif d['type'] == 'permanent':
            durations.append('Permanent')
        elif d['type'] == 'special':
            durations.append('Special')
        else:
            raise Exception(f"Unexpected duration type: {d['type']} found in entity: {entity['name']}")
    duration = ', '.join(durations)

    range_source = entity['range']
    if range_source['type'] == 'radius':
        if range_source['distance']['type'] == 'feet':
            range_value = f" Self ({range_source['distance']['amount'] // 5}-square radius)"
        elif range_source['distance']['type'] == 'miles':
            range_value = f" Self ({range_source['distance']['amount'] * 1.5} km radius)"
        else:
            raise Exception(
                f"Unexpected range distance type: {range_source['distance']['type']} found in entity: {entity['name']}")
    elif range_source['type'] == 'point':
        if range_source['distance']['type'] == 'feet':
            range_value = f"{range_source['distance']['amount'] // 5} sq."
        elif range_source['distance']['type'] == 'miles':
            range_value = f"{range_source['distance']['amount'] * 1.5} km"
        elif range_source['distance']['type'] == 'touch':
            range_value = 'Touch'
        elif range_source['distance']['type'] == 'self':
            range_value = 'Self'
        elif range_source['distance']['type'] == 'sight':
            range_value = 'Sight'
        elif range_source['distance']['type'] == 'unlimited':
            range_value = 'Unlimited'
        else:
            raise Exception(
                f"Unexpected range distance type: {range_source['distance']['type']} found in entity: {entity['name']}")
    elif range_source['type'] == 'cone':
        if range_source['distance']['type'] == 'feet':
            range_value = f"Self ({range_source['distance']['amount'] // 5}-square cone)"
        else:
            raise Exception(
                f"Unexpected range distance type: {range_source['distance']['type']} found in entity: {entity['name']}")
    elif range_source['type'] == 'line':
        if range_source['distance']['type'] == 'feet':
            range_value = f"Self ({range_source['distance']['amount'] // 5}-square line)"
        else:
            raise Exception(
                f"Unexpected range distance type: {range_source['distance']['type']} found in entity: {entity['name']}")
    elif range_source['type'] == 'special':
        range_value = 'Special'
    elif range_source['type'] == 'hemisphere':
        if range_source['distance']['type'] == 'feet':
            range_value = f"Self ({range_source['distance']['amount'] // 5}-square-radius hemisphere)"
        else:
            raise Exception(
                f"Unexpected range distance type: {range_source['distance']['type']} found in entity: {entity['name']}")
    elif range_source['type'] == 'cube':
        if range_source['distance']['type'] == 'feet':
            range_value = f"Self ({range_source['distance']['amount'] // 5}-square cube)"
        else:
            raise Exception(
                f"Unexpected range distance type: {range_source['distance']['type']} found in entity: {entity['name']}")
    elif range_source['type'] == 'sphere':
        if range_source['distance']['type'] == 'feet':
            range_value = f"Self ({range_source['distance']['amount'] // 5}-square-radius sphere)"
        else:
            raise Exception(
                f"Unexpected range distance type: {range_source['distance']['type']} found in entity: {entity['name']}")
    else:
        raise Exception(f"Unexpected range type: {range_source['type']} found in entity: {entity['name']}")

    spell_classes = list()
    if 'classes' in entity:
        classes = entity['classes']
        if 'fromClassList' in classes:
            for cl in classes['fromClassList']:
                spell_classes.append(cl['name'])

    if 'scalingLevelDice' in entity:
        higher_levels = transform_entry(entity['entries'][-1])
        description = transform_entry_list(entity['entries'][:-1])
    else:
        higher_levels = ''
        description = transform_entry_list(entity['entries'])

    if 'entriesHigherLevel' in entity:
        if len(entity['entriesHigherLevel']):
            if higher_levels:
                raise Exception("Both entriesHigherLevel and scalingLevelDice found")
            higher_levels = transform_entry_list(entity['entriesHigherLevel'][0]['entries'])

    attack_values = list()
    if 'savingThrow' in entity:
        attack_values.extend(map_saving_throws_to_texts(entity['savingThrow']))
    elif 'spellAttack' in entity:
        attack_values.extend([map_spell_attack_to_enum(x) for x in entity['spellAttack']])
    elif 'conditionInflict' in entity:
        attack_values.extend(entity['conditionInflict'])
    attack_value = ', '.join(attack_values)

    time_value = list()
    for time in entity['time']:
        time_value.append(f"{time['number']} {time['unit']}")
    time_value = ', '.join(time_value)

    ritual = False
    if 'meta' in entity:
        if 'ritual' in entity['meta']:
            ritual = entity['meta']['ritual']
        if len(entity['meta']) > 1:
            raise Exception(f"Unexpected meta keys found: {entity['meta']}")
    return f"""name: "{entity['name']}"
spell_level: "{map_spell_to_enum(entity['level'])}"
casting_time: "{time_value}"
range: "{range_value}"
components: "{', '.join(value_components)}"
materials: "{material}"
duration: "{duration}"
school: "{map_spell_school_to_enum(entity['school'])}"
attack: "{attack_value}"
effect: "{', '.join(entity['damageInflict']) if 'damageInflict' in entity else ''}"
higher_levels: "{higher_levels}"
classes: "{', '.join(spell_classes)}"
ritual: "{'1' if ritual else '0'}"
spell_description: "{description}"
source: "{entity['source']}, p. {entity['page']}"
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
