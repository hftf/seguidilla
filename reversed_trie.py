class ReversedTrie:
    def __init__(self, trie):
        self.trie = trie
    
    @staticmethod
    def __reverse_str(s):
        return s[::-1]

    @staticmethod
    def __reverse_list(l):
        return map(ReversedTrie.__reverse_str, l)

    @staticmethod
    def __reverse_tuple(t):
        k, v = t
        return ReversedTrie.__reverse_str(k), v

    @staticmethod
    def __prefix_or_none(prefix):
        return None if not prefix else ReversedTrie.__reverse_str(prefix)

    def keys(self, prefix=None):
        return ReversedTrie.__reverse_list(self.trie.keys(ReversedTrie.__prefix_or_none(prefix)))

    def items(self, prefix=None):
        return map(ReversedTrie.__reverse_tuple, self.trie.items(ReversedTrie.__prefix_or_none(prefix)))

    def has_keys_with_prefix(self, prefix=None):
        return self.trie.has_keys_with_prefix(ReversedTrie.__prefix_or_none(prefix))

    def prefix_items(self, prefix=None):
        return None if not prefix else map(ReversedTrie.__reverse_tuple, self.trie.prefix_items(ReversedTrie.__prefix_or_none(prefix)))

    def save(self, f):
        return self.trie.save(f)

    def __contains__(self, key):
        return self.trie.__contains__(self.__reverse_str(key))

    def __getitem__(self, key):
        return self.trie.__getitem__(self.__reverse_str(key))

    def __setitem__(self, key, value):
        return self.trie.__setitem__(self.__reverse_str(key), value)
