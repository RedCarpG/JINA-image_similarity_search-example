import os
import sys

import click
import logging
import matplotlib.pyplot as plt
from jina import Flow, Document, DocumentArray

MAX_DOCS = int(os.environ.get("JINA_MAX_DOCS", 10000))
cur_dir = os.path.dirname(os.path.abspath(__file__))

DEFAULT_QUERY_IMAGE = 'data/toy-data/example.jpg'
DEFAULT_QUERY_TEXT = 'example'

def config():
    os.environ.setdefault('JINA_WORKSPACE', os.path.join(cur_dir, 'workspace'))
    os.environ.setdefault('JINA_WORKSPACE_MOUNT',
                          f'{os.environ.get("JINA_WORKSPACE")}:/workspace/workspace')
    os.environ.setdefault('JINA_LOG_LEVEL', 'INFO')
    os.environ.setdefault('JINA_PORT', str(12345))

def index(data_set, num_docs, request_size):
    flow = Flow().load_config('flows/flow-index.yml')
    with flow:
        flow.post(on='/index',
                  inputs=input_index_data(num_docs, request_size, data_set),
                  request_size=request_size,
                  show_progress=True)

def index_restful():
    flow = Flow().load_config('flows/flow-index.yml', override_with={'protocol': 'http'})
    with flow:
        flow.block()

def query(query_image, query_text):
    flow = Flow().load_config('flows/flow-query.yml')
    with flow:
        img_uri = query_image
        text_doc = Document(text=query_text,
                            modality='text')
        image_doc = Document(uri=img_uri,
                             modality='image')
        import time
        start = time.time()
        result_text = flow.post(on='/search', inputs=text_doc,
                                return_results=True)
        result_image = flow.post(on='/search', inputs=image_doc,
                                 return_results=True)
        print(f'Request duration: {time.time() - start}')
        check_query_result(result_text[0].docs[0], result_image[0].docs[0], img_uri)

def query_restful():
    flow = Flow(cors=True).load_config('flows/flow-query.yml')
    flow.rest_api = True
    flow.protocol = 'http'
    with flow:
        flow.block()


@click.command()
@click.option('--task', '-t', type=click.Choice(['index', 'index_restful', 'query', 'query_restful']), default='index')
@click.option("--num_docs", "-n", default=MAX_DOCS)
@click.option('--request_size', '-s', default=16)
@click.option('--data_set', '-d', type=click.Choice(['f30k', 'f8k', 'toy-data'], case_sensitive=False), default='toy-data')
@click.option('--query-image', '-i', type=str, default=DEFAULT_QUERY_IMAGE)
@click.option('--query-text', '-i', type=str, default=DEFAULT_QUERY_TEXT)

def main(task, num_docs, request_size, data_set, query_image, query_text):
    config()
    workspace = os.environ['JINA_WORKSPACE']
    logger = logging.getLogger('example0-image-search')

    if 'index' in task:
        if os.path.exists(workspace):
            logger.error(
                f'\n +------------------------------------------------------------------------------------+ \
                    \n |                                   🤖🤖🤖                                           | \
                    \n | The directory {workspace} already exists. Please remove it before indexing again.  | \
                    \n |                                   🤖🤖🤖                                           | \
                    \n +------------------------------------------------------------------------------------+'
            )
            sys.exit(1)
    if 'query' in task:
        if not os.path.exists(workspace):
            logger.error(f'The directory {workspace} does not exist. Please index first via `python app.py -t index`')
            sys.exit(1)

    if task == 'index':
        index(data_set, num_docs, request_size)
    elif task == 'index_restful':
        index_restful()
    elif task == 'query':
        query(query_image, query_text)
    elif task == 'query_restful':
        query_restful()


if __name__ == '__main__':
    main()
