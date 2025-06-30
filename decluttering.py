import os
import spacy


model_dir = ""
declutter_model_path = os.path.join(model_dir, "declutter_model")
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

output = declutter("Copyright (C) 1989, 1991 Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.", "f")
print(output)