import nltk
import sys

import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    dir_map = dict()

    for file in os.listdir(directory):
        file_open = open(os.path.join(directory,file),"r",encoding='utf-8')
        dir_map[file] = file_open.read()

    return dir_map


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    words = nltk.word_tokenize(document.lower())

    tokenised_words = []

    for word in words:
        if word not in string.punctuation:
            if word not in nltk.corpus.stopwords.words("english"):
                tokenised_words.append(word)

    return tokenised_words
    

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    word_in_file = dict()
    idfs = dict()

    for key, values in documents.items():
        for value in values:
            if value not in word_in_file.keys():
                word_in_file[value] = [key]
            else:
                if key not in word_in_file[value]:
                    word_in_file[value].append(key)
                    
    for word, list_files in word_in_file.items():
        idfs[word] = math.log(len(documents.keys()) / len(list_files))

    return idfs
        

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    tf_idf = dict()

    tf_idf_ranked = []

    for word in query:
        for file in files.keys():
            if file not in tf_idf.keys():
                tf_idf[file] = 0

    
    for word in query:
        for file, words in files.items():
            if word in words:
                word_count = 0
                for w in words:
                    if w == word:
                        word_count = word_count + 1
                tf_idf[file] = tf_idf[file] + word_count * idfs[word]

    for word, score in sorted(tf_idf.items(),key=lambda x:x[1],reverse=True)[:n]:
        tf_idf_ranked.append(word)

    return tf_idf_ranked
  

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    sentences_idf = dict()
    sentences_density = dict()

    sentence_ranked = []
    
    for sentence, words in sentences.items():
        sentences_idf[sentence] = 0
        sentences_density[sentence] = 0
        word_count = 0
        for word in query:
            if word in words:
                sentences_idf[sentence] = sentences_idf[sentence] + idfs[word]
                word_count = word_count + 1

        sentences_density[sentence] = word_count/len(words)

    for sentence, score in sorted(sentences_idf.items(),key=lambda x:x[1],reverse=True)[:n]:
        sentence_ranked.append(sentence)
        for sentence1, score1 in sentences_idf.items():
            if score1 == score:
                if sentence1 != sentence:
                    if sentences_density[sentence1] > sentences_density[sentence]:
                        sentence_ranked.remove(sentence)
                        sentence_ranked.append(sentence1)

    return sentence_ranked


if __name__ == "__main__":
    main()
