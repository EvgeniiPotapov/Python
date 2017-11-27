from os import listdir
from os import path as pathfile
from math import log2


def file_splitter(pathname):  # Divides given file into a list of separate words
    file = open(pathname, "r", encoding="utf-8")
    a = file.read()
    a = a.lower()
    for letter in a:
        if not letter.isalpha():
            a = a.replace(letter, " ")  # Replace all non-letters with space
    b = a.split(" ")
    while "" in b:
        b.remove("")  # Delete empty words
    file.close()
    return b


def freq(q, d):  # Word frequency in current document
    return float(q)/d


def bm25(query):  # BM25 algorithm with k1=2, b=0.75
    k1 = 2
    b = 0.75
    words = query.lower()
    words = words.split(' ')  # Divides entry into separate words
    while '' in words:
        words.remove('')
    word_in_docs = []  # List of how many docs have word[i]
    avg_doc_len = 0.0
    frequency = []  # Frequency of each entry word in each document
    doc_lens = []
    idf = []
    word_score = []  # BM25 of separated words
    score_list = []  # BM25 of phrase in each document
    for i in range(len(words)):
        word_in_docs.append(0)
        idf.append(0)
    for i in range(docs_quantity):
        frequency.append(word_in_docs[:])
        word_score.append(word_in_docs[:])  # Raising correct ranges of lists

    for document in range(docs_quantity):
        text = file_splitter(path + r'/' + docs[document])  # Dividing document into words
        curr_doc_len = len(text)
        avg_doc_len += curr_doc_len
        doc_lens.append(curr_doc_len)
        for i in range(len(words)):
            if words[i] in text:
                word_in_docs[i] += 1  # Counting word existence in current document
            word_freq = freq(text.count(words[i]), curr_doc_len)
            frequency[document][i] = word_freq  # Filling frequency list
    avg_doc_len /= docs_quantity
    for k in range(len(idf)):
        idf[k] = log2(docs_quantity / word_in_docs[k])  # Filling IDF list
    for i in range(docs_quantity):
        for j in range(len(words)):
            if frequency[i][j] == 0:
                word_score[i][j] = 0
            else:  # The main formula with k=2 and b=0.75
                word_score[i][j] = idf[j] * (((k1+1) * frequency[i][j])/(frequency[i][j] + k1 * ((1-b)+(b*doc_lens[i])/avg_doc_len)))
    for i in range(docs_quantity):
        score_list.append(sum(word_score[i]))
    return score_list
# --------------------------------------------------------------------------------------------------------------


def is_anagram(word, clone):  # Returns True if the second string is anagram of the first
    if len(word) != len(clone):
        return False
    a = sorted(list(word))
    b = sorted(list(clone))
    return a == b


def anagrams():  # Finds anagrams in each document separately
    for document in range(docs_quantity):
        anagrams_dict = {}   # Dictionary with first unique word as a key and its anagrams as list of values
        doc = file_splitter(path + r'/' + docs[document])  # Dividing document into words
        doc = set(doc)  # Leave only unique words
        for element in doc:
            keys = anagrams_dict.keys()  # Gets list of words have been read already
            indicator = False  # Is element an anagram to something or not
            for key in keys:
                if is_anagram(key, element):
                    indicator = True
                    anagrams_dict[key].append(element)
                    break
            if not indicator:  # Add new word to collection as key
                anagrams_dict[element] = []
        print("Anagrams in ", docs[document], ":\n")
        for key in anagrams_dict:
            if anagrams_dict[key]:
                print(key, ":", anagrams_dict[key], "\n")


def anagrams2():  # Finds anagrams in collection, quite the same as previous function
    anagrams_dict = {}  # Dictionary with first unique word as a key and its anagrams as list of values
    for document in range(docs_quantity):

        doc = file_splitter(path + r'/' + docs[document])  # Dividing document into words
        doc = set(doc)  # Leave only unique words
        for element in doc:
            keys = anagrams_dict.keys()  # Gets list of words have been read already
            indicator = False  # Is element an anagram to something or not
            for key in keys:
                if is_anagram(key, element) and key != element:
                    indicator = True
                    if element not in anagrams_dict[key]:  # avoid dict value repeating
                        anagrams_dict[key].append(element)
                    break
            if not indicator:
                anagrams_dict[element] = []  # Add new word to collection as key
    print("Anagrams in collection:\n")
    for key in anagrams_dict:
        if anagrams_dict[key]:
            print(key, ":", anagrams_dict[key], "\n")


# INTERFACE
path = "docs"  # Default path
greeting = "z"
while greeting not in "yn":
    greeting = input("Welcome\nIs 'docs' your catalogue to analyse? (Y/N)\n")
    greeting = greeting.lower()
    if greeting == "y":
        pass
    elif greeting == "n":
        path = input("Please type the correct path\nto your files without last '/'\n")
        if not pathfile.exists(path):
            print("Error: this path does not exist\n")
            greeting = "z"


docs = listdir(path)
docs_quantity = len(docs)  # How many docs in catalogue
choice = input("1.BM25\n2.Anagram search\n")
if choice == "1":
    phrase = input("Enter the string to search\n")
    result = bm25(phrase)
    print("BM25 for ", phrase, ":\n")
    for i in range(docs_quantity):
        print(docs[i], "  ", result[i])
elif choice == "2":  # Submenu
    variant = input("1.Separately in each file\n2.In catalogue\n")
    if variant == "1":
        anagrams()
    elif variant == "2":
        anagrams2()
leave = input("Press Enter to exit\n")
