from typing import List

def build_array_from_string(input_string: str, initial_object, final_value):
    keys = input_string.split('/')
    final = initial_object.copy()  # Copia l'oggetto iniziale per evitare modifiche indesiderate
    current_object = final

    for index, key in enumerate(keys):
        if index == len(keys) - 1:
            current_object[key] = final_value
        else:
            if key not in current_object:
                current_object[key] = {}
            current_object = current_object[key]

    return final

def add_amount_one(amounts: List[int]):
    amounts = amounts[:]  # Copia la lista di input per evitare modifiche indesiderate
    if 1 in amounts:
        amounts.remove(1)
    amounts.insert(0, 1)
    return amounts
