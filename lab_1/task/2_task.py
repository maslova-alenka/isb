import os
from working_with_a_file import*


def frequency_analysis(text_path: str, path: str) -> None:
    """
    Performs a frequency analysis of the text and returns a sorted
    dictionary with the frequency of each character.
    """
    text = read_file(text_path)
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
    write_json(sorted_freq, path)


if __name__ == "__main__":
    frequency_analysis(os.path.join('text', 'second_task', 'text_second.txt'),
                       os.path.join('text', 'second_task', 'freq.json'))
