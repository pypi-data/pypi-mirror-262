from dict_toolkit.dict_handler import DictHandler
from dict_toolkit.lexical_item import LexicalItem
from dict_toolkit import default_dict_path
import csv
import os

class DictCSVHandler(DictHandler):
    def __init__(self, dict_path=None):
        self.dict_path = dict_path if dict_path else default_dict_path

    def search_csv_files(directory, column_name, match_function):
        csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

        found_data = []
        for file_name in csv_files:
            file_path = os.path.join(directory, file_name)
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if match_function(row[column_name]):
                        found_data.append(row)

        return found_data

    def query(self, word):
        match_word = lambda w: w.lower() == word.lower()

        found_data = DictCSVHandler.search_csv_files(self.dict_path, 'word', match_word)

        if found_data:
            return LexicalItem(found_data[0]['word'], found_data[0]['definition'], found_data[0]['translation'])
        else:
            return None
