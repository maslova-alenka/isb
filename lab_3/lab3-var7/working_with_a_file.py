import json


def read_json(path: str) -> dict:
    """
    A function for reading data from a JSON file and returning a dictionary.

    Parameters
        path: the path to the JSON file to read

    Returns
        Dictionary of data from a JSON file
    """
    try:
        with open(path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("The file was not found")
    except Exception as e:
        print(f"An error occurred while reading the JSON file: {str(e)}")


def read_file(path: str) -> str:
    """
    A function for reading the contents of a file and returning it as a string.

    Parameters
        path: the path to the file to read
    Returns
        A line with the contents of the file
    """
    try:
        with open(path, "r", encoding='UTF-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print("The file was not found")
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")


def write_file(path: str, data: str) -> None:
    """
    A function for writing data to a file.

    Parameters
        path: the path to the file to write
        data: data to write to a file
    """
    try:
        with open(path, "a+", encoding='UTF-8') as file:
            file.write(data)
        print(f"The data has been successfully written to the file '{path}'.")
    except Exception as e:
        print(f"An error occurred while writing the file: {str(e)}")


def read_bytes(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        data = file.read()
    return data


def write_bytes_text(file_path: str, bytes_text: bytes) -> None:
    with open(file_path, "wb") as file:
        file.write(bytes_text)


def serialize_sym_key(path: str, key) -> None:
    with open(path, 'wb') as key_file:
        key_file.write(key)


def deserialization_sym_key(path: str) -> bytes:
    with open(path, mode='rb') as key_file:
        return key_file.read()

