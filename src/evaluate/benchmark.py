import pandas as pd
import weaviate
from tqdm import tqdm
from config import *
from src.db.models import *

def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

def process_results(results):
    return results.objects[0].properties if results.objects else None

def evaluate(df, function):
    correct = 0
    total = len(df)

    for _, row in tqdm(df.iterrows(), total=total):
        gt_uid = row['uid']
        question = row['question']
        
        retrieved = function(question)
        retrieved = process_results(retrieved)
        if retrieved and retrieved['uid'] == gt_uid:
            correct += 1

    accuracy = correct / total
    return accuracy


def KW_Title(query):
    collection = get_collection(DB_DOC_COLLECTION_NAME)
    return collection.query.bm25(
        query=query,
        query_properties=["title"],
        limit=1,
    )

def KW_Abstract(query):
    collection = get_collection(DB_DOC_COLLECTION_NAME)
    return collection.query.bm25(
        query=query,
        query_properties=["abstract"],
        limit=1,
    )

def KW_Both(query):
    collection = get_collection(DB_DOC_COLLECTION_NAME)
    return collection.query.bm25(
        query=query,
        query_properties=["title", "abstract"],
        limit=1,
    )


def Vec_Title(query):
    collection = get_collection(DB_DOC_COLLECTION_NAME)
    return collection.query.hybrid(
        query=query,
        query_properties=[], # Parameters only for keyword search
        target_vector="title",
        # max_vector_distance=0.2,
        limit=1,
        alpha=1, # An alpha of 1 is a pure vector search.
    )


def Vec_Abstract(query):
    collection = get_collection(DB_DOC_COLLECTION_NAME)
    return collection.query.hybrid(
        query=query,
        query_properties=[], # Parameters only for keyword search
        target_vector="abstract",
        # max_vector_distance=0.2,
        limit=1,
        alpha=1, # An alpha of 1 is a pure vector search.
    )

def KW_Title_Vec_Abstract(query):
    collection = get_collection(DB_DOC_COLLECTION_NAME)
    return collection.query.hybrid(
        query=query,
        query_properties=["title"], # Parameters only for keyword search
        target_vector="abstract",
        # max_vector_distance=0.2,
        limit=1,
        alpha=0.5, # An alpha of 1 is a pure vector search.
    )

def KW_Abstract_Vec_Title(query):
    collection = get_collection(DB_DOC_COLLECTION_NAME)
    return collection.query.hybrid(
        query=query,
        query_properties=["abstract"], # Parameters only for keyword search
        target_vector="title",
        # max_vector_distance=0.2,
        limit=1,
        alpha=0.5, # An alpha of 1 is a pure vector search.
    )


def KW_Title_Vec_Title(query):
    collection = get_collection(DB_DOC_COLLECTION_NAME)
    return collection.query.hybrid(
        query=query,
        query_properties=["title"], # Parameters only for keyword search
        target_vector="title",
        # max_vector_distance=0.2,
        limit=1,
        alpha=0.5, # An alpha of 1 is a pure vector search.
    )
# from weaviate.collections.classes.grpc import MultiTargetVector
# def Vec_Both(query):
#     collection = get_collection(DB_DOC_COLLECTION_NAME)
#     return collection.query.hybrid(
#         query=query,
#         query_properties=[], # Parameters only for keyword search
#         target_vector=MultiTargetVector([
#             ("title", 0.5),
#             ("abstract", 0.5)
#         ]),
#         # max_vector_distance=0.2,
#         limit=1,
#         alpha=1, # An alpha of 1 is a pure vector search.
#     )






def main():
    methods = [
        # {'function':'Vec_Both', 'title':'Vec-Both'},
        {'function':'KW_Title_Vec_Title', 'title':'KW-Title + Vec-Title'},
        {'function':'KW_Title', 'title':'KW-Title'},
        {'function':'KW_Abstract', 'title':'KW-Abstract'},
        {'function':'KW_Both', 'title':'KW-Both'},

        {'function':'Vec_Title', 'title':'Vec-Title'},
        {'function':'Vec_Abstract', 'title':'Vec-Abstract'},
        {'function':'KW_Title_Vec_Abstract', 'title':'KW-Title + Vec-Abstract'},
        {'function':'KW_Abstract_Vec_Title', 'title':'KW-Abstract + Vec-Title'},
        
    ]
    file_path = "dataset/benchmark.xlsx"  # Change to your actual file path
    sample_df = load_data(file_path)
    print("Loaded benchmark dataset with", len(sample_df), "samples.")
    print("Evaluating keyword search performance...")
    results = {}
    for method in methods:
        accuracy = evaluate(sample_df, globals()[method['function']])
        print(f"\n✅ Final Accuracy ({method['title']}): {accuracy * 100:.2f}%")
        results[f"{method['title']}"] = accuracy
    return results





if __name__ == "__main__":
    main()
