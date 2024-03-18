from collections import UserDict

from personal_assistant.src.exceptions.exceptions import NoValue
from personal_assistant.src.utils import get_birthdays_num_days


def error_handler(function):
    def handle(self, *args, **kwargs):
        try:
            return function(self, *args, **kwargs)
        except KeyError:
            raise KeyError(f"The contacts book doesn't have a contact named {args[0]}")
        except NoValue as err:
            raise NoValue from err
        except TypeError:
            raise TypeError("Record details not provided.")
        except:
            raise Exception("Something went wrong.")

    return handle


class Contacts(UserDict):

    def __init__(self):
        super().__init__()
        self.data = {}

    @property
    def size(self):
        return len(self.data)

    @error_handler
    def add_record(self, record):
        self.data.update({str(record.name): record})

    @error_handler
    def find(self, name=None):
        if not name:
            raise NoValue("The name of a contact not provided.")
        return self.data[name]

    @error_handler
    def delete(self, name=None):
        if not name:
            raise NoValue("The name of a contact not provided.")
        self.data.pop(name)

    @error_handler
    def birthdays_num_days(self, days):
        users = [user for user in self.data.values()]
        birthdays = get_birthdays_num_days(users, days)
        return birthdays
