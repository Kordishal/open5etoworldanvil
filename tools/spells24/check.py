import json
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

    block = client.block.get('1483629', 2)

    print(json.dumps(block, indent=4))

