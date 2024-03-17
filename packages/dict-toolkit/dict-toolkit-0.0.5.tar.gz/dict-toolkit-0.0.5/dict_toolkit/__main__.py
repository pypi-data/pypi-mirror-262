from dict_toolkit.extensions.query_agent import auto_query

if __name__ == '__main__':
    word = input('Enter a word: ')
    lexical_item = auto_query(word)
    print(lexical_item)