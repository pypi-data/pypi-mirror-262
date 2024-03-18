from datetime import datetime
import collections
from personal_assistant.src.exceptions.exceptions import (
    WrongInfoException,
    WrongDate,
    NoValue,
    NoPhones,
    WrongEmail,
    WrongAddress,
)


def wrong_input_handling(function):
    def handling(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except WrongInfoException as err:
            return err.args[0]
        except WrongDate as err:
            return err.args[0]
        except WrongEmail as err:
            return err.args[0]
        except WrongAddress as err:
            return err.args[0]
        except NoValue as err:
            return err.args[0]
        except NoPhones as err:
            return err.args[0]
        except AttributeError as err:
            return err.args[0]
        except KeyError as err:
            return err.args[0]
        except ValueError as err:
            return err.args[0]
        except TypeError as err:
            return err.args[0]
        except Exception as err:
            return err.args[0]

    return handling


def get_contact(book, name):
    try:
        contact = book.contacts[name]
        return contact
    except KeyError:
        raise KeyError(f"The contacts book doesn't have a contact named {name}")


def check_args(args, exc: Exception):
    if isinstance(exc, WrongInfoException):
        if len(args) == 1:
            raise WrongInfoException("Please provide both a name and a phone number.")

        elif len(args) < 1:
            raise WrongInfoException(
                "Neither name nor phone number provided. Please try again."
            )
    elif isinstance(exc, WrongEmail):
        if len(args) == 1:
            raise WrongEmail("Please provide both a name and email.")

        elif len(args) < 1:
            raise WrongEmail("Neither name nor email was provided. Please try again.")

    elif isinstance(exc, WrongAddress):
        if len(args) == 1:
            raise WrongAddress("Please provide both a name and adress.")

    elif isinstance(exc, WrongDate):
        if len(args) == 1:
            raise WrongDate("Please provide both a name and a date.")

        elif len(args) < 1:
            raise WrongDate("Neither name nor date was provided. Please try again.")

    elif isinstance(exc, NoValue):
        args = args[0].split()
        if len(args) != 1:
            raise NoValue("Please provide a contact name only.")

    elif isinstance(exc, ValueError):
        if len(args) == 2:
            raise ValueError("Please provide both old and new phone numbers.")

        elif 1 < len(args) < 2:
            raise ValueError(
                "Neither old nor new phone number provided. Please try again."
            )

        elif len(args) <= 1:
            raise ValueError(
                "Please provide an account name, old and new phone numbers."
            )

    elif isinstance(exc, AttributeError):
        args = args[0].split()
        if len(args) < 1:
            raise WrongInfoException("No search query was provided. Please try again.")
        elif len(args) > 1:
            raise WrongInfoException(
                "More than one search query found. Please enter one search query."
            )


def pre_check_addr(args):
    if args[1:]:
        address = " ".join(args[1:])
        return address
    else:
        raise IndexError


# def parser(user_input):
#     if user_input == "":
#         return None, None, "Please start with a valid command."
#     print(personal_assistant.classifier.predict(user_input))
#     command, *args = user_input.split()
#     command = command.lower().strip()
#     return command, *args, None


def get_birthdays_num_days(users: list[any], days: int = ...):
    bds_num_days = collections.defaultdict(list)
    current_date = datetime.today().date()
    birthdays = []

    for user in users:
        if user.birthday:
            user_bd = user.birthday.value.date()
            bd_this_year = user_bd.replace(year=current_date.year)
        else:
            continue

        if bd_this_year < current_date:
            bd_this_year = bd_this_year.replace(year=current_date.year + 1)

        days_delta = (bd_this_year - current_date).days

        if days_delta < days:
            day_to_congrats = bd_this_year.strftime("%A")

            ## if the function is run on Sunday and the BD is in 6 days
            if days_delta == days - 1 and day_to_congrats in ["Saturday", "Sunday"]:
                day_to_congrats = "Next Monday"
            elif day_to_congrats in ["Saturday", "Sunday"]:
                day_to_congrats = "Monday"

            bds_num_days[day_to_congrats].append([user.name.value, user.birthday.value])
    if len(bds_num_days) > 0:
        ## print out the list of names per day for the next num days
        for day, names in bds_num_days.items():
            for name in names:
                date_of_birth = name[1].strftime("%Y-%m-%d")
                birthdays.append(
                    "{:<10} | {:^15} : {:^15}".format(day, date_of_birth, name[0])
                )
    else:
        birthdays.append(f"No birthdays within the next {days} days.")

    ## in case the list is needed elsewhere
    return birthdays


def compose_contacts_list(found_contacts, all_records: list):
    separator = f"{'-' * 4}|{'-' * 22}|{'-' * 62}|"

    def compose_message(name: str, item: any):

        line = "{:>3} | {:^20} | {:^60} |\n".format("", name, item)
        return line

    for i, record in enumerate(found_contacts):
        name = record.name.value
        all_records.append(
            separator
            + "\n{:>3} | {:^20} | {:^60} |\n".format(i + 1, "Name", name)
            + separator
        )

        phones = (
            "; ".join(p.value for p in record.phones)
            if record.phones
            else "No associated phones found"
        )
        emails = (
            "; ".join(e.value for e in record.emails)
            if record.emails
            else "No emails on record"
        )
        birthday = (
            str(record.birthday.value.date()) if record.birthday else "Not indicated"
        )
        address = (
            record.address.value if record.address else "No current address stored"
        )

        message = compose_message("Phone numbers", phones)
        message += compose_message("Emails", emails)
        message += compose_message("Birthday", birthday)
        message += compose_message("Address", address).rstrip("\n")
        all_records.append(message)

    return separator


def str_items(lst):
    return list(map(str, lst))
