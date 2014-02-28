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

    def keys(self, prefix):
        return ReversedTrie.__reverse_list(self.trie.keys(ReversedTrie.__reverse_str(prefix)))

    def has_keys_with_prefix(self, prefix):
        return self.trie.has_keys_with_prefix(ReversedTrie.__reverse_str(prefix))

    def save(self, f):
        return self.trie.save(f)


BOLD_ON, BOLD_OFF, UNDERLINE_ON, UNDERLINE_OFF = '\033[1m', '\033[22m', '\033[4m', '\033[24m'
COMMAND_ON, COMMAND_OFF, WORD_ON, WORD_OFF = BOLD_ON, BOLD_OFF, UNDERLINE_ON, UNDERLINE_OFF

def memoize(f):
    class memodict(dict):
        __slots__ = ()
        def __missing__(self, key):
            self[key] = ret = f(key)
            return ret
    return memodict().__getitem__

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

numbers = range(1, 9)

memoized = {}
commands_ending_with_memoized = {}
words_ending_with_memoized = {}

def complete(this_word, n):
    for i in range(len(this_word), 0, -1):
        end_of_this_command = this_word[:i]
        end_of_this_word = this_word[1+i:]
        print '\t'*n+'('+str(i)+'\t',BOLD_ON+end_of_this_command+BOLD_OFF
        prev_commands = ending_with('command', end_of_this_command, 1+n)
        print '\t'*n+')',str(prev_commands)
        if prev_commands:
            return prev_commands

class Which:
    def __init__(self, name):
        self.name = name
        self.reversed_trie = globals()['reversed_' + name + 's_trie']
        self.on = globals()[key.upper() + '_ON']
        self.off = globals()[key.upper() + '_OFF']
        
    memo = datrie.Trie(string.ascii_lowercase)

    def memoize(self, key, value):
        memo[key] = value
    
class CommandWhich(Which):
    def __init__(self, name):
        super(self.__class__, self).__init__(name)
        self.opposite = WordWhich
        self.test = lambda largest_end_of_prev_command: [largest_end_of_prev_command[:j] for j in range(len(largest_end_of_prev_command), 0, -1)]

class WordWhich(Which):
    def __init__(self, name):
        super(self.__class__, self).__init__(name)
        self.opposite = CommandWhich
        self.test = lambda largest_end_of_prev_command: [largest_end_of_prev_word]

whiches = {
    'command': {
        'opposite': 'word',
        'test': lambda largest_end_of_prev_command: [largest_end_of_prev_command[:j] for j in range(len(largest_end_of_prev_command), 0, -1)]
    },
    'word': {
        'opposite': 'command',
        'test': lambda largest_end_of_prev_word: [largest_end_of_prev_word]
    }
}
for key in whiches:
    whiches[key].update({
        'name': key,
        'memoized': datrie.Trie(string.ascii_lowercase),
        'memoize': lambda k, v: whiches[key]['memoized'].__setitem__(k, v),
        'reversed_trie': globals()['reversed_' + key + 's_trie'],
        'on': globals()[key.upper() + '_ON'],
        'off': globals()[key.upper() + '_OFF'],
    })


print CommandWhich.memo
pass

#whiches['word']['memoize'](u'a', '3')
print whiches['word']['memoized'].__setitem__(u'a', 3)
print whiches['word']['memoized'].keys()
exit()

def which_memoize(which, key, value):
    trie[key] = value
    print 'Memoizing', key, '=', value
    return value

