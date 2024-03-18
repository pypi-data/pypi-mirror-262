import re
from datetime import datetime

from personal_assistant.src.exceptions.exceptions import (
    WrongDate,
    WrongEmail,
    WrongAddress,
)


class Field:
    def __init__(self, value):
        self.value = self._has_validated(value)

    @staticmethod
    def _has_validated(value):
        """
        Field validation default implementation to be invoked
        :param value: value to validate
        :return: value
        """
        return value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone: str):
        super().__init__(phone)

    @staticmethod
    def _has_validated(value):
        return re.match(r"^[0-9]{10}$", value).group(0)


class Birthday(Field):
    def __init__(self, birthday: str):
        super().__init__(birthday)

    @staticmethod
    def _has_validated(value):
        try:
            birthday = re.match(
                r"^[0-3]{1}[0-9]{1}\.[0-1]{1}[0-9]{1}\.[0-9]{4}$", value
            ).group(0)
            return datetime.strptime(birthday, "%d.%m.%Y")
        except (AttributeError, ValueError):
            raise WrongDate("The date must be of the DD.MM.YYYY format. Try again.")


class Email(Field):
    def __init__(self, email: str):
        super().__init__(email)

    @staticmethod
    def _has_validated(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            raise WrongEmail(
                "Invalid email address format. Please enter the email address in the format example@example.com"
            )
        return email


class Address(Field):
    def __init__(self, address: str):
        super().__init__(address)

    @staticmethod
    def _has_validated(address):
        pattern = r"^.{10,100}$"
        if not re.match(pattern, address):
            raise WrongAddress(
                "Invalid address format - it must be between 10 and 100 characters long. "
                + "Please enter the house number, street, city, and postal code'."
            )
        return address
