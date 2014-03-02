# -*- coding: utf-8 -*-
import collections
import marisa_trie
import string, datrie
import sys
sys.setrecursionlimit(100)

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
    def __prefix_or_none(prefix):
        return None if not prefix else ReversedTrie.__reverse_str(prefix)

    def keys(self, prefix=None):
        return ReversedTrie.__reverse_list(self.trie.keys(ReversedTrie.__prefix_or_none(prefix)))

    def has_keys_with_prefix(self, prefix=None):
        return self.trie.has_keys_with_prefix(ReversedTrie.__prefix_or_none(prefix))

    def iter_prefix_items(self, prefix=None):
        iter = self.trie.iter_prefix_items(ReversedTrie.__prefix_or_none(prefix))
        for i in iter:
            yield (lambda (k, v): (ReversedTrie.__reverse_str(k), v))(i)

    def save(self, f):
        return self.trie.save(f)

    def __contains__(self, key):
        return self.trie.__contains__(self.__reverse_str(key))

    def __getitem__(self, key):
        return self.trie.__getitem__(self.__reverse_str(key))

    def __setitem__(self, key, value):
        return self.trie.__setitem__(self.__reverse_str(key), value)


BOLD_ON, BOLD_OFF, UNDERLINE_ON, UNDERLINE_OFF = '\033[1m', '\033[22m', '\033[4m', '\033[24m'
COMMAND_ON, COMMAND_OFF, WORD_ON, WORD_OFF = BOLD_ON, BOLD_OFF, UNDERLINE_ON, UNDERLINE_OFF

REWRITE = False
FIXTURE = False
if REWRITE:
    # Build dictionary tries once and save to files
    with open('onlysowpods.txt') as f:
        words = f.read().splitlines()
if FIXTURE:
    words = ['alef']
if REWRITE or FIXTURE:
    reversed_words = [word[::-1] for word in words]

    words_trie = marisa_trie.Trie(words)
    reversed_words_trie = ReversedTrie(marisa_trie.Trie(reversed_words))
    if REWRITE:
        words_trie.save('words.trie')
        reversed_words_trie.save('reversed_words.trie')
else:
    words_trie = marisa_trie.Trie().load('words.trie')
    reversed_words_trie = ReversedTrie(marisa_trie.Trie().load('reversed_words.trie'))
    

commands = ['a', 'b', 'up', 'down', 'left', 'right', 'start', 'wait']
commands_trie = marisa_trie.Trie(commands)
reversed_commands = [command[::-1] for command in commands]
reversed_commands_trie = ReversedTrie(marisa_trie.Trie(reversed_commands))

# Ordered unique substrings [c:] of words
test_words = []
[test_words.append(command[c:]) for command in commands for c in range(len(command)) if command[c:] not in test_words]
#test_words = ['orange','tier', 'it']

numbers = range(1, 1+9)

def complete(this_word, n):
    for i in range(len(this_word), 0, -1):
        end_of_this_command = this_word[:i]
        end_of_this_word = this_word[1+i:]
        ##print '\t'*n+'('+str(i)+'\t',BOLD_ON+end_of_this_command+BOLD_OFF
        prev_commands = ending_with(CommandWhich, end_of_this_command, 1+n)
        ##print '\t'*n+')',str(prev_commands)
        if prev_commands:
            return prev_commands
    
def add_name_stuff(cls):
    cls.reversed_trie = globals()['reversed_' + cls.name + 's_trie']
    cls.on = globals()[cls.name.upper() + '_ON']
    cls.off = globals()[cls.name.upper() + '_OFF']
    return cls

class Which:
    memo = ReversedTrie(datrie.Trie(string.ascii_lowercase))
    memo[u'zzz'] = None # Because datrie hangs if empty

    @classmethod
    def memoize(cls, key, value):
        #print 'Memoizing',cls.name, key, u'\t→\t', value
        cls.memo[key] = value
        return value

@add_name_stuff
class CommandWhich(Which):
    name = 'command'

    @staticmethod
    def test(end):
        return [end[:j] for j in range(len(end), 0, -1)]

@add_name_stuff
class WordWhich(Which):
    name = 'word'

    @staticmethod
    def test(end):
        return [end]

CommandWhich.opposite = WordWhich
WordWhich.opposite = CommandWhich


# Find all commands that end with a string
def ending_with(which, end_of_this, n):
    indent = '>>\t'*n
    ##print indent+'['+BOLD_ON+which.name+'s'+BOLD_OFF+'] ending in '+end_of_this+'\t'
    try:
        shortest_suffix, this = which.memo.iter_prefix_items(end_of_this).next()
        print end_of_this, ':', shortest_suffix, this
        return this
    except StopIteration:
        pass
    
    #for memo in memos:

    #print memos
    if end_of_this in which.memo:
        #print '(Memoized!    )'
        return which.memo[end_of_this]
    #print '(Not memoized.)',
    #print '~'*14

    completions = which.reversed_trie.keys(end_of_this)#[:92]
    completions.sort(key=len)
    ##print indent+'Found',len(completions),'completions:', completions

    l = len(end_of_this)
    if not which.reversed_trie.has_keys_with_prefix(end_of_this):
        ##print indent,
        return which.memoize(end_of_this, None)

    for this in completions:
        largest_end_of_prev = this[:-l]
        end_of_prevs = which.test(largest_end_of_prev)
        #print indent+'>'+this+':\t', 'largest_end_of_prev:',largest_end_of_prev,'\tend_of_prevs:',' '.join(end_of_prevs)
        
        # This means this is a command or word by itself
        if not largest_end_of_prev:
            ##print indent,
            return which.memoize(end_of_this, this)

        for end_of_prev in end_of_prevs:
            # m = n - len(str(end_end_of_prev))
            prev = ending_with(which.opposite, end_of_prev, 1+n)

            if prev:
                #print indent+which['on'] + str(prev) + which['off']
                ##print indent,
                return which.memoize(end_of_this, (prev, end_of_this))

    return which.memoize(end_of_this, None)


test_words = ['tire', 'paw', 'eft', 'own', 'art', 'through', 'prefix', 'it']
test_words = ['apple', 'banana', 'durian', 'egg', 'fruit', 'guava', 'hello', 'iodine',
 'loquat', 'nutmeg', 'orange', 'pear', 'raisin', 'sugar', 'time', 'under', 'what']

def main():
    for word in map(unicode, test_words):
        result = complete(word,0)
        print word+'\t', BOLD_ON+UNDERLINE_ON+str(result)+UNDERLINE_OFF+BOLD_OFF

    return

memoized = {}

def segment(word):
    if word in commands:
        return word
    if word in memoized:
        return memoized[word]

    for i in range(1, len(word)):
        prefix = word[:i]
        if prefix in commands:
            suffix = word[i:]
            seg_suffix = segment(suffix)
            if seg_suffix:
                memoized[word] = (prefix, seg_suffix)
                return memoized[word]
        memoized[word] = None

if 0:
    for word in words:
        seg = segment(word)
        if seg is not None:
            print word, seg


if __name__ == '__main__':
    main()
