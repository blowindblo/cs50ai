import nltk
import sys
from nltk.tokenize import word_tokenize
nltk.download('punkt')

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | NP VP Conj VP | NP VP Conj NP VP
NP -> N | Det N | Det AP N | P NP | NP P NP
VP -> V | Adv V | V Adv | VP NP | V NP Adv
AP -> Adj | AP Adj

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        print(np_chunk(tree))
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # separate sentence by space
    tokens = word_tokenize(sentence)

    # remove words that do not contain at least one alphabet 
    # lowercase words
    words = [word.lower() for word in tokens if any(c.isalpha() for c in word)]
    return (words)


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []
    
    parent_tree = nltk.tree.ParentedTree.convert(tree)


    # for subtree in parent_tree.subtrees():
    #     print(subtree)
    #     if subtree.label() == 'N':
    #         chunks.append(subtree.parent())
    def np_search(tree):
        # print(f' tree {tree} current np chunk {current_np_chunk}')
        # loop through each child
        for t in tree:
            if t.label() == 'N':
                chunks.append(t.parent())
            elif t.label() == 'NP' and len(t) == 1:
                chunks.append(t)
            # elif t.label() == 'NP':
            #     np_search(t)
            elif isinstance(t, nltk.ParentedTree) and len(t) > 1:
                # print(t)
                np_search(t)
    #     #     np_search(t)
    #     #     print(f'current {t} {len(t)}')
    #     #     # check that it's a tree with more than one children 
    #     #     if isinstance(t, nltk.Tree) and len(t) > 1:
    #     #         if t.label() == 'NP' or t.label() == 'S' or t.label() == 'VP':
    #     #             current_np_chunk = t
    #     #             print(f'This is NP. Search {t}')
    #     #             np_subtree = np_search(t, current_np_chunk, np_subtree)
    #     #         else:
    #     #             print(f'Search {t}')
    #     #             np_subtree = np_search(t, current_np_chunk, np_subtree)
    #     # # if there are no subtrees that are NP, append to chunks and return True
    #     # if not np_subtree and current_np_chunk != "":
    #     #     print(f'add NP {current_np_chunk}')
    #     #     print(f'{isinstance(current_np_chunk, nltk.Tree)}')
    #     #     chunks.append(current_np_chunk)
    #     #     print(f'{len(chunks)}')
    #     #     print(chunks)
    #     #     return True

    np_search(parent_tree)
    

    return(chunks)

if __name__ == "__main__":
    main()
