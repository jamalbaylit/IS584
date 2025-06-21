import os
import pandas as pd
import json

def get_content_and_paper_folders(directory):
    content_folders = []
    paper_folders = []

    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        if os.path.isdir(path):
            if entry.endswith('_content'):
                content_folders.append(path)
            elif entry.endswith('_paper'):
                paper_folders.append(path)

    return content_folders, paper_folders

def get_json_files(directory):
    json_files = []
    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        if os.path.isfile(path) and entry.lower().endswith('.json'):
            json_files.append(path)
    return json_files

def get_all_json_files(folders):
    files = set()
    for folder in folders:
        files.update(get_json_files(folder))
    return list(files)


def parse_info(paper_files):
    data = []
    for file_path in paper_files:
        with open(file_path, 'r') as file:
            data.append(json.load(file))
    df = pd.DataFrame(data)
    return df

def parse_abstract(file_path, df):
    df['abstract'] = ""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            row = json.loads(line)
            row_id = row['id']
            row_text = row['text']
            df.loc[df['id'] == row_id, 'abstract'] = row_text
    return df


if __name__=="__main__":
    main_directory = 'dataset/papers/'
    content_folders, paper_folders = get_content_and_paper_folders(main_directory)
    paper_files = get_all_json_files(paper_folders)
    df = parse_info(paper_files)
    df = parse_abstract('dataset/aspect_data/review_with_aspect.jsonl',df)
    df = df.replace('', pd.NA).dropna(how='any')
    df.to_json('dataset/processed.jsonl', orient='records', lines=True, force_ascii=False)

















