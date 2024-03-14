class CaesarCipher:
    """
    Class contains methods to encrypt and decrypt string using Caesar cipher
    """

    def __init__(self, k: int) -> None:
        """
        Initializes the k(key) parameter
        :param k: Integer value to shift elements in a string
        """
        self.k = k

    def encrypt(self, text: str) -> str:
        """
        Encrypts a text using the Caesar cipher with the specified key.

        :param text: Text to be encrypted.
        :return: Encrypted text.
        """
        # Check if the key is within the valid range
        if not (-26 <= self.k <= 26):
            raise ValueError("Key must be a value between -26 and 26")

        encrypted_text = ""
        for char in text:
            if char.isalpha():  # Check if the character is a letter
                is_upper = char.isupper()
                offset = ord('A' if is_upper else 'a')

                encrypted_char = chr((ord(char) - offset + self.k) % 26 + offset)
                encrypted_text += encrypted_char
            else:
                encrypted_text += char  # Leave non-alphabetic characters unchanged

        return encrypted_text

    def decrypt(self, text: str) -> str:
        """
        Decrypts a text using the Caesar cipher with the specified key.

        :param text: Text to be decrypted.
        :return: Decrypted text.
        """
        if not (-26 <= self.k <= 26):
            raise ValueError("Key must be a value between -26 and 26")

        decrypted_text = ""
        for char in text:
            if char.isalpha():  # Check if the character is a letter
                is_upper = char.isupper()
                offset = ord('A' if is_upper else 'a')

                decrypted_char = chr((ord(char) - offset - self.k) % 26 + offset)
                decrypted_text += decrypted_char
            else:
                decrypted_text += char  # Leave non-alphabetic characters unchanged

        return decrypted_text

