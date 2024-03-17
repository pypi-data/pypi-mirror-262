from dict_toolkit.extensions.dict_csv_handler import DictCSVHandler

def auto_query(word):
    dic_csv_hander = DictCSVHandler()
    lexical_item = dic_csv_hander.query(word)
    
    # if lexical_item is None: query online and add to the dict data

    return lexical_item