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

    with open('data/blocks.csv', 'r') as f:
        data = csv.reader(f)
        for row in data:
            client.block.delete(row[1])
