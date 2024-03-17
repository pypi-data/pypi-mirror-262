import csv
import os

def index_csv_files(directory, word):
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    matched_files = []
    for file_name in csv_files:
        if file_name.lower().startswith(word.lower()[:1]):
            matched_files.append(file_name)
    return matched_files

def search_csv_files(directory, word, word_match_function):
    matched_files = index_csv_files(directory, word)

    for file_name in matched_files:
        file_path = os.path.join(directory, file_name)
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if word_match_function(row["word"], word):
                    return row



