from jina import Flow, Document, DocumentArray
import os
from jina.logging.logger import JinaLogger

def _check_query_result(result_response):
    logger = JinaLogger("query_result")

    # Find matches for each query doc
    for doc in result_response[0].docs:
    
        if doc.matches:
            match_info = ""
            for m in doc.matches:
                match_info += f'\n\t@ IMAGE: {m.tags["name"]: <15};  SCORE: {1 - m.scores["cosine"].value:.4f};  PATH: {m.tags["path"]: <25}'
            logger.info(
                f"\n==========================="
                f"\n- Image: {doc.tags__path}"
                f"\n- Find Matches: "
                f"{match_info}"
                f"\n===========================")
        else:
            logger.info(
                f"\n==========================="
                f"\n- Image: {doc.tags__path}"
                f"\n- Match didn't find"
                f"\n===========================")

def _index_data_generator(dir, num_docs=None):
    logger = JinaLogger('index_generator')

    img_extensions = ['.png', '.jpg']
    txt_extensions = ['.txt']

    files = os.listdir(dir) 

    for i, file in enumerate(files):
        
        file_name, file_extension = os.path.splitext(file)   

        if file_extension in img_extensions:
            modality = 'image'
        elif file_extension in txt_extensions:
            modality = 'text'
        else: 
            logger.warning(f'Not supported extension: {file}')
            continue

        file_path = os.path.join(dir, file)
        doc = Document(id = i, 
                        uri = file_path,
                        modality = modality,
                        tags = {
                            'name': file_name,
                            'path': file_path,
                            'extension': file_extension,
                            'index': i,
                            }
                        )

        yield doc

        if num_docs and (i + 1) >= num_docs:
            break

def index(data_set, num_docs, request_size):
    flow = Flow().load_config('index.yml')

    parameters = {'img_dir': data_set,
                  'num_docs': num_docs}

    with flow:
        flow.post(on='/index',
                  inputs=_index_data_generator(data_set, num_docs=num_docs),
                  parameters=parameters,
                  request_size=request_size,
                  show_progress=True)

def index_restful():
    flow = Flow().load_config('index.yml', override_with={'protocol': 'http'})
    with flow:
        flow.block()

def query(query_image):
    logger = JinaLogger("query_flow")

    flow = Flow().load_config('query.yml')
    with flow:
        parameters = {'img_path': query_image}

        import time
        start = time.time()
        result_response = flow.post(on='/search', 
                                 parameters=parameters,
                                 return_results=True)
        logger.info(f'Request duration: {time.time() - start}')
        _check_query_result(result_response)

def query_restful():
    flow = Flow(cors=True).load_config('query.yml')
    flow.rest_api = True
    flow.protocol = 'http'
    with flow:
        flow.block()
