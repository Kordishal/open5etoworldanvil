import os
import re
from enum import Enum
from html.parser import HTMLParser
from typing import Dict, Any, Iterable

import markdown
import requests

from pywaclient.api import BoromirApiClient

documents = {
    'https://api-beta.open5e.com/v2/documents/a5esrd/': 'A5E-SRD',
    'https://api-beta.open5e.com/v2/documents/srd/': 'WOTC-SRD',
    'https://api-beta.open5e.com/v2/documents/taldorei/': 'TAL',
    'https://api-beta.open5e.com/v2/documents/toh/': 'TOH',

}


class State(Enum):
    UNKNOWN = 0
    INITIALIZING = 1
    ADD_TEXT = 2
    IGNORE = 3


class BackgroundSuggestedCharacteristicsHtmlParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.content = ''
        self.state = State.INITIALIZING

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.state = State.ADD_TEXT
        elif tag == 'strong':
            self.content += "[b]"
            self.state = State.ADD_TEXT
        elif tag == 'em':
            self.content += "[i]"
            self.state = State.ADD_TEXT
        elif tag == 'table':
            self.content += "[table]\n"
        elif tag == 'thead':
            pass
        elif tag == 'tbody':
            pass
        elif tag == 'tr':
            self.content += "  [tr]\n"
        elif tag == 'th':
            self.content += "    [th]"
            self.state = State.ADD_TEXT
        elif tag == 'td':
            self.content += "    [td]"
            self.state = State.ADD_TEXT
        elif tag == 'ol':
            self.content += "[ol]\n"
            self.state = State.IGNORE
        elif tag == 'ul':
            self.content += "[ul]\n"
            self.state = State.IGNORE
        elif tag == 'li':
            self.content += "  [li]"
            self.state = State.ADD_TEXT
        elif tag == 'h3':
            self.content += "[h3]"
            self.state = State.ADD_TEXT
        elif tag == 'pre':
            pass
        elif tag == 'code':
            self.state = State.ADD_TEXT
        else:
            print("Opening Tag: ", tag)
            self.state = State.UNKNOWN

    def handle_endtag(self, tag):
        if tag == 'p':
            self.state = State.IGNORE
            self.content += "\n\n"
        elif tag == 'strong':
            self.content += "[/b]"
            self.state = State.ADD_TEXT
        elif tag == 'em':
            self.content += "[/i]"
            self.state = State.ADD_TEXT
        elif tag == 'table':
            self.content += "[/table]\n"
        elif tag == 'thead':
            pass
        elif tag == 'tbody':
            pass
        elif tag == 'tr':
            self.content += "  [/tr]\n"
        elif tag == 'th':
            self.content += "[/th]\n"
            self.state = State.IGNORE
        elif tag == 'td':
            self.content += "[/td]\n"
            self.state = State.IGNORE
        elif tag == 'ol':
            self.content += "[/ol]\n"
            self.state = State.IGNORE
        elif tag == 'ul':
            self.content += "[/ul]\n"
            self.state = State.IGNORE
        elif tag == 'li':
            self.content += "[/li]\n"
            self.state = State.IGNORE
        elif tag == 'h3':
            self.content += "[/h3]\n"
            self.state = State.ADD_TEXT
        elif tag == 'pre':
            pass
        elif tag == 'code':
            self.state = State.ADD_TEXT
        else:
            print("Closing Tag: ", tag)
            self.state = State.UNKNOWN

    def handle_data(self, data):
        if self.state == State.ADD_TEXT:
            matched = re.match(r'd(\d)$', data)
            if matched is not None:
                self.content += f"[roll:1d{matched.group(1)}]"
            else:
                self.content += data
        elif self.state == State.IGNORE or self.state == State.INITIALIZING:
            pass
        elif self.state == State.UNKNOWN:
            print("Content for unknown tag: " + data)


def to_bbcode(text: str) -> str:
    html = markdown.markdown(text, extensions=['tables'])
    parser = BackgroundSuggestedCharacteristicsHtmlParser()
    parser.feed(html)
    return parser.content


def get_content(world_id: str, category_id: str) -> Iterable[Dict[str, Any]]:
    backgrounds = requests.get('https://api-beta.open5e.com/v2/backgrounds/')
    results = backgrounds.json()['results']

    for result in results:
        main_content = dict()
        sidebar_content = dict()
        for benefit in result['benefits']:
            if benefit['type'] in ['language', 'skill_proficiency', 'equipment', 'ability_score', 'ability_score_increase',
                                   'tool_proficiency']:
                sidebar_content[benefit['type']] = f"--{benefit['name']}::{benefit['desc']}--"
            elif benefit['type'] in ['feature', 'suggested_characteristics', 'adventures_and_advancement',
                                     'adventures-and-advancement', 'connection_and_memento']:
                main_content[benefit['type']] = f"[h1]{benefit['name']}[/h1]\n{to_bbcode(benefit['desc'])}"
            else:
                print(benefit)

        yield {
            'title': result['name'] + " | " + documents[result['document']],
            'templateType': 'article',
            'state': 'public',
            'isDraft': False,
            'isWip': False,
            'slug': result['key'],
            'content': to_bbcode(result['desc']).strip() + '\n'.join(
                [value for key, value in sorted(main_content.items())]),
            'sidepanelcontenttop': "\n".join([value for key, value in sorted(sidebar_content.items())]),
            'world': {
                'id': world_id
            },
            'category': {
                'id': category_id
            }
        }


if __name__ == '__main__':
    client = BoromirApiClient(
        name='open5e to world anvil client',
        url='local script',
        version='1.0.0',
        application_key=os.getenv('APPLICATION_KEY'),
        authentication_token=os.getenv('AUTHENTICATION_TOKEN')
    )

    world = client.world.get('eca3a195-890f-48ad-83c7-5d806add75c8', -1)

    category = client.category.get('0b893d6d-21c1-43b3-9305-e363bf904ec3', -1)

    existing_articles_map = dict()
    existing_articles = client.world.articles(world['id'], category['id'])
    for article in existing_articles:
        existing_articles_map[article['title']] = article['id']

    previous_article = None
    for item in get_content(world['id'], category['id']):
        if item['title'] not in existing_articles_map:
            client.article.put(item)
        else:
            del item['templateType']

            if previous_article is not None:
                item['articlePrevious'] = previous_article
            client.article.patch(existing_articles_map[item['title']], item)

            if previous_article is not None:
                next_article = existing_articles_map[item['title']]
                client.article.patch(previous_article, {
                    'articleNext': next_article
                })

            previous_article = existing_articles_map[item['title']]


def create_statblock_folder():
    statblock_folders = client.world.statblock_folders(world_id=world['id'])
    has_background = False
    background_folder_id = None
    for statblock_folder in statblock_folders:
        if statblock_folder['title'] == 'Backgrounds':
            has_background = True
            background_folder_id = statblock_folder['id']

    if not has_background:
        folder = client.block_folder.put({
            'title': 'Backgrounds', 'world': {
                'id': world['id']
            }})
        background_folder_id = folder['id']

    print(background_folder_id)
