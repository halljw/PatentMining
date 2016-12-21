#!/usr/bin/env python3

class Master_Matrix:

  def __init__(self):
    self.int2word = []
    self.word2int = Matrix_Trie()

  def search(self, word):
    index = self.word2int.get_int(word, len(self.int2word))
    if index == len(self.int2word):
      self.int2word.append(word)
    return index

  def words(self):
    return self.int2word


class Matrix_Trie:

  def __init__(self):
    self.root = {}

  def get_int(self, word, current):
    """
    Return a words integer marker if found in the trie.
    If word not in tree, assign it an integer
    """
    branch = self.root
    if len(word) == 0:
      if '$' in branch:
        return branch['$']
      else:
        branch['$'] = current
        return current
    else:
      if word[0] in branch:
        return branch[word[0]].get_int(word[1:], current)
      else:
        branch[word[0]] = Matrix_Trie()
        return branch[word[0]].get_int(word[1:], current)