# Find all commands that end with a string
#@memoize
def ending_with(which, end_of_this, n):
    indent = '>>\t'*n
    #which = whiches[which]
    #print
    print indent+'['+BOLD_ON+which['name']+'s'+BOLD_OFF+'] ending in '+end_of_this+'\t'
    if end_of_this in which['memoized']:
        return which.memoize
        #print '(Memoized!    )'
        return which['memoized'][end_of_this]
    #print '(Not memoized.)',
    #print '~'*14

    completions = which['reversed_trie'].keys(end_of_this)[:92]
    completions.sort(key=len)
    print indent+'Found',len(completions),'completions:', completions

    l = len(end_of_this)
    if not which['reversed_trie'].has_keys_with_prefix(end_of_this):
        which['memoized'][end_of_this] = None
        print indent+'Memoizing None.'
        return

    for this in completions:
        largest_end_of_prev = this[:-l]
        end_of_prevs = which['test'](largest_end_of_prev)
        #print indent+'>'+this+':\t', 'largest_end_of_prev:',largest_end_of_prev,'\tend_of_prevs:',' '.join(end_of_prevs)
        
        # This means this is a command or word by itself
        if not largest_end_of_prev:
            which['memoized'][end_of_this] = this
            return which['memoized'][end_of_this]

        for end_of_prev in end_of_prevs:
            # m = n - len(str(end_end_of_prev))
            prev = ending_with(which['opposite'], end_of_prev, 1+n)

            if prev:
                #print indent+which['on'] + str(prev) + which['off']
                which['memoized'][end_of_this] = prev + end_of_this
                return which['memoized'][end_of_this]

    which['memoized'][end_of_this] = None
    return
# -------------






def commands_ending_with(end_of_this_command):
    if end_of_this_command in commands_ending_with_memoized:
        return commands_ending_with_memoized[end_of_this_command]
    ii = len(end_of_this_command)
    if not reversed_commands_trie.has_keys_with_prefix(end_of_this_command):
        commands_ending_with_memoized[end_of_this_command] = None
        return
    completions = reversed_commands_trie.keys(end_of_this_command)
    for this_command in completions:
        largest_end_of_prev_word = this_command[ii:]

        # This means this_command is a word by itself ("a")
        if not largest_end_of_prev_word:
            commands_ending_with_memoized[end_of_this_command] = this_command[::-1]
            return commands_ending_with_memoized[end_of_this_command]

        for j in range(len(largest_end_of_prev_word), 0, -1):
            end_of_prev_word = largest_end_of_prev_word[:j]
            # m = n - len(str(end_of_prev_word))
            prev_word = words_ending_with(end_of_prev_word)
            if prev_word:
                print WORD_ON+str(prev_word)+WORD_OFF
                commands_ending_with_memoized[end_of_this_command] = prev_word + end_of_this_command[::-1]
                return commands_ending_with_memoized[end_of_this_command]
    commands_ending_with_memoized[end_of_this_command] = None
    return

#@memoize
def words_ending_with(end_of_this_word):
    if end_of_this_word in words_ending_with_memoized:
        return words_ending_with_memoized[end_of_this_word]
    print 'LOOKING FOR WORDS ENDING WITH',end_of_this_word[::-1]
    if not reversed_words_trie.has_keys_with_prefix(end_of_this_word):
        words_ending_with_memoized[end_of_this_word] = None
        return

    iii = len(end_of_this_word)
    completions = reversed_words_trie.keys(end_of_this_word)
    for this_word in completions:
        #print 'FOUND WORD:', this_word[::-1]
        largest_end_of_prev_command = this_word[iii:]

        # This means this_word is a command by itself
        if not largest_end_of_prev_command:
            words_ending_with_memoized[end_of_this_word] = this_word[::-1]
            return words_ending_with_memoized[end_of_this_word]

        end_of_prev_command = largest_end_of_prev_command#[:j]
        #m = n - len(str(end_of_prev_command))
        prev_command = commands_ending_with(end_of_prev_command)
        if prev_command:
            print COMMAND_ON+str(prev_command)+COMMAND_OFF
            words_ending_with_memoized[end_of_this_word] = prev_command + end_of_this_word[::-1]
            return words_ending_with_memoized[end_of_this_word]
    words_ending_with_memoized[end_of_this_word] = None
    return

#test_words = ['tire', 'paw', 'eft', 'own', 'art', 'through', 'prefix', 'it']
#test_words = ['apple', 'banana', 'durian', 'egg', 'fruit', 'guava', 'hello', 'iodine', 'loquat', 'nutmeg', 'orange', 'pear', 'raisin', 'sugar', 'time', 'under', 'what']

test_words = map(unicode, test_words)
for word in test_words:
    result = complete(word,0)
    print word, BOLD_ON+UNDERLINE_ON+str(result)+UNDERLINE_OFF+BOLD_OFF

print commands_ending_with_memoized
print words_ending_with_memoized

exit()

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

for word in words:
    seg = segment(word)
    if seg is not None:
        print word, seg
