import marisa_trie
from load import *
from reversed_trie import ReversedTrie
from which import CommandWhich, WordWhich
import sys, codecs
sys.setrecursionlimit(100)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def complete(this_word, n):
    for i in range(len(this_word), 0, -1):
        end_of_this_command = this_word[:i]
        end_of_this_word = this_word[1+i:]
        ##print '\t'*n+'('+str(i)+'\t',BOLD_ON+end_of_this_command+BOLD_OFF
        prev_commands = ending_with(CommandWhich, end_of_this_command, 1+n)
        ##print '\t'*n+')',str(prev_commands)
        if prev_commands:
            return prev_commands

# Find all commands that end with a string
def ending_with(which, end_of_this, n):
    indent = '>\t'*n
    if __debug__:
        print indent+'['+BOLD_ON+which.name+'s'+BOLD_OFF+'] ending in '+end_of_this+'\t'

    # Return result if already memoized
    if end_of_this in which.memo:
        return which.memo[end_of_this]

    # If there was no solution to any suffixes of end_of_this,
    # then there can't be a solution for end_of_this
    prefix_items = which.memo.prefix_items(end_of_this)
    for suffix, this in prefix_items:
        if __debug__:
            print indent, 'Checking memoized suffixes of', end_of_this+':', (suffix, this)
        if not this:
            return this

    # Get all the words that have the suffix end_of_this
    completions = which.reversed_trie.keys(end_of_this)
    completions.sort(key=len)
    if __debug__:
        print indent+'Found',len(completions),'completions:', completions[:12]

    l = len(end_of_this)
    if not which.reversed_trie.has_keys_with_prefix(end_of_this):
        return which.memoize(end_of_this, None, indent)

    for this in completions:
        largest_end_of_prev = this[:-l]
        end_of_prevs = which.test(largest_end_of_prev)
        if __debug__:
            print indent+'>'+this+':\t', 'largest_end_of_prev:',largest_end_of_prev,'\tend_of_prevs:',' '.join(end_of_prevs)
        
        # If the prefix of this completion is empty,
        # then it means the suffix is a word by itself
        if not largest_end_of_prev:
            return which.memoize(end_of_this, this, indent)

        # Get all words that are (non-strict) suffixes of the prefix of this completion
        suffixes_of_prefix = which.opposite.reversed_trie.prefixes(largest_end_of_prev)
        suffixes_of_prefix.sort(key=len)

        for suffix_of_prefix in suffixes_of_prefix:
            prefix_of_prefix = largest_end_of_prev[:-len(suffix_of_prefix)]

            # If the prefix of the prefix is empty,
            # then it means the prefix is a word by itself
            if not prefix_of_prefix:
                return which.memoize(end_of_this, (largest_end_of_prev, end_of_this), indent)

            prev = ending_with(which.opposite, prefix_of_prefix, 1+n)
            if prev:
                return which.memoize(end_of_this, (prev, suffix_of_prefix, end_of_this), indent)

        for end_of_prev in end_of_prevs:
            # m = n - len(str(end_end_of_prev))
            prev = ending_with(which.opposite, end_of_prev, 1+n)
            if __debug__:
                print indent+'PREV...', prev

            if prev:
                #print indent+which['on'] + str(prev) + which['off']
                return which.memoize(end_of_this, (prev, end_of_this), indent)

    return which.memoize(end_of_this, None, indent)


def main():
    global test_words
    if len(sys.argv) > 1:
        test_words = sys.argv[1:]
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
