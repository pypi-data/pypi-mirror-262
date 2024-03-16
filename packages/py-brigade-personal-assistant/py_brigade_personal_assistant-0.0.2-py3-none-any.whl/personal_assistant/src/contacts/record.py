from personal_assistant.src.contacts.fields import (
    Name,
    Phone,
    Email,
    Birthday,
    Address,
)
from personal_assistant.src.exceptions.exceptions import NoValue, WrongDate, WrongEmail


def error_handler(function):
    def handle(self, *args, **kwargs):
        try:
            return function(self, *args, **kwargs)
        except IndexError:
            raise IndexError("This phone number is not associated with this contact.")

        except NoValue as err:
            raise NoValue from err

        except TypeError:
            raise TypeError("The phone number(s) not provided. Try again.")

        except AttributeError:
            raise AttributeError(
                "The phone number must be 10 digits long " + "and contain only digits."
            )

        except WrongDate as err:
            raise WrongDate from err

        except WrongEmail as err:
            raise WrongEmail(err)

        except ValueError:
            raise ValueError(
                f"{args[0]} is not on the list of {self.name}'s phone numbers."
            )

        except:
            raise Exception("Something went wrong. Please try again.")

    return handle


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.emails = []
        self.address = None

    def __str__(self):
        address = self.address if self.address else "No associated address found"
        bd = self.birthday if self.birthday else "Not indicated"
        emails = (
            "; ".join(e.value for e in self.emails) if self.emails else "Not specified"
        )
        phones = (
            "; ".join(p.value for p in self.phones) if self.phones else "Not specified"
        )

        contact_str = (
            f"Contact name: {self.name.value}, phones: {phones}, "
            + f"emails: {emails}, address: {address}, birthday: {bd}"
        )
        return contact_str

    @staticmethod
    def list_str_rep(lst: list):
        return [str(i) for i in lst]

    @error_handler
    def add_phone(self, phone=None):
        if not phone:
            raise NoValue("No phone number was provided.")
        phone_num = Phone(phone)
        self.phones.append(phone_num)

    @error_handler
    def edit_phone(self, old_phone, new_phone):
        old_phone_index = self.list_str_rep(self.phones).index(old_phone)
        self.phones[old_phone_index] = Phone(new_phone)

    @error_handler
    def find_phone(self, phone=None):
        if not phone:
            raise NoValue("No phone number was provided.")
        found_phone_index = self.list_str_rep(self.phones).index(phone)
        found_phone = self.phones[found_phone_index]
        return found_phone

    @error_handler
    def remove_phone(self, phone=None):
        if not phone:
            raise NoValue("No phone number was provided.")
        found_phone_index = self.list_str_rep(self.phones).index(phone)
        self.phones.pop(found_phone_index)

    def add_birthday(self, birthday=None):
        if not birthday:
            raise NoValue("No birthday date was provided.")
        self.birthday = Birthday(birthday)

    @error_handler
    def add_email(self, email: str = None):
        if not email:
            raise NoValue("No email address was provided.")
        e_mail = Email(email)
        self.emails.append(e_mail)

    @error_handler
    def change_email(self, old_email, new_email):
        old_email_index = self.list_str_rep(self.emails).index(old_email)
        self.emails[old_email_index] = Email(new_email)

    def delete_email(self, email: str = None):
        if not email:
            raise NoValue("No email address was provided.")
        email_index = self.list_str_rep(self.emails).index(email)
        self.emails.pop(email_index)

    def add_address(self, address: str = None):
        if not address:
            raise NoValue("No address was provided.")
        self.address = Address(address)

    def change_address(self, new_address: str = ...):
        if not new_address:
            raise NoValue("No address was provided.")
        self.address = Address(new_address)

    def delete_address(self):
        self.address = None
