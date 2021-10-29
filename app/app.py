import os
import sys

import click
import logging

from .config import *
from flows import *

@click.command()
@click.option('--task', '-t', type=click.Choice(['index', 'index_restful', 'query', 'query_restful']), default='index')
@click.option("--num_docs", "-n", default=MAX_DOCS)
@click.option('--request_size', '-s', default=16)
@click.option('--data_set', '-d', type=click.Choice(['images', 'toy_data'], case_sensitive=False), default='toy_data')
@click.option('--query-image', '-i', type=str, default=DEFAULT_QUERY_IMAGE)
@click.option('--query-text', '-i', type=str, default=DEFAULT_QUERY_TEXT)

def app(task, num_docs, request_size, data_set, query_image, query_text):
    config_env()
    workspace = os.environ['JINA_WORKSPACE']
    logger = logging.getLogger('example-image-search')

    # if 'index' in task:
    #     if os.path.exists(workspace):
            
    #         logger.error(
    #             f'\n +------------------------------------------------------------------------------------+ \
    #                 \n |                                   🤖🤖🤖                                           | \
    #                 \n | The directory {workspace} already exists. Please remove it before indexing again.  | \
    #                 \n |                                   🤖🤖🤖                                           | \
    #                 \n +------------------------------------------------------------------------------------+'
    #         )
    #         sys.exit(1)
    if 'query' in task:
        if not os.path.exists(workspace):
            logger.error(f'The directory {workspace} does not exist. Please index first via `python main.py -t index`')
            sys.exit(1)

    if task == 'index':
        index("data/"+data_set, num_docs, request_size)
    elif task == 'index_restful':
        index_restful()
    elif task == 'query':
        query(query_image)
    elif task == 'query_restful':
        query_restful()
