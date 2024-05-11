import hashlib
import multiprocessing as mp
import time
import working_with_a_file

from matplotlib import pyplot as plt
from tqdm import tqdm


def check_card_number(part: int, bins: list, last_digit: int, original_hash: str) -> str | None:
    for card_bin in bins:
        card_number = f"{card_bin}{str(part).zfill(6)}{last_digit}"
        if hashlib.sha256(card_number.encode()).hexdigest() == original_hash:
            return card_number


def get_card_number(original_hash: str, bins: list, last_digit: int, count_process: int = mp.cpu_count()):
    with mp.Pool(count_process) as p:
        for result in p.starmap(check_card_number,
                                [(i, bins, last_digit, original_hash) for i in list(range(0, 999999))]):
            if result:
                print(f"The number of the selected card with the number of processes = {count_process} : {result}")
                p.terminate()
                return result


def luhn_algorithm(card_number: str) -> bool:
    digits = [int(digit) for digit in reversed(card_number)]
    for i in range(1, len(digits), 2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] = (digits[i] // 10) + (digits[i] % 10)
    return sum(digits) % 10 == 0


def graphing(original_hash: str, bins: list, last_digit: int) -> None:
    time_list = list()
    for count_process in tqdm(range(1, int(mp.cpu_count() * 1.5)), desc="Finding a collision"):
        start_time = time.time()
        if get_card_number(original_hash, bins, last_digit, count_process):
            time_list.append(time.time() - start_time)
    fig = plt.figure(figsize=(30, 5))
    plt.ylabel('Time, s')
    plt.xlabel('Processes')
    plt.title("Statistics")
    plt.plot(range(1, int(mp.cpu_count() * 1.5)), time_list, color='lime', linestyle='--', marker='x',
             linewidth=2, markersize=8)
    plt.show()


if __name__ == "__main__":
    setting = working_with_a_file.read_json("parametrs.json")
    o_h = "70ba6e37c3be80134c2fd8563043c0cb9278a43116b3bc2dfad03e2e455ed473"
    b = [413064, 415028, 427230, 427275, 429749, 446674, 462017, 462043, 489327]
    #graphing(o_h, b, 1378)

    get_card_number(o_h, b, 1378, )
