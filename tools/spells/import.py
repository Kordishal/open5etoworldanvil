import csv
import json
import os

from pywaclient.api import BoromirApiClient

from tools.shared.folders import create_folders
from tools.spells.util import map_spell_level_to_folder, update


def main():
    client = BoromirApiClient(
        name='open5e to world anvil client',
        url='local script',
        version='1.0.0',
        application_key=os.getenv('APPLICATION_KEY'),
        authentication_token=os.getenv('AUTHENTICATION_TOKEN')
    )

    world = client.world.get('cd8d7774-14cd-4451-baa2-3c0d8c44cfe7', -1)

    folders = create_folders(client, world['id'], ['Spells - Cantrips', 'Spells - 1st Level', 'Spells - 2nd Level', 'Spells - 3rd Level', 'Spells - 4th Level', 'Spells - 5th Level', 'Spells - 6th Level', 'Spells - 7th Level', 'Spells - 8th Level', 'Spells - 9th Level'])

    existing_blocks = dict()
    if os.path.exists('data/blocks.csv'):
        with open('data/blocks.csv', 'r') as b:
            data = csv.reader(b)
            for row in data:
                existing_blocks[row[0]] = row[1]

    with open('data/spells.json', 'r') as f:
        data = json.load(f)
        written_rows = list()

        for entity in data:
            if entity['name'] in existing_blocks:
                print("updating block for", entity['name'])
                textdata = update(entity)
                print(textdata)
                block = client.block.patch(existing_blocks[entity['name']], {
                    'state': 'private',
                    'folder': {
                        'id': folders[map_spell_level_to_folder(entity['level'])]
                    },
                    'isShared': False,
                    'tags': f"{entity['source']}",
                    'textualdata': f"name: {entity['name']}",
                })
            else:
                print("creating block for", entity['name'])
                block = client.block.put({
                    'title': entity['name'],
                    'folder': {
                        'id': folders[map_spell_level_to_folder(entity['level'])]
                    },
                    'template': {
                        'id': 3000  # D&D 5e Statblock Spell Template
                    },
                    'RPGSRD': {
                        'id': 1  # D&D 5e
                    },
                    'dataParser': 'yaml',
                    'textualdata': f"name: {entity['name']}",
                    'world': {
                        'id': world['id']
                    }
                })
            written_rows.append([entity['name'], block['id'], block['url']])

        with open('data/blocks.csv', 'w') as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(written_rows)


if __name__ == '__main__':
    main()