from pywaclient.api import BoromirApiClient


def create_folders(c: BoromirApiClient, world_id: str, folder_names: list):
    folders = dict()
    for folder in c.world.statblock_folders(world_id=world_id):
        if folder['title'] in folder_names:
            folders[folder['title']] = folder['id']

    for folder_name in folder_names:
        if folder_name not in folders:
            folder = c.block_folder.put({
                'title': folder_name,
                'world': {
                    'id': world_id
                }
            })
            folders[folder_name] = folder['id']

    return folders
