import math
import os

from working_with_a_file import *

PI = {0: 0.2148, 1: 0.3672, 2: 0.2305, 3: 0.1875}


def frequency_test(path: str, path_write: str, key: str) -> None:
    """
    Performs a frequency test on a binary sequence and writes the result to a file.

    Parameters:
        path: the path to the JSON file containing the binary sequence.
        path_write: the path to write the result of the test.
        key: the key in the dictionary to the binary sequence.
    """
    b_sequence = read_json(path)
    try:
        sequence = [-1 if bit == "0" else 1 for bit in b_sequence.get(key)]
        s_n = sum(sequence) / math.sqrt(len(sequence))
        p_value = math.erfc(math.fabs(s_n) / math.sqrt(2))
        write_file(path_write, f'{key} : {p_value}\n')
    except Exception as e:
        print("Error when performing a frequency bitwise test: ", e)


def same_bits_test(path: str, path_write: str, key: str) -> None:
    """
    Performs a test for the same consecutive bits and writes the result to a file.

    Parameters:
        path: the path to the JSON file containing the binary sequence.
        path_write: the path to write the result of the test.
        key: the key in the dictionary to the binary sequence.
    """
    sequence = read_json(path)
    try:
        n = len(sequence.get(key))
        ones_count = sequence.get(key).count("1")
        zita = ones_count / n
        if abs(zita - 0.5) < (2 / math.sqrt(len(sequence.get(key)))):
            v = 0
            for bit in range(len(sequence.get(key)) - 1):
                if sequence.get(key)[bit] != sequence.get(key)[bit + 1]:
                    v += 1
            numerator = abs(v - 2 * n * zita * (1 - zita))
            denominator = 2 * math.sqrt(2 * n) * zita * (1 - zita)
            p_value = math.erfc(numerator / denominator)
        else:
            p_value = 0
        write_file(path_write, f'{key} : {p_value}\n')
    except Exception as e:
        print("An error occurred when performing a test for the same consecutive bits: ", e)


if __name__ == "__main__":
    frequency_test(os.path.join('sequence.json'), os.path.join('result.txt'), 'java')
    frequency_test(os.path.join('sequence.json'), os.path.join('result.txt'), 'c++')

    same_bits_test(os.path.join('sequence.json'), os.path.join('result.txt'), 'java')
    same_bits_test(os.path.join('sequence.json'), os.path.join('result.txt'), 'c++')