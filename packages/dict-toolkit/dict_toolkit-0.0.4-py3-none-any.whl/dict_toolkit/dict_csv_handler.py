from dict_toolkit.dict_handler import DictHandler
from dict_toolkit.lexical_item import LexicalItem
from dict_toolkit import default_dict_path
from dict_toolkit.match_rules import word_match
from dict_toolkit.utils.csv_util import search_csv_files

class DictCSVHandler(DictHandler):
    def __init__(self, dict_path=None):
        self.dict_path = dict_path if dict_path else default_dict_path

    def query(self, word):
        found_data = search_csv_files(self.dict_path, word, word_match)
        return LexicalItem(found_data["word"], found_data['definition'], found_data['translation']) if found_data else None

        