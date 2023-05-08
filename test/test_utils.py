
def parse_product_url(url: str) -> str:
    """
    Parses a given product URL to retrieve the name of the product in the URL.

    Args:
        url (str): A string representing the product URL.

    Returns:
        str: A string representing the name of the product in the URL.
    """
    # Remove any trailing forward slash
    url = url.rstrip('/')

    # Get the last piece of the URL after the last '/'
    last_piece = url.split('/')[-1]

    # Remove any '-' characters
    product_name = last_piece.replace('-', '')

    return product_name


def compare_words(word1:str, word2:str):
    """
    Compare two words alphabetically and return a string indicating their relationship.

    :param word1: A string representing the first word to compare.
    :type word1: str
    :param word2: A string representing the second word to compare.
    :type word2: str
    :return: A string indicating whether word1 comes before, after, or is the same as word2 alphabetically.
    :rtype: str
    """

    # Convert words to lowercase and remove non-alphabetic characters
    word1 = ''.join(filter(str.isalpha, word1.lower()))
    word2 = ''.join(filter(str.isalpha, word2.lower()))

    if word1 < word2:
        return "word1 comes before word2 alphabetically"
    elif word1 > word2:
        return "word1 comes after word2 alphabetically"
    else:
        return "word1 and word2 are the same word"

