from jina import Executor, requests, Document, DocumentArray
import numpy as np
from PIL import Image
from jina.logging.logger import JinaLogger

class ImageUriLoader(Executor):
    """ Load Image data from uri """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = JinaLogger(self.__class__.__name__)

    def _loader(self, uri):

        img = Image.open(uri)
        
        document_img = Document(blob=np.asarray(img),
                                modality = 'image',
                                mime_type = 'image/' + img.format.lower(),

                                tags = {
                                    'mode': img.mode,
                                    'shape': { 
                                        'height': img.size[0],
                                        'width': img.size[1]
                                        }
                                    }
                                )
        return document_img

    @requests(on='/index')
    def index_directory(self, docs: DocumentArray, parameters: dict, **kwargs):
        docs = DocumentArray(list(filter(lambda doc: doc.modality=='image', docs)))

        if not docs:
            return DocumentArray([])

        for doc in docs:
            
            _doc = self._loader(doc.uri)
            doc.update(_doc)

        return docs

    @requests(on='/search')
    def get_url(self, parameters: dict, **kwargs):
        img_path = parameters.setdefault('img_path', 'data/toy_data/example.jpg')
        
        self.logger.info(f"Load query image file: {img_path}")

        img = Image.open(img_path)
    
        document_img = Document(blob=np.asarray(img),
                                uri = img_path,
                                modality = 'image',
                                mime_type = 'image/' + img.format.lower(),

                                tags = {
                                    'mode': img.mode,
                                    'shape': { 
                                        'height': img.size[0],
                                        'width': img.size[1]
                                        },
                                    'name': img_path,
                                    'path': img_path,
                                    }
                                )

        docs = DocumentArray([document_img])

        return docs
