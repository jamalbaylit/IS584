import pandas as pd
import weaviate
from tqdm import tqdm
from config import *
from db.models import *

def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

def keyword_search(client, query, top_k=1):
    try:
        collection = get_collection(DB_DOC_COLLECTION_NAME)
        results = collection.query.bm25(
            query=query,
            query_properties=["abstract"],
            limit=1,
        )
        # results = collection.query.hybrid(
        #     query=query,
        #     query_properties=["title", "text"], # Parameters only for keyword search
        #     target_vector="body",
        #     # max_vector_distance=0.2,
        #     limit=5,
        #     alpha=0.6, # An alpha of 1 is a pure vector search.
        # )
        
        return results.objects[0].properties if results.objects else None
    except Exception as e:
        print(f"Error during search: {e}")
        return None

def evaluate(df, dbclient):
    correct = 0
    total = len(df)

    for _, row in tqdm(df.iterrows(), total=total):
        gt_uid = row['uid']
        question = row['question']
        
        retrieved = keyword_search(dbclient, question)
        if retrieved and retrieved['uid'] == gt_uid:
            correct += 1

    accuracy = correct / total
    return accuracy

def main():
    file_path = "benchmark.xlsx"  # Change to your actual file path
    sample_df = load_data(file_path)
    print("Loaded benchmark dataset with", len(sample_df), "samples.")
    print("Evaluating keyword search performance...")
    accuracy = evaluate(sample_df, dbclient)
    print(f"\n✅ Final Accuracy: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    main()
