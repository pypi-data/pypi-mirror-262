def remove_empty_items(words:list)->list:
    """
    This function is used to remove empty items from a list of words.

    :param words:
    :return:
    """
    return [word for word in words if (word and word.strip() and word.strip() != '')]