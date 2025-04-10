# trie.py
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.data = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, data):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.data = data

    def search(self, word):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                return None
            node = node.children[char]
        if node.is_end:
            return node.data
        return None