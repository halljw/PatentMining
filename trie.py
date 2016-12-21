#!/usr/bin/env python3

from string import punctuation

"""
An implementation of a trie data structure for use in storing the word counts
extracted from multiple patent text documents. Terminal nodes are marked with '$'
It is assumed text document lines are of the format:
	SECTION :: TEXT

Author: John W. Hall, jwhall5@illinois.edu
"""
class Trie:

    def __init__(self):
        self.root = {}

    def insert(self, word):
        """
        Add a word to the trie with a starting value of 0
        """
        branch = self.root
        if len(word) == 0:
            branch['$'] = 0
        else:
            if word[0] in branch:
                branch[word[0]].insert(word[1:])
            else:
                branch[word[0]] = Trie()
                branch[word[0]].insert(word[1:])


    def count(self, word):
        """
        Increment word's value in the trie
        Returns True if a new word is introduced
        Returns False otherwise
        """
        branch = self.root
        if len(word) == 0:
            if '$' in branch:
                branch['$'] += 1
                return False
            else:
                branch['$'] = 1
                return True
        else:
            if word[0] in branch:
                return branch[word[0]].count(word[1:])
            else:
                branch[word[0]] = Trie()
                return branch[word[0]].count(word[1:])

    def get_val(self, word):
        """
        Return word's value in the trie
        """
        branch = self.root
        if len(word) == 0:
            return branch['$']
        else:
            if word[0] in branch:
                return branch[word[0]].get_val(word[1:])
            else:
                return 0

    def clear_vals(self):
        """
        Set all values in trie to 0
        """
        branch = self.root
        for letter in branch:
            if letter == '$':
                branch[letter] = 0
            else:
                branch[letter].clear_vals()

    def count_line(self, line):
        """
        Count the words in a line and update word-count values in trie.
        Returns a list of words encountered for the first time.
        """
        try:
            new_words = []
            words = ''.join([char for char in line.split("::")[1].lower().strip() if not char in punctuation]).split()
            for word in words:
                if word.isalpha():
                    if self.count(word):
                        new_words.append(word)
            return new_words
        except:
            return []
		

if __name__=='__main__':
    trie = Trie()
    txt = """"
    ABST :: Is this a dagger which I see before me, the handle toward my hand? 
    Come, let me clutch thee. I have thee not, and yet I see thee still.
    """
    trie.count_line(txt)

    txt = ''.join([char for char in txt.lower().strip() if not char in punctuation])
    for word in txt.split():
        print(word, end=' ')
        print(trie.get_val(word))
