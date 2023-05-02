from .pipeline_object import PipelineObject
class LoadData(PipelineObject):
    def __init__(self,params):
        self.params = params
        super().__init__(params)
    def process(self):
        super().process()
        spark = self.params['spark']
        self.df = spark.read.format("json").load(self.params['in_path'])
        self.df = self.df.drop_duplicates(['url'])
        print(f"Total documents loaded {self.df.count()}") 
        PipelineObject.load_df(self.df)
        print("Data loaded successfully")