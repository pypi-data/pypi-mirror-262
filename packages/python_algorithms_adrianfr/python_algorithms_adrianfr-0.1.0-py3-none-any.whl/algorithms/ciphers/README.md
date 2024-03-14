## Ciphers

## Table of Content
* [Caesar cipher](#caesar-cipher)
* [Morse cipher](#morse-cipher)
* [Swap cipher](#swap-cipher)


### Caesar cipher
    The Caesar Cipher is one of the simplest and earliest known encryption techniques, falling under
    the category of shifting ciphers. It operates by shifting each letter in the plaintext by a fixed
    value known as the key. Here's a brief overview of the encryption and decryption process:

    Encryption
    During encryption, each letter in the message is shifted by the specified key value. 
    For example, let's encrypt the word "Mark" with a key of -2:
    
    Before encryption	After encryption
    M	                K
    A	                Y
    R	                P
    K	                J
    The encryption is performed within the range of letters of the Latin alphabet. 
    If a letter needs to be shifted beyond the end of the alphabet, it wraps around 
    to the beginning. For instance, to encrypt the letter 'A' with a key of -2, we 
    move back to the end of the alphabet, resulting in the letter 'Y'.
    
    Decryption
    Decryption is the reverse process of encryption. To decrypt a message, each character
    is shifted back by the key value. In the example above, if the key used for encryption
    was -2, then for decryption, we shift each letter by +2.
    
    Caesar's cipher is a symmetric cipher, meaning the same key is used for both encryption 
    and decryption. It is also a substitution cipher, where letters retain their positions 
    but are substituted with others based on the key.
    

### Morse cipher
    The Morse Cipher is a simple substitution cipher that encodes letters, numbers, and symbols into
    a unique sequence of dots and dashes. In this cipher, each character is represented by a specific
    combination of dots (.) and dashes (-). The Morse Code was historically used for efficient and 
    accurate communication, especially in telegraphy.

    Encoding
    In Morse Code, each letter of the alphabet, as well as numbers and certain symbols, is assigned
    a distinct sequence. For example:
    
    "A" is represented by ".-"
    "B" is represented by "-..."
    "1" is represented by ".----"
    "/" is represented by "-..-."
    The length of the dots and dashes, as well as the pauses between them, is standardized to 
    facilitate clear and reliable communication.
    
    Encryption
    To encrypt a message using the Morse Cipher, each character in the text is replaced with its 
    corresponding Morse Code sequence. The individual Morse Code representations of the characters
    are then combined with spaces to separate words.
    
    For example, the word "HELLO" would be encrypted as ".... . .-.. .-.. ---".
    
    Decoding
    Decoding a Morse Code message involves reversing the process. The encoded message, consisting
    of dots, dashes, and spaces, is split into individual Morse Code representations of characters.
    Each Morse Code sequence is then matched to its corresponding character based on the Morse Code table.
    
    Decryption
    To decrypt a Morse Code message back into plain text, each Morse Code sequence is replaced with its 
    corresponding character. The resulting characters are combined to reconstruct the original message.
    
    For example, the Morse Code ".... . .-.. .-.. ---" would be decrypted back to "HELLO".

### Swap cipher
    The Swap Cipher is a simple encryption technique that involves swapping adjacent characters in a string. 
    This cipher is a form of transposition cipher where the positions of characters are rearranged. 
    Let's delve into how the encoding process works:

    Encoding
    The encoding process of the Swap Cipher takes a string and swaps each character with its adjacent character.
    For example, let's consider the string "HELLO":

    Before encoding	After encoding
    H	            E
    E	            H
    L	            L
    L	            O
    O	            L
    The adjacent characters are swapped, and this process continues throughout the entire string.
    Decoding encoded string is as simple as passing encoded string into the encode function again.

