import re
import os
import spacy
import pandas as pd



model_dir = ""
# model_dir = (
#             model_dir
#             if model_dir
#             else (
#                 LOCAL_MODEL_DIR
#                 if use_local_model and os.path.exists(LOCAL_MODEL_DIR)
#                 else DEFAULT_MODEL_DIR
#             )
#         )

entity_recognizer_path = os.path.join(model_dir, "entity_recognizer")
entity_recognizer = spacy.load(entity_recognizer_path)
def _replace_entities(data):
    """
    Replaces detected copyright holder entities with ' ENTITY '.

    Uses the entity_recognizer model to identify copyright holder entities,
    which are often name or organization entities, and replaces them with
    the string ' ENTITY '.

    Parameters:
    data (list): A list of strings.

    Returns:
    list: A list of strings with copyright holder entities replaced.
    """

    new_data = []
    for sentence in data:
        # Process the sentence using the entity recognizer
        doc = entity_recognizer(sentence)
        new_sentence = doc.text
        for entity in doc.ents:
            # If the entity is a copyright holder entity, replace it with
            # ' ENTITY '
            if entity.label_ == "ENT":
                new_sentence = re.sub(
                    re.escape(entity.text), " ENTITY ", new_sentence
                )
        new_data.append(new_sentence)
    return new_data

def _perform_text_substitutions(data):
    """
    Performs a series of text substitutions to clean and standardize the
    data.

    This includes:
    - Replacing four-digit numbers (assumed to be years) with ' DATE '.
    - Removing all other numbers.
    - Replacing copyright symbols with ' COPYRIGHTSYMBOL '.
    - Replacing emails with ' EMAIL '.
    - Removing any special characters not already replaced or removed.
    - Converting text to lowercase.
    - Stripping extra whitespace from the text.

    Parameters:
    data (list): A list of strings.

    Returns:
    list: A list of cleaned and standardized strings.
    """

    # Define the substitution patterns and their replacements
    subs = [
        (r"\d{4}", " DATE "),
        (r"\d+", " "),
        (r"©", " COPYRIGHTSYMBOL "),
        (r"\(c\)", " COPYRIGHTSYMBOL "),
        (r"\(C\)", " COPYRIGHTSYMBOL "),
        (
            r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"
            (?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|
            \\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@
            (?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9]
            (?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|
            1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|
            1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(
            [\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|
            \\[\x01-\x09\x0b\x0c\x0e-\x7f])+)])""",
            " EMAIL ",
        ),
        (r"[^a-zA-Z0-9]", " "),
    ]
    # Perform the substitutions for each pattern in the list
    for pattern, replacement in subs:
        data = [
            re.sub(pattern, replacement, sentence) for sentence in data
        ]
    # Convert text to lowercase and strip extra whitespace
    return [sentence.lower().strip() for sentence in data]

def _ensure_list_of_strings(data):
    """
    Ensures the data is a list of strings.

    If the input data is not a list, attempts to convert it to a list.
    Then, ensures each element of the list is a string.

    Parameters:
    data (iterable): The data to be converted to a list of strings.

    Returns:
    list: A list of strings.
    """

    # If data is not a list, try converting it to a list
    if not isinstance(data, list):
        data = data.to_list()
    # Ensure each item in the list is a string
    return [str(item) for item in data]

def preprocess_data(data):
    """
    Preprocesses the given data by performing various text cleaning and
    transformation tasks.

    Parameters:
    data (iterable): The data to preprocess.

    Returns:
    data (list): List of preprocessed strings.
    """

    # Ensure the data is a list of strings
    data = _ensure_list_of_strings(data)

    # Replace copyright holder entities in the data
    data = _replace_entities(data)

    # Perform text substitutions for dates, numbers, symbols, emails, etc.
    data = _perform_text_substitutions(data)

    return data

data = pd.read_csv('copyrights.csv')
data = data['original_content']
# print(data.head())
prep = preprocess_data(data)
new_df = pd.DataFrame({
    'original_content': data,
    'preprocessed_content': prep
})
new_df.to_csv('data/preprocessed_copyrights.csv')
