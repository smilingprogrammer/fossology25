import os
import spacy
import pandas as pd


model_dir = ""
declutter_model_path = os.path.join("declutter_model")
declutter_model = spacy.load(declutter_model_path)


def declutter(data, predictions):
    """
    Cleans up a copyright notice by removing extra text based on the
    predictions.

    Parameters:
    data (iterable): The data to declutter.
    predictions (list): The predictions indicating false positives.

    Returns:
    list: The decluttered data.
    """

    # Iterate over each sentence and its corresponding prediction
    # Remove text from sentences marked as false positives, and keep the
    # entities (copyrights) in other sentences
    return [
        (
            ""
            if prediction == "f"
            else " ".join(
                [ent.text for ent in declutter_model(sentence).ents]
            )
        )
        for sentence, prediction in zip(data, predictions)
    ]

# imput_prompt = "Copyright (C) 1989, 1991 Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed."
# input_prompt = "copyright  copyrightsymbol   date    date   entity     franklin street  fifth floor  boston  ma  date    date  usa everyone is permitted to copy and distribute verbatim copies of this license document  but changing it is not allowed"
data = pd.read_csv('data/preprocessed_copyrights.csv')
data = data['original_content']
# print(data.head())
decl = declutter(data, ["f"] * len(data))

new_df = pd.DataFrame({
    'original_content': data,
    'decluttered_content': decl
})
new_df.to_csv('data/decluttered_copyrights.csv')
