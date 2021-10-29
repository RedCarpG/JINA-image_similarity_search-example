from genericpath import exists
import os
import sys

import click
import logging
from jina.logging.logger import JinaLogger
from .config import *
from flows import *
import shutil

@click.command()
@click.option('--task', '-t', type=click.Choice(['index', 'index_restful', 'query', 'query_restful']), default='index')
@click.option("--num_docs", "-n", default=MAX_DOCS)
@click.option('--request_size', '-s', default=16)
@click.option('--data_set', '-d', type=click.Choice(['images', 'toy_data'], case_sensitive=False), default='toy_data')
@click.option('--query-image', '-i', type=str, default=DEFAULT_QUERY_IMAGE)
@click.option('--force', '-f', is_flag=True)
def app(task, num_docs, request_size, data_set, query_image, force):
    config_env()
    workspace = os.environ['JINA_WORKSPACE']
    logger = JinaLogger('app')

    if 'index' in task:
        if os.path.exists(workspace):
            if not force:
                logger.error(f"\n------------------------------------------------------------------------"
                             f"\n\t🤖🤖🤖 Workspace {workspace} already exists"
                             f"\n\tuse -f to force clean workspace"
                             f"\n------------------------------------------------------------------------")
                sys.exit(1)
            else:
                logger.info(
                    f"\n------------------------------------------------------------------------"
                    f"\n\t🤖🤖🤖 Cleaning workspace {workspace}"
                    f"\n------------------------------------------------------------------------")
                try:
                    shutil.rmtree(workspace)
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))

    if 'query' in task:
        if not os.path.exists(workspace):
            logger.error(f"\n------------------------------------------------------------------------"
                            f"\n\t🤖🤖🤖 The directory {workspace} does not exist"
                            f"\n\tPlease index first via `python main.py -t index`"
                            f"\n------------------------------------------------------------------------")
            sys.exit(1)
            
    if task == 'index':
        data_path = "data/"+data_set
        logger.info(
            f"\n------------------------------------------------------------------------"
            f"\n\t🤖🤖🤖 Start indexing in data {data_path}"
            f"\n------------------------------------------------------------------------")
        index(data_path, num_docs, request_size)
    elif task == 'index_restful':
        index_restful()
    elif task == 'query':
        logger.info(
            f"\n------------------------------------------------------------------------"
            f"\n\t🤖🤖🤖 Start querying data with {query_image}"
            f"\n------------------------------------------------------------------------")
        query(query_image)
    elif task == 'query_restful':
        query_restful()
