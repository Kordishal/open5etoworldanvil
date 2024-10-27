import csv
import os
import re
from typing import Dict, List, Any
import markdown

from pywaclient.api import BoromirApiClient

from tools.shared.folders import create_folders


def map_spell_level_to_folder(level: int) -> str:
    return {
        0: 'Spells 24 - Cantrips',
        1: 'Spells 24 - 1st Level',
        2: 'Spells 24 - 2nd Level',
        3: 'Spells 24 - 3rd Level',
        4: 'Spells 24 - 4th Level',
        5: 'Spells 24 - 5th Level',
        6: 'Spells 24 - 6th Level',
        7: 'Spells 24 - 7th Level',
        8: 'Spells 24 - 8th Level',
        9: 'Spells 24 - 9th Level'
    }[level]


def map_spell_level_to_input(level: int) -> str:
    return {
        0: 'Cantrip',
        1: '1st',
        2: '2nd',
        3: '3rd',
        4: '4th',
        5: '5th',
        6: '6th',
        7: '7th',
        8: '8th',
        9: '9th'
    }[level]


def map_spell_level_to_tag(level: int) -> str:
    return {
        0: 'Cantrip',
        1: '1st Level',
        2: '2nd Level',
        3: '3rd Level',
        4: '4th Level',
        5: '5th Level',
        6: '6th Level',
        7: '7th Level',
        8: '8th Level',
        9: '9th Level'
    }[level]

def process_line(input_line: str) -> str:
    input_line = input_line.replace('—', '-')

    return (markdown.markdown(input_line)
            .replace('<p>', '')
            .replace('</p>', '')
            .replace('<h5>', '[h5]')
            .replace('</h5>', '[/h5]')
            .replace('<em>', '[i]')
            .replace('</em>', '[/i]')
            .replace('<strong>', '[b]')
            .replace('</strong>', '[/b]')
            .replace('<li>', '[li]')
            .replace('</li>', '[/li]')
            .replace('<ul>', '')
            .replace('</ul>', '').strip())

def parse_spell(lines: List[str]) -> Dict[str, Any]:
    spell = dict()
    spell['title'] = lines[0][4:].strip()
    level_tmp = lines[1].strip('*\n').split(' ')
    if len(level_tmp) == 2:
        spell['level'] = 0
        spell_school = level_tmp[0]
    elif len(level_tmp) == 3:
        spell['level'] = int(level_tmp[1])
        spell_school = level_tmp[2]
    else:
        raise Exception(f'Failed to parse level line: {lines[1]}')

    if not lines[3].startswith('- **Casting Time:**'):
        raise Exception(f'Failed to parse line 3: {lines[3]}')

    if not lines[4].startswith('- **Range:** '):
        raise Exception(f'Failed to parse line 4: {lines[4]}')

    if not lines[5].startswith('- **Components:** '):
        raise Exception(f'Failed to parse line 5: {lines[5]}')

    if not lines[6].startswith('- **Duration:** '):
        raise Exception(f'Failed to parse line 6: {lines[6]}')

    description = ""
    available = ""
    higherlevel = ""

    for line in lines[8:]:
        if line.startswith('**Classes:** '):
            available = line[len('**Classes:** '):]
            break

        if line.startswith("***Using a Higher-Level Spell Slot.*** "):
            higherlevel = line[len("***Using a Higher-Level Spell Slot.*** "):]
        elif line.startswith("***Cantrip Upgrade.*** "):
            higherlevel = line[len("***Cantrip Upgrade.*** "):]
        else:
            description += process_line(line.strip()) + "\n"

    if '|' in description:
        matches = re.findall(r'\|.+?\|\n\n', description, flags=re.S)
        if matches:
            for match in matches:
                match: str = match.strip()
                match_lines = match.split('\n')
                new_table = "[table]"
                line = match_lines[0]
                new_table += '[tr]'
                values = line.split('|')
                for v in values:
                    if v != '':
                        new_table += '[th]' + v.strip() + '[/th]'
                new_table += '[/tr]'

                for line in match_lines[2:]:
                    new_table += '[tr]'
                    values = line.split('|')
                    for v in values:
                        if v != '':
                            new_table += '[td]' + v.strip() + '[/td]'
                    new_table += '[/tr]'
                new_table += "[/table]\n"
                description = description.replace(match, new_table)

    if '[li]' in description:
        description = description.replace("\n\n[li]", "\n\n[ul][li]")
        description = description.replace("[/li]\n\n", "[/li][/ul]\n\n")

    description = description.strip()

    spell["textualdata"] = f"""name: "{spell["title"]}"
level: "{map_spell_level_to_input(spell['level'])}"
casting_time: "{lines[3][20:].strip()}"
rangearea: "{lines[4][13:].strip()}"
components: "{lines[5][18:].strip()}"
duration: "{lines[6][16:].strip()}"
school: "{spell_school.lower()}"
attacksave: ''
damageeffect: ''
description: "{description}"
higherlevel: "{higherlevel}"
available: "{available}"
imageid: ''
source: "Player's Handbook (2024)"
"""
    spell['tags'] = f"{map_spell_level_to_tag(spell['level'])},{spell_school},{','.join([a.strip() for a in available.split(',')])}"
    return spell


def main():
    client = BoromirApiClient(
        name='open5e to world anvil client',
        url='local script',
        version='1.0.0',
        application_key=os.getenv('APPLICATION_KEY'),
        authentication_token=os.getenv('AUTHENTICATION_TOKEN')
    )

    world = client.world.get('cd8d7774-14cd-4451-baa2-3c0d8c44cfe7', -1)

    folders = create_folders(client, world['id'], [
        'Spells 24 - Cantrips',
        'Spells 24 - 1st Level',
        'Spells 24 - 2nd Level',
        'Spells 24 - 3rd Level',
        'Spells 24 - 4th Level',
        'Spells 24 - 5th Level',
        'Spells 24 - 6th Level',
        'Spells 24 - 7th Level',
        'Spells 24 - 8th Level',
        'Spells 24 - 9th Level'])

    existing_blocks = dict()
    if os.path.exists('data/blocks.csv'):
        with open('data/blocks.csv', 'r') as b:
            data = csv.reader(b)
            for row in data:
                existing_blocks[row[0]] = row[1]

    with open('data/phb_24_spells.md', 'r') as f:
        spells = []
        spell_data = None
        for line in f.readlines():
            if line.startswith('#### '):
                if spell_data:
                    spells.append(spell_data)
                spell_data = [line]
            else:
                spell_data.append(line)
        spells.append(spell_data)
        print(f"Number of spells: {len(spells)}")
        for s in spells:
            spell_entity = parse_spell(s)
            spell_entity['state'] = "private"  # let others view the statblock.
            spell_entity['isShared'] = False  # share with community.
            spell_entity['dataParser'] = 'yaml'
            spell_entity['template'] = {
                'id': 17213  # Spell (D&D 5e 2024)
            }
            spell_entity['RPGSRD'] = {
                'id': 739  # D&D 5e 2024
            }
            spell_entity['folder'] = {
                'id': folders[map_spell_level_to_folder(spell_entity['level'])]
            }
            spell_entity['world'] = {
                'id': world['id']
            }
            print(spell_entity)

            #if spell_entity['title'] in existing_blocks:
            #    client.block.patch(existing_blocks[spell_entity['title']], spell_entity)
            #else:
            #    client.block.put(spell_entity)


if __name__ == '__main__':
    main()
