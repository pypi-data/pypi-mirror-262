import os
import random
import pathlib
import pickle

from personal_assistant.src.contacts.contacts import Contacts
from personal_assistant.src.notes.notes import Notes
from personal_assistant.src.intent_classifier.intent_classifier import IntentClassifier


_CACHE_DIR = pathlib.Path(__file__).parent.parent.joinpath(".cache")

os.makedirs(_CACHE_DIR, exist_ok=True)


class PersonalAssistant:

    def __init__(self):
        self._notes = Notes()
        self._contacts = Contacts()
        self._classifier = IntentClassifier()
        self._load_cache_data()

    @property
    def notes(self):
        return self._notes

    @property
    def contacts(self):
        return self._contacts

    @property
    def classifier(self):
        return self._classifier

    def cache_data(self):
        with open(_CACHE_DIR.joinpath("notes.bin"), "wb") as file:
            pickle.dump(self._notes, file)
        with open(_CACHE_DIR.joinpath("contacts.bin"), "wb") as file:
            pickle.dump(self._contacts, file)

    def _load_cache_data(self):
        notes_cache = _CACHE_DIR.joinpath("notes.bin")
        contacts_cache = _CACHE_DIR.joinpath("contacts.bin")

        if notes_cache.exists():
            with open(notes_cache, "rb") as file:
                cache = pickle.load(file)
                self._notes.data.extend(cache)

        if contacts_cache.exists():
            with open(contacts_cache, "rb") as file:
                cache = pickle.load(file)
                self._contacts.data.update(cache)


print(
    random.choice(
        [
            "\nLoading guns..",
            "\nChecking gadgets..",
            "\nIroning the tuxedo..",
            "\nDetecting bugs..",
            "\nServicing the Aston Martin..",
        ]
    )
)
personal_assistant = PersonalAssistant()
