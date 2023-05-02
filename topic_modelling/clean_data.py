from .pipeline_object import PipelineObject
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, CountVectorizer, StopWordsRemover
from pyspark.sql.functions import *

class CleanData(PipelineObject):
    def __init__(self, params):
        super().__init__(params)
        self.params = params
        pass
    def process(self):
        super().process()
        df = PipelineObject.get_df()
        tokenizer = Tokenizer(inputCol="all_paragraphs", outputCol="words")
        wordsData = tokenizer.transform(df)
        
        remover = StopWordsRemover(inputCol="words", outputCol="filtered")
        filtered = remover.transform(wordsData)
        cv = CountVectorizer(inputCol="filtered", outputCol="rawFeatures"
                             , vocabSize=self.params['vocab_size']
                             , minDF=self.params['min_df']
                             , maxDF=self.params['max_df'])
        cvmodel = cv.fit(filtered)
        vocab = cvmodel.vocabulary
        PipelineObject.load_vocab(vocab)
        featurizedData = cvmodel.transform(filtered)
        
        idf = IDF(inputCol="rawFeatures", outputCol="features")
        idfModel = idf.fit(featurizedData)
        rescaledData = idfModel.transform(featurizedData)
        rescaledData = rescaledData.withColumn('stringFeatures', rescaledData.rawFeatures.cast(StringType()))
        rescaledData = rescaledData.withColumn('coltext', concat_ws(',', 'filtered' ))
        PipelineObject.load_df(rescaledData)
        print("Data cleaned successfully")