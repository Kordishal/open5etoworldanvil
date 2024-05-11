import csv
import json
import os

from pywaclient.api import BoromirApiClient

from tools.monsters.util import update, collect_monster_type


def import_data(file: str, folder_id: str):
    existing_blocks = dict()

    if os.path.exists(f'data/{file}.csv'):
        with open(f'data/{file}.csv', 'r') as b:
            data = csv.reader(b)
            for row in data:
                existing_blocks[row[0]] = row[1]

    with open(f'data/{file}.json', 'r') as f:
        data = json.load(f)
        written_rows = list()
        for entity in data:
            if entity['name'] in existing_blocks:
                print("updating block for", entity['name'])
                textdata = update(entity)
                print(textdata)
                block = client.block.patch(existing_blocks[entity['name']], {
                    'state': 'public',
                    'folderId': folder_id,
                    'folder': {
                        'id': folder_id
                    },
                    'isShared': True,
                    'tags': f"{entity['source']},{collect_monster_type(entity)},CR {entity['cr']}",
                    'textualdata': textdata
                })
            else:
                print("creating block for", entity['name'])
                block = client.block.put({
                    'title': entity['name'],
                    'tags': f'{entity['source']},{collect_monster_type(entity)},CR {entity["cr"]}',
                    'folderId': folder_id,
                    'folder': {
                        'id': folder_id
                    },
                    'isShared': True,
                    'isSRD': False,
                    'template': {
                        'id': 2991  # D&D 5e Statblock Monster Template
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
            with open(f'data/{file}.csv', 'a') as output:
                writer = csv.writer(output, lineterminator='\n')
                writer.writerows(written_rows)


if __name__ == '__main__':
    client = BoromirApiClient(
        name='open5e to world anvil client',
        url='local script',
        version='1.0.0',
        application_key=os.getenv('APPLICATION_KEY'),
        authentication_token=os.getenv('AUTHENTICATION_TOKEN')
    )

    world = client.world.get('cd8d7774-14cd-4451-baa2-3c0d8c44cfe7', -1)
    glory_of_giants_folder = None
    plants_folder = None
    for block_folder in client.world.statblock_folders(world_id=world['id']):
        if block_folder['title'] == 'Monsters - Glory of the Giants':
            glory_of_giants_folder = block_folder['id']
        if block_folder['title'] == 'Monsters - Plants':
            plants_folder = block_folder['id']

    if glory_of_giants_folder is None:
        raise Exception("Folder 'Monsters - Glory of Giants' not found")
    if plants_folder is None:
        raise Exception("Folder 'Monsters - Plants' not found")

    import_data('plants', plants_folder)
