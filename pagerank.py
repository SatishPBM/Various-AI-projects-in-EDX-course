import os
import random
import re
import sys

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

    pages_dist = dict()

    if corpus[page]:
        for page_link in corpus[page]:
            pages_dist[page_link] = damping_factor/len(corpus[page])
    for key in corpus.keys():
        if key not in pages_dist.keys():
            pages_dist[key] = 0
        pages_dist[key] = round(pages_dist[key] + (1 - damping_factor)/len(corpus.keys()),4)
        
    return pages_dist
        

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    s_pagerank = dict()
    
    sample_page = random.choice(list(corpus.keys()))

    s_pagerank[sample_page] = 1

    for _ in range(n-1):
        prob_dist = transition_model(corpus, sample_page, damping_factor)
        sample_page = random.choices(list(prob_dist.keys()),list(prob_dist.values()))[0]
        if sample_page in s_pagerank.keys():
            s_pagerank[sample_page] = s_pagerank[sample_page] + 1
        else:
            s_pagerank[sample_page] = 1    
        
    for key, value in s_pagerank.items():
        s_pagerank[key] = value/n

    return s_pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    i_pagerank = dict()
    
    for page in corpus.keys():
        i_pagerank[page] = 1/len(corpus)

    converged = False
    
    while converged == False:
        converged = True
        for i_page in i_pagerank.keys():
            numlinks_factor = 0
            prev_pagerank = i_pagerank[i_page]
            for key, values in corpus.items():
                if i_page in values:
                    numlinks_factor = numlinks_factor + i_pagerank[key]/len(values)
            i_pagerank[i_page] = (1 - damping_factor)/len(corpus) + damping_factor * numlinks_factor
            if abs(i_pagerank[i_page] - prev_pagerank) >= 0.001:
                converged = False

    return i_pagerank

    
if __name__ == "__main__":
    main()
