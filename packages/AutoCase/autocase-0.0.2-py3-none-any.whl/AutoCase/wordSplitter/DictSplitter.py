
def DictSplitter(word,word_list,include_partial_matches=False) -> list:
    """
    This function is used to split a word into a list of words based on a dictionary.
    :argument word: str
    :argument word_list: list
    :argument include_partial_matches: bool
    :return: list
    """
    word = word.lower()
    words = []
    temp = ''
    for i in range(len(word)):
        temp += word[i]
        if temp in word_list:
            words.append(temp)
            temp = ''
    if include_partial_matches and temp:
        words.append(temp)
    return words

if __name__ == "__main__":
    word_list = ['this', 'is', 'a', 'sample', 'python', 'file']
    word = "ThisisaSamplePythonFile"
    print(DictSplitter(word, word_list, True) == ['this', 'is', 'a', 'sample', 'python', 'file'])
    print(DictSplitter(word, word_list) == ['this', 'is', 'a', 'sample', 'python', 'file'])
    word = "ThisisaSamplePython"
    print(DictSplitter(word, word_list, True) == ['this', 'is', 'a', 'sample', 'python'])
    print(DictSplitter(word, word_list) == ['this', 'is', 'a', 'sample', 'python'])
    word = "ThisisaSamplePythonFile1"
    print(DictSplitter(word, word_list, True) == ['this', 'is', 'a', 'sample', 'python', 'file', '1'])
    print(DictSplitter(word, word_list) == ['this', 'is', 'a', 'sample', 'python', 'file'])
    word = "ThisisaSampleePython1File1"
    print(DictSplitter(word, word_list, True) == ['this', 'is', 'a', 'sample', 'e','python', 'file', '1'])