import marisa_trie
from reversed_trie import ReversedTrie

BOLD_ON, BOLD_OFF, UNDERLINE_ON, UNDERLINE_OFF = '\033[1m', '\033[22m', '\033[4m', '\033[24m'
COMMAND_ON, COMMAND_OFF, WORD_ON, WORD_OFF = BOLD_ON, BOLD_OFF, UNDERLINE_ON, UNDERLINE_OFF

REWRITE = False
FIXTURE = False
if REWRITE:
    # Build dictionary tries once and save to files
    # grep -v [^ABDEFGHILNOPRSTUW] sowpods.txt | dd conv=lcase > onlysowpods.txt
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
