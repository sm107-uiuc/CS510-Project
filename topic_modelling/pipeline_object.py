from abc import ABC, abstractmethod
class PipelineObject(ABC):
   
    @abstractmethod
    def process(self):
        pass
    
    def __init__(self, params):
        self.params = params
        pass
    
    @staticmethod
    def load_df(data_frame):
        PipelineObject.df = data_frame
    @staticmethod 
    def get_df():
        return PipelineObject.df
    
    @staticmethod
    def load_vocab(vocab):
        PipelineObject.vocab = vocab
    @staticmethod 
    def get_vocab():
        return PipelineObject.vocab
    
    