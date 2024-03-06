alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
reversed_alphabet = "ЯЮЭЬЫЪЩШЧЦХФУТСРПОНМЛКЙИЗЖЁЕДГВБА"


def atbash_cipher(text: str) -> str:
    """
    Atbash cipher

    Parameters
        text: message
    Returns
        encrypted message
    """
    result = ''

    for char in text:
        if char in alphabet:
            index = alphabet.index(char)
            result += reversed_alphabet[index]
        else:
            result += char

    return result


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
