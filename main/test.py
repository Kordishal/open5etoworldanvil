import json
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

    # article = client.article.get('fd5df128-8f5c-4e3b-a5e1-63e62c18eb2d', 3) # Acolyte
    # article = client.article.get('a12a257a-157e-43d6-b51a-372effdddf97', 3) # Artisan

   #  with open('data/output.json', 'w') as fp:
   #     json.dump(article, fp, indent='    ')


    block = client.block.get('1393572', 2)
    print(block)

    client.block.patch('1393572', {
        'title': 'Test Block'
    })