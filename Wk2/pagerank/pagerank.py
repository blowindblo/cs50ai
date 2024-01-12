import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # no. of keys (i.e. pages)
    corpus_size = len(corpus)

    # if page has no outgoing links
    if len(corpus[page]) == 0:
        model = dict.fromkeys(corpus.keys(), 1 / corpus_size)       # equal prob
    else:
        base_prob = (1 - damping_factor)/corpus_size
        model = dict.fromkeys(corpus.keys(), base_prob)
        links_count = len(corpus[page])
        for link in corpus[page]:
            model[link] += damping_factor/links_count

    return model



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    results = dict.fromkeys(corpus.keys(),0)
    page = random.choice(list(corpus.keys()))
    results[page] = 1/n

    for i in range(n):
        prob_dict = transition_model(corpus, page, damping_factor)
        links = list(prob_dict.keys())
        prob = list(prob_dict.values())
        page = random.choices(links, weights = prob)[0]
        results[page] += 1/n

    return results


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # no. of keys (i.e. pages)
    corpus_size = len(corpus)

    # set up result dict
    results = dict.fromkeys(corpus.keys(), 1/len(corpus))

    # prob of landing on a random page in the corpus
    base_prob = (1 - damping_factor)/corpus_size

    # create empty dictionary for new results
    new_results = {}
    iterate = True

    # iterate until it converages
    while iterate == True:
        print('iterating')
        iterate = False
        for main_page in corpus.keys():
            # set first part of equation (base prob)
            new_results[main_page] = base_prob
            for link_page, links in corpus.items():
                # if no links on page, randomly pick from all links in corpus 
                if len(links) == 0:
                    new_results[main_page] += damping_factor * (results[link_page] / corpus_size)
                # if link_page has a link to main_page, randomly pick from all links from link_page
                elif main_page in links:
                    new_results[main_page] += damping_factor * (results[link_page] / len(links))

        # normalize page ranks
        factor = sum(new_results.values())
        new_results = {page: (prob / factor) for page, prob in new_results.items()}

        # Check for changes in page rank
        for p in corpus.keys():
            if abs(new_results[p] - results[p]) > 0.001:
                iterate = True
                break

        # Create a copy to track changes later
        results = copy.deepcopy(new_results)

    return results


if __name__ == "__main__":
    main()
