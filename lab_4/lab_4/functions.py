import hashlib
import multiprocessing as mp
import time
import working_with_a_file

from matplotlib import pyplot as plt
from tqdm import tqdm


def check_card_number(part: int, bins: list, last_digit: int, original_hash: str) -> str:
    """
    Checks if the given part of the card number can be the full card number.

    Parameters
        part: The part of the card number to check.
        bins: A list of possible card number prefixes (BINs).
        last_digit: The last digit of the card number.
        original_hash:The hash value of the full card number to find a match for.
    Returns
        The full card number
    """
    for card_bin in bins:
        card_number = f"{card_bin}{str(part).zfill(6)}{last_digit}"
        if hashlib.sha256(card_number.encode()).hexdigest() == original_hash:
            return card_number


def get_card_number(original_hash: str, bins: list, last_digit: int, count_process: int = mp.cpu_count()) -> str:
    """
    Finds the full card number by checking all possible combinations of the given parameters.

    Parameters:
        original_hash: The hash value of the full card number to find a match for.
        bins: A list of possible card number prefixes (BINs).
        last_digit: The last digit of the card number.
        count_process: The number of processes to use for the search. Defaults to the number of CPUs available.
    Returns:
        The full card number
    """
    with mp.Pool(count_process) as p:
        for result in p.starmap(check_card_number,
                                [(i, bins, last_digit, original_hash) for i in list(range(0, 999999))]):
            if result:
                print(f"The number of the selected card with the number of processes = {count_process} : {result}")
                p.terminate()
                return result


def luhn_algorithm(card_number: str) -> bool:
    """
    Validates a credit card number using the Luhn algorithm.

    Parameters:
        card_number: The credit card number to validate.
    Returns:
        True if the credit card number is valid, False otherwise.
    """
    digits = [int(digit) for digit in reversed(card_number)]
    for i in range(1, len(digits), 2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] = (digits[i] // 10) + (digits[i] % 10)
    return sum(digits) % 10 == 0


def graphing(original_hash: str, bins: list, last_digit: int) -> None:
    """
    Plots a graph of the execution time of the `get_card_number` function based on the number of processes used.

    Parameters:
        original_hash: The hash value of the full card number to find a match for.
        bins: A list of possible card number prefixes (BINs).
        last_digit: The last digit of the card number.
    """
    time_list = list()
    for count_process in tqdm(range(1, int(mp.cpu_count() * 1.5)), desc="Finding a collision"):
        start_time = time.time()
        if get_card_number(original_hash, bins, last_digit, count_process):
            time_list.append(time.time() - start_time)
    fig = plt.figure(figsize=(30, 5))
    plt.ylabel('Time, s')
    plt.xlabel('Processes')
    plt.title("Statistics")
    plt.plot(range(1, int(mp.cpu_count() * 1.5)), time_list, color='lime', linestyle='--', marker='*',
             linewidth=1, markersize=8)
    plt.show()


if __name__ == "__main__":
    setting = working_with_a_file.read_json("parametrs_card.json")
    number = working_with_a_file.read_json("card.json")
    print(f"The card number is correct: {luhn_algorithm(number["card_number"])}")
    graphing(setting["hash"], setting["bins"], setting["last_numbers"])
    get_card_number(setting["hash"], setting["bins"], setting["last_numbers"])
