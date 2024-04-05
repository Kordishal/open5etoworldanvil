import os

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

    category = client.category.get('0b893d6d-21c1-43b3-9305-e363bf904ec3', -1)  # backgrounds

    existing_articles = client.world.articles(world['id'], category['id'])
    for article in existing_articles:
        client.article.delete(article['id'])
