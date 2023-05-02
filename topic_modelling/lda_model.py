
from .pipeline_object import PipelineObject
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.ml.clustering import LDA
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.sql.functions import udf
import datetime

class LdaModel(PipelineObject):
    def __init__(self, params):
        super().__init__(params)
        self.params = params
    
    def process(self):
        super().process()
        spark = self.params['spark']
        lda_model = LDA(k=self.params['num_topics'], maxIter=self.params['max_iter'])
        df_new = PipelineObject.get_df()
        model = lda_model.fit(df_new)
        lda_data = model.transform(df_new)
        
        ll = model.logLikelihood(lda_data)
        lp = model.logPerplexity(lda_data)
        print("The lower bound on the log likelihood of the entire corpus: " + str(ll))
        print("The upper bound on perplexity: " + str(lp))
        
        # -------------- Read vocab and map words to topics ---------------- #
        vocab_read_list = PipelineObject.get_vocab()
        vocab_broadcast = spark.sparkContext.broadcast(vocab_read_list)
        topics = model.describeTopics(maxTermsPerTopic = self.params['max_terms_per_topic'])
                
        def map_termID_to_Word(termIndices):
            words = []
            for termID in termIndices:
                words.append(vocab_broadcast.value[termID])
        
            return words
        
        udf_map_termID_to_Word = udf(map_termID_to_Word , ArrayType(StringType()))
        
        ldatopics_mapped = topics.withColumn("topic_desc", udf_map_termID_to_Word(topics.termIndices))
        
        topics_df = ldatopics_mapped.select(col("termweights"), col("topic_desc")).toPandas()
        print(topics_df.head())