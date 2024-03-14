## Strings


### Table of content
* [Is anagram](#is-anagram)
* [Is palindrome](#is-palindrome)
* [Pattern search](#pattern-search)
* [Lexicographic sort](#lexicographic-sort)


### Is anagram
    An anagram is a word or phrase formed by rearranging the letters of 
    another word or phrase, using all the original letters exactly once. 
    This function checks if the input strings have the same characters, 
    irrespective of their order.

    How is anagram Works
    1. Character Frequency Comparison:
    The function compares the frequency of characters in both strings.
    It ensures that both strings contain the same characters with the same 
    frequency.
    2. Handling Spaces and Case Sensitivity:
    The function usually treats spaces as valid characters but ignores 
    them during the comparison. It may or may not be case-sensitive, 
    depending on the implementation.
    3. Efficiency:
    The algorithm generally has a time complexity of O(n), where n is 
    the length of the strings.

### Is palindrome
    This function determines whether a given string is a palindrome. 
    A palindrome is a word, phrase, number, or other sequence of 
    characters that reads the same forward and backward. This function
    checks if the input string remains the same when its characters are 
    reversed.

    How isPalindrome Works
    1. String Reversal:
    The function reverses the characters in the input string.
    2. Comparison:
    It compares the reversed string with the original string.
    3. Handling Spaces and Case Sensitivity:
    The function may or may not consider spaces and be case-sensitive, 
    depending on the implementation.
    4. Efficiency:
    The algorithm typically has a time complexity of O(n), where n is the 
    length of the string.

### Pattern search
    The pattern search function checks whether a specific pattern exists 
    in a given text. This type of search is often employed in string 
    matching algorithms to find occurrences of a pattern within a larger
    text or document.
    
    How patternSearch Works
    1. Iterative Comparison:
    The function iterates through the text, comparing substrings of the 
    same length as the pattern.
    2. Pattern Matching:
    It checks if the current substring matches the pattern.
    Reporting Matches:
    The function may return the indices or positions where the pattern
    is found in the text.
    3. Efficiency:
    The efficiency of the algorithm depends on the specific search strategy. 
    Common approaches include brute-force, Knuth-Morris-Pratt (KMP), 
    and Boyer-Moore algorithms.

### Lexicographic sort
    Lexicographic sort, also known as dictionary order or alphabetical order, 
    arranges elements based on their dictionary or alphabetical order. For 
    strings, this means arranging them based on the order of their characters
    from left to right.

    How Lexicographic Sort Works
    1. Comparison of Elements:
    The algorithm compares elements based on their lexicographic order.
    2. Swapping Elements:
    If the current element is greater than the next one in lexicographic 
    order, they are swapped.
    3. Iterative Process:
    The process is repeated until the entire list is sorted.
    4. Efficiency:
    The efficiency depends on the sorting algorithm used. Common algorithms 
    for lexicographic sorting include quicksort and mergesort.
