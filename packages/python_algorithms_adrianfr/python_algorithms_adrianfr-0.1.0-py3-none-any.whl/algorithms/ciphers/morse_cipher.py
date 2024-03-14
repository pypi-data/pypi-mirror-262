

class MorseCipher:

    def __init__(self) -> None:
        self.morse_code = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
            'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
            'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..',
            '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.', '0': '-----',
            ' ': '/'
        }

    def text_to_morse(self, text: str) -> str:
        """
        Converts a text to Morse code.

        :param text: Text to be converted to Morse code.
        :return: Morse code representation of the input text.
        """
        morse_code_list = [self.morse_code[char.upper()] for char in text if char.upper() in self.morse_code]
        return ' '.join(morse_code_list)

    def morse_to_text(self, encoded_text: str) -> str:
        """
        Converts a Morse code to original text.

        :param encoded_text: Encrypted text to be converted into original text.
        :return: Original text
        """
        return ''.join([char for code in encoded_text.split(' ') for char, morse in self.morse_code.items() if morse == code])
