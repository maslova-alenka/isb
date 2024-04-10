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