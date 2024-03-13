import json
import os
from working_with_a_file import*


alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def atbash_cipher(text_path: str, path: str) -> None:
    """
    Atbash cipher

    Parameters
        text: message
    Returns
        encrypted message
    """
    reversed_alphabet = alphabet[::-1]
    result = ''
    text = read_file(text_path)
    for char in text:
        if char in alphabet:
            index = alphabet.index(char)
            result += reversed_alphabet[index]
        else:
            result += char

    write_file(path, result)


def frequency_analysis(text: str) -> dict:
    """
    Performs a frequency analysis of the text and returns a sorted
    dictionary with the frequency of each character.
    """
    frequencies = {}
    total_chars = len(text)
    for char in text:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
    for char, count in frequencies.items():
        frequencies[char] = count / total_chars
    sorted_freq = dict(sorted(frequencies.items(), key=lambda x: x[1], reverse=True))
    return sorted_freq


def key_json(path: str) -> None:
    reversed_alphabet = alphabet[::-1]
    key = dict()
    for i, char in enumerate(alphabet):
        key[char] = reversed_alphabet[i]
    write_json(key, path)


def decryption(path_encryption: str, path_key: str, path_decryption: str):
    key = read_json(path_key)
    decrypted_text = ''
    text = read_file(path_encryption)
    for char in text:
        if char in key:
            decrypted_text += key[char]
        else:
            decrypted_text += char
    write_file(path_decryption, decrypted_text)


if __name__ == "__main__":
    atbash_cipher(os.path.join('text', 'first_task', 'text.txt'),
                  os.path.join('text', 'first_task', 'encryption.txt'))

    key_json(os.path.join('text', 'first_task', 'key.json'))

    decryption(os.path.join('text', 'first_task', 'encryption.txt'),
               os.path.join('text', 'first_task', 'key.json'),
               os.path.join('text', 'first_task', 'decryption.txt'))


