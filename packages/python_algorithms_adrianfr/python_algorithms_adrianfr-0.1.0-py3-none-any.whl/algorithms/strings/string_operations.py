

class StringOperations:

    def __init__(self, text: str) -> None:
        self.text = text

    def is_anagram(self, text_to_check: str) -> bool:
        """
        Check if two strings are anagrams.

        :param text_to_check: String to be checked if is anagram with the other.
        :return: True if the strings are anagrams, else False.
        """

        return sorted(self.text) == sorted(text_to_check)

    def is_palindrome(self) -> bool:
        """
        Check if the string is a palindrome.

        :return: True if the string is a palindrome, else False.
        """
        return self.text[::] == self.text[::-1]

    def pattern_search(self, pattern: str) -> bool:
        """
        Check if a pattern exists in the given text.

        :param pattern: Pattern to be searched in the text.
        :return: True if the pattern is found in the text, else False.
        """
        pattern_length = len(pattern)
        text_length = len(self.text)

        # Iterate through the text, up to the point where the remaining characters are less than the pattern length
        for i in range(text_length - pattern_length + 1):
            match = True  # Flag to track if a match is found
            # Check if characters in the pattern match the corresponding characters in the text
            for j in range(pattern_length):
                if self.text[i + j] != pattern[j]:
                    match = False  # Set the flag if a mismatch is found
                    break

            if match:
                return True  # Return True if the entire pattern matches the substring of the text

        return False  # Return False if the pattern is not found in the text

    def lex_sort(self) -> str:
        """
        Perform lexicographic sort on a string without using built-in methods.

        :return: Lexicographically sorted string.
        """
        n = len(self.text)
        char_list = list(self.text)

        for i in range(n):
            for j in range(0, n - i - 1):
                if char_list[j] > char_list[j + 1]:
                    char_list[j], char_list[j + 1] = char_list[j + 1], char_list[j]

        return ''.join(char_list)
