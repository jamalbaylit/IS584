from weaviate.exceptions import WeaviateBatchError
from pathlib import Path
from tqdm import tqdm
from config import *
import time
import uuid
import json
from db.models import *




def main(file_path, collection_name):
    collection = dbclient.collections.get(collection_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        with collection.batch.fixed_size(batch_size=10) as batch:
            for line in tqdm(f):
                row = json.loads(line)
                while True:
                    try:
                        # batch.add_reference(from_collection="WikiArticle", from_uuid=src_uuid, from_property="linkedArticle", to=tgt_uuid)
                        batch.add_object(
                            properties={
                                "abstract": row['abstract'],
                                "title": row['title'],
                                "url": row['url'],
                                "uid": row['id'],
                                "conference": row['conference'],
                                "decision": row['decision'],
                                "authors": row['authors'],
                            },
                        )
                        break
                    except WeaviateBatchError as e:
                        print(f"Batch error: {e}. Retrying in 2s...")
                        time.sleep(5)

            failed_objects = collection.batch.failed_objects
            if failed_objects:
                print(f"Number of failed imports: {len(failed_objects)}")
                print(f"First failed object: {failed_objects[0]}")


if __name__=='__main__':
    # print('#️⃣  Total Data Count:', get_data_count(DB_DOC_COLLECTION_NAME))
    # main('dataset/processed.jsonl',DB_DOC_COLLECTION_NAME)
    # print('#️⃣  Total Data Count:', get_data_count(DB_DOC_COLLECTION_NAME))
    collection=get_collection(DB_DOC_COLLECTION_NAME)
    for item in collection.iterator(
        include_vector=True  # If using named vectors, you can specify ones to include e.g. ['title', 'body'], or True to include all
    ):
        print(f"{item.properties['uid']}.",item.properties['title'])