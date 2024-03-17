from .utils import remove_empty_items
def CamelSplitter(word: str) -> list:
    """
    This function is used to split camel case words into a list of words.

    :return:
    """
    alphabets = 'abcdefghijklmnopqrstuvwxyz'.upper()
    word = list(word)
    words = []
    temp = ''
    for i in range(len(word)):
        if word[i] in alphabets:
            if temp:
                words.append(temp)
            temp = word[i]
        else:
            temp += word[i]
    words.append(temp)
    return remove_empty_items(words)

def SnakeSplitter(word: str) -> list:
    """
    This function is used to split snake case words into a list of words.

    :return:
    """
    words=word.split('_')
    return remove_empty_items(words)


def KebabSplitter(word: str) -> list:
    """
    This function is used to split kebab case words into a list of words.

    :return:
    """
    words=word.split('-')
    return remove_empty_items(words)

def TitleSplitter(word: str) -> list:
    """
    This function is used to split titled case words into a list of words.

    :return:
    """
    words=word.split(' ')
    return remove_empty_items(words)

def MixedSplitter(word:str)->list:
    """
    This function is used to split mixed cases into list of words

    :param word:
    :return:
    """
    words = [word]
    splitters = [CamelSplitter, SnakeSplitter, KebabSplitter, TitleSplitter]
    for splitter in splitters:
        temp = []
        for word in words:
            temp += splitter(word)
        words = temp
    return remove_empty_items(words)


if __name__ == "__main__":
    test='game_engine_se rVer_servicesModuleBase'
    test='gameEngineServerServicesModuleBase'
    print(MixedSplitter(test))

    # for test in camel_split_tests:
    #     print(CamelSplitter(test[0]) == test[1])