import csv
import os

from pywaclient.api import BoromirApiClient

if __name__ == '__main__':

    client = BoromirApiClient(
        name='open5e to world anvil client',
        url='local script',
        version='1.0.0',
        application_key=os.getenv('APPLICATION_KEY'),
        authentication_token=os.getenv('AUTHENTICATION_TOKEN')
    )

    for f in client.world.statblock_folders(world_id='cd8d7774-14cd-4451-baa2-3c0d8c44cfe7'):
        if f['title'] == 'Monsters - Plants':
            for s in client.block_folder.blocks(f['id']):
                print(s['title'])
                client.block.delete(s['id'])
