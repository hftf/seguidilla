import marisa_trie
from load import *
from reversed_trie import ReversedTrie
from which import CommandWhich, WordWhich
import sys
sys.setrecursionlimit(100)

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
