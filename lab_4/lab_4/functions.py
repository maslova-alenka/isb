import multiprocessing as mp
import hashlib


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
                print(f"Номер подобранной карты при количестве процессов = {count_process} : {result}")
                p.terminate()
                return result


def luhn_algorithm(card_number: str) -> bool:
    digits = [int(digit) for digit in reversed(card_number)]
    for i in range(1, len(digits), 2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] = (digits[i] // 10) + (digits[i] % 10)
    return sum(digits) % 10 == 0
