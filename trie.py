#!/usr/bin/env python3

class Trie:

	def __init__(self, parent = None, children = []):
		self.root = {}

	def insert(self, word):
		"""
		Add a word to the trie with a starting
		value of 0
		"""
		branch = self.root
		for letter in word:
			if not letter in branch:
				branch[letter] = {}
				branch = branch[letter]
			else:
				branch = branch[letter]
		if not '$' in branch:
			branch['$'] = 0

	def count(self, word):
		"""
		Increment word's value in the trie
		Returns True if a new word is introduced
		Returns False otherwise
		"""
		new_word = False
		branch = self.root
		for letter in word:
			if not letter in branch:
				self.insert(word)
				new_word = True
				branch = branch[letter]
			else:
				branch = branch[letter]
		branch['$'] += 1
		return new_word

	def get_val(self, word):
		"""
		Return word's value in the trie
		"""
		branch = self.root
		for letter in word:
			branch = branch[letter]
		return branch['$']

if __name__=='__main__':
	trie = Trie()
	txt = "Hello world My name is John and Python is awesome Hello hello hello"
	for word in txt.lower().split():
		trie.count(word)

	for word in txt.lower().split():
		print(word, end=' ')
		print(trie.get_val(word))
