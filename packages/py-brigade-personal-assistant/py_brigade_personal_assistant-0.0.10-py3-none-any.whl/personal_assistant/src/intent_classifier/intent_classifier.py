from keras.utils import pad_sequences
import numpy as np
import os
import pathlib
import pickle
import keras


class IntentClassifier:
    def __init__(self):
        res_pth = pathlib.Path(__file__).parents[2].joinpath("resources")
        # Load tokenizer
        with open(os.path.join(res_pth, "tokenizer_v6.bin"), "rb") as handle:
            self.tokenizer = pickle.load(handle)
        # Load preprocessing parameters
        with open(os.path.join(res_pth, "preprocessing_params_v6.bin"), "rb") as handle:
            self.preprocessing_params = pickle.load(handle)

        self.model = keras.models.load_model(os.path.join(res_pth, "intent_cat_v6"))
        self.labels_dict = {
            0: "delete-email",
            1: "find-note",
            2: "add-contact",
            3: "birthdays",
            4: "add-email",
            5: "add-note",
            6: "delete-note",
            7: "change-phone",
            8: "change-email",
            9: "show-all",
            10: "remove-phone",
            11: "show-all-notes",
            12: "add-birthday",
            13: "find-contact",
            14: "delete-contact",
            15: "edit-note",
            16: "show-birthday",
        }

    def predict(self, sentence="i want to add a new contact"):

        self.PAD = self.preprocessing_params["PAD"]
        self.TRUNC = self.preprocessing_params["TRUNC"]
        self.MAX_LEN = self.preprocessing_params["MAX_LEN"]

        test_sentence = [sentence]

        test_sequence = self.tokenizer.texts_to_sequences(texts=test_sentence)

        test_sequence = pad_sequences(
            test_sequence, padding=self.PAD, truncating=self.TRUNC, maxlen=self.MAX_LEN
        )
        predicted = self.model.predict(test_sequence, verbose=0)
        probable_intent_key = np.where(predicted[0] == max(predicted[0]))[0][0]
        probable_intent = self.labels_dict[probable_intent_key]
        return probable_intent
