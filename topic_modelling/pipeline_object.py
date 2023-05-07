from abc import ABC, abstractmethod
class PipelineObject(ABC):
   
    @abstractmethod
    def process(self):
        pass
    
    def __init__(self, params):
        self.params = params
        PipelineObject.data = {}
        pass
        
    
    