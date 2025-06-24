from weaviate.classes.config import Configure, Property, DataType, Tokenization
from weaviate import WeaviateClient
from config import *
import asyncio



def get_collection(collection_name):
    return dbclient.collections.get(collection_name)


def get_data_count(collection_name):
    collection = get_collection(collection_name)
    result = collection.aggregate.over_all(
        total_count=True
    )
    return result.total_count







# https://weaviate.io/developers/weaviate/client-libraries/python

if __name__ == '__main__':
    try:
        if dbclient.collections.exists(DB_DOC_COLLECTION_NAME):  
            dbclient.collections.delete(DB_DOC_COLLECTION_NAME)  
        dbclient.collections.create(
            DB_DOC_COLLECTION_NAME,
            # vectorizer_config=Configure.Vectorizer.text2vec_transformers(),
            # vector_index_config=Configure.VectorIndex.hnsw(),
            vectorizer_config= [
                Configure.NamedVectors.text2vec_transformers(
                    name="title",
                    source_properties=["title"],
                ),
                Configure.NamedVectors.text2vec_transformers(
                    name="abstract",
                    source_properties=["abstract"],
                )
            ],
            # vector_index_config=Configure.VectorIndex.flat(),  
            # vector_index_config=Configure.VectorIndex.dynamic(),  
            
            # generative_config=Configure.Generative.aws(
            #     region="us-east-1",
            #     service="sagemaker",
            #     endpoint="<custom_sagemaker_url>"
            # )
            properties=[
                Property(
                    name="abstract",
                    data_type=DataType.TEXT,
                    skip_vectorization=False,
                    vectorize_property_name = False,
                    # vectorizer="text2vec-transformers",
                    # tokenization=Tokenization.LOWERCASE,    https://weaviate.io/developers/weaviate/config-refs/schema#tokenization
                ),
                Property(
                    name="title", 
                    data_type=DataType.TEXT,
                    skip_vectorization=True,
                    vectorize_property_name = False,
                ),
                Property(
                    name="url", 
                    data_type=DataType.TEXT,
                    skip_vectorization=True,
                    vectorize_property_name = False,
                ),
                Property(
                    name="uid", 
                    data_type=DataType.TEXT,
                    skip_vectorization=True,
                    vectorize_property_name = False,
                ),
                Property(
                    name="conference", 
                    data_type=DataType.TEXT,
                    skip_vectorization=True,
                    vectorize_property_name = False,
                ),
                Property(
                    name="decision", 
                    data_type=DataType.TEXT,
                    skip_vectorization=True,
                    vectorize_property_name = False,
                ),
                Property(
                    name="authors", 
                    data_type=DataType.TEXT_ARRAY,
                    skip_vectorization=True,
                    vectorize_property_name = False,
                ),
            ]
        )
        print(get_collection(DB_DOC_COLLECTION_NAME))
    except Exception as e:
        print('⛔ ERROR:', e) 
    finally:
        dbclient.close()