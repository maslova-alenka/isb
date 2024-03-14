import os
from working_with_a_file import*
from task_1 import decryption


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


def combine_dicts(path1, path2, path_new):
    dict1 = read_json(path1)
    dict2 = read_json(path2)
    keys = dict1.keys()
    values = dict2.keys()
    new_dict = {key: value for key, value in zip(keys, values)}
    write_json(new_dict, path_new)


if __name__ == "__main__":
    frequency_analysis(os.path.join('text', 'second_task', 'text_second.txt'),
                       os.path.join('text', 'second_task', 'freq.json'))

    combine_dicts(os.path.join('text', 'second_task', 'freq.json'),
                  os.path.join('text', 'second_task', 'standard.json'),
                  os.path.join('text', 'second_task', 'key.json'))

    decryption(os.path.join('text', 'second_task', 'text_second.txt'),
               os.path.join('text', 'second_task', 'key.json'),
               os.path.join('text', 'second_task', 'text_decryption.txt'))
