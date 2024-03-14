def encode(text: str) -> str:
    """
    Encodes a string by swapping adjacent characters.

    :param text: String to be encoded.
    :return: Encoded string.
    """
    # Convert the string to a list of characters
    text_list = list(text)

    length = len(text_list)

    # Swap adjacent characters in the text
    for i in range(0, length - 1, 2):  # Move by two characters
        text_list[i], text_list[i + 1] = text_list[i + 1], text_list[i]  # Swap adjacent characters

    # Convert the list back to a string
    encoded_text = ''.join(text_list)

    return encoded_text
