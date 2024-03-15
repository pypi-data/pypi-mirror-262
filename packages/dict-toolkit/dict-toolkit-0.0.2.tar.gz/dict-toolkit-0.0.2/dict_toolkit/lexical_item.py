
class LexicalItem:
    def __init__(self, word, definition, translation):
        self.word = word
        self.definition = definition
        self.translation = translation
    
    def __str__(self):
        return f'{self.word}: {self.definition} ({self.translation})'