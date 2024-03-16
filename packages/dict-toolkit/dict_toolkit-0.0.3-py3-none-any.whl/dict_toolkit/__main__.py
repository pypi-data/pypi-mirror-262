from dict_toolkit.dict_csv_handler import DictCSVHandler

if __name__ == '__main__':
    dic_csv_hander = DictCSVHandler()
    word = input('Enter a word: ')
    lexical_item = dic_csv_hander.query(word)
    print(lexical_item)