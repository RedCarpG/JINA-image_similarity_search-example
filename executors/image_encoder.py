import numpy as np
from keras.applications.resnet import ResNet50, preprocess_input

from jina import Executor, requests, DocumentArray
from PIL import Image
from jina.logging.logger import JinaLogger

class ImageProcessor(Executor):
    def __init__(self, **kwargs):
        super().__init__()
        self.logger = JinaLogger(self.__class__.__name__)

        self.enable_rescale = True
        self.rescale_height = 224
        self.rescale_width = 224

        # self.enable_normalization = False
        # self.type = 'float32'

    def _preprocess(self, blob) -> np.ndarray:
        
        _img = Image.fromarray(blob)

        if self.enable_rescale:
            _img = _img.resize((self.rescale_width, self.rescale_height))

        _img_blob = np.asarray(_img)
        
        # if self.enable_normalization:
        #     _img_blob = (_img_blob / 255).astype(self.type)
        #     _img_blob = _img_blob.astype('float32')
        
        _img_blob = preprocess_input(_img_blob) # ResNet50 preprocess_input


        return _img_blob
        
    @requests
    def process_img(self, docs: DocumentArray, parameters: dict = None, **kwargs):
        docs = DocumentArray(list(filter(lambda doc: doc.modality=='image', docs)))

        # Filter image mode which is not 'RGB'
        modes, _ = docs.get_attributes_with_docs('tags__mode')
        s_modes = set(modes)
        if len(s_modes) > 1:
            for each_mode in s_modes:
                if each_mode != 'RGB':
                    found_index = np.where(np.array(modes) == each_mode)[0]
                    for i in found_index:
                        self.logger.warning(f"Unsupported image mode: {each_mode}; image: '{docs[int(i)].tags__path}'")
            docs = DocumentArray(list(filter(lambda doc: doc.tags__mode=='RGB', docs)))

        # Process data
        for doc in docs:
            
            doc.blob = self._preprocess(doc.blob)

        return docs

class TfModelEncoder(Executor):
    def __init__(self, **kwargs):
        super().__init__()
        self.image_dim = 224
        self.model = ResNet50(pooling='max', 
                              input_shape=(self.image_dim, self.image_dim, 3),
                              weights='imagenet')

    # def _resize_images(self, tensors):
    #     resized_tensors = []
    #     for t in tensors:
    #         try:
    #             resized_tensors.append(tf.keras.preprocessing.image.smart_resize(t, (self.image_dim, self.image_dim)))
    #         except InvalidArgumentError:
    #             # this can happen if you include empty or other malformed images
    #             pass
    #     return resized_tensors

    @requests
    def encode(self, docs, **kwargs):

        blobs, _ = docs.get_attributes_with_docs('blob')

        # buffers, docs = docs.get_attributes_with_docs('buffer')
        # tensors = [tf.io.decode_image(contents=b, channels=3) for b in buffers]
        # resized_tensors = preprocess_input(np.array(self._resize_images(tensors)))
        
        embeds = self.model.predict(np.stack(blobs))
        for d, b in zip(docs, embeds):
            d.embedding = b
