# -*- coding: utf-8 -*-
import string, datrie
from reversed_trie import ReversedTrie
from load import *

def add_name_stuff(cls):
    cls.reversed_trie = globals()['reversed_' + cls.name + 's_trie']
    cls.on = globals()[cls.name.upper() + '_ON']
    cls.off = globals()[cls.name.upper() + '_OFF']
    return cls


class Which:
    memo = ReversedTrie(datrie.Trie(string.ascii_lowercase))
    memo[u'zzz'] = None # Because datrie hangs if empty

    @classmethod
    def memoize(cls, key, value, indent=''):
        if __debug__:
            print indent+'Memoizing',cls.name, key, u'\t→\t', value
        cls.memo[key] = value
        return value

@add_name_stuff
class CommandWhich(Which):
    name = 'command'

    @staticmethod
    def test(end):
        return [end[j:] for j in range(len(end))]

@add_name_stuff
class WordWhich(Which):
    name = 'word'

    @staticmethod
    def test(end):
        return [end]

CommandWhich.opposite = WordWhich
WordWhich.opposite = CommandWhich
