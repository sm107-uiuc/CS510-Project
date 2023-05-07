

class Constants:
    initialized = False
    instance = None
    def __init__(self):
        self.data = {}
        pass
    
    @classmethod
    def getInstance(cls):
        
        if not Constants.initialized:
            Constants.instance = Constants()
            Constants.initialized = True
        return Constants.instance
    
    
    def set_data(self, key, value):
        self.instance.data[key] = value
    
    def get_data(self, key):
        return self.instance.data.get(key,None)
    
    