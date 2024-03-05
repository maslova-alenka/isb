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
