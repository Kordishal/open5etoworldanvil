import os
import requests

from pywaclient.api import BoromirApiClient

if __name__ == '__main__':
    client = BoromirApiClient(
        name='open5e to world anvil client',
        url='https://open5e',
        version='1.0.0',
        application_key=os.getenv('APPLICATION_KEY'),
        authentication_token=os.getenv('AUTHENTICATION_TOKEN')
    )

    world = client.world.get('eca3a195-890f-48ad-83c7-5d806add75c8', -1)


    api_response = requests.get('https://api.open5e.com/v1/monsters/')
    results = api_response.json()['results']
    statblock_folders = client.world.statblock_folders(world_id=world['id'])

    has_folder = False
    folder_id = None
    for statblock_folder in statblock_folders:
        if statblock_folder['title'] == 'Monsters':
            has_folder = True
            folder_id = statblock_folder['id']

    if not has_folder:
        folder = client.block_folder.put({
            'title': 'Monsters', 'world': {
                'id': world['id']
            }})
        folder_id = folder['id']

    print(folder_id)