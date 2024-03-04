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
NP -> N | Det N | Det AP N | P NP | NP P NP | Det N PP | Det AP N PP | AP N PP | N PP
VP -> V | Adv VP | VP Adv | V NP | VP Conj VP | V PP
AP -> Adj | AP Adj
PP -> P NP

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

    # check nested substrees
    np_subtree = list(tree.subtrees(lambda t: t.label() == 'NP'))
    chunks = []

    # check each subtree
    for t in np_subtree:
        nested_subtree = list(t.subtrees(lambda st: st.label() == 'NP' and t != st))
        # if list is empty (i.e. not NP subtrees)
        # append t
        if not nested_subtree:
            chunks.append(t)
            
    return chunks

    # return tree.subtrees(
    #     lambda t: t.label() == 'NP' and
    #     not list(t.subtrees(lambda st: t != st and st.label() == 'NP'))
    # )

if __name__ == "__main__":
    main()
