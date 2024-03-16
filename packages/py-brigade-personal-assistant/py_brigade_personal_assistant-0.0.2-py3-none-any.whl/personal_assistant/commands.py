import random
from functools import wraps

from personal_assistant.src.contacts.record import Record
from personal_assistant.src.exceptions.exceptions import (
    WrongInfoException,
    NoValue,
    WrongDate,
    WrongEmail,
    WrongAddress,
)
from personal_assistant.src.personal_assistant import personal_assistant
from personal_assistant.src.utils import (
    check_args,
    wrong_input_handling,
    get_contact,
    pre_check_addr,
)


def greeting():
    ## select and play a greeting reaction
    prompt = random.choice(["Hello!", "Hi!", "Greetings!"])
    return prompt


def farewell():
    prompt = random.choice(
        [
            "Bye!",
            "Good Bye!",
            "See you!",
            "Have a good one!",
            "Farewell!",
            "Ok, ok.. Get out!",
        ]
    )
    return prompt


def exit_assistant():
    personal_assistant.cache_data()
    print(farewell())
    exit()


def cache_data(command):
    @wraps(command)
    def wrapper(*args, **kwargs):
        result = command(*args, **kwargs)
        personal_assistant.cache_data()
        return result

    return wrapper


@cache_data
@wrong_input_handling
def add_contact(args):
    check_args(args, WrongInfoException())

    name = args[0]
    phone = args[-1]

    if name in list(personal_assistant.contacts.data.keys()):

        book_entry = personal_assistant.contacts.data[name]
        try:
            if book_entry.find_phone(phone):
                return "This phone number is already associated with this contact."
        except:
            pass

        confirm = input("A contact with this name found. Update it? yes / no: ")

        if confirm.lower() in ["yes", "1", "affirmative", "y"]:
            book_entry.add_phone(args[-1])
        else:
            return "Cancelling contact addition."

    else:
        contact = Record(name)
        contact.add_phone(args[-1])
        personal_assistant.contacts.add_record(contact)

    return "Contact added."


@wrong_input_handling
def find_contact(args):
    check_args(args, AttributeError())
    query = args[0]

    def match_item(record: Record):
        match = (
            True
            if (
                query in str(record.name)
                or query in str(record.address)
                or True
                in [query in email for email in record.list_str_rep(record.emails)]
                or True
                in [query in phone for phone in record.list_str_rep(record.phones)]
            )
            else False
        )
        return match

    matching_contacts = list(
        filter(match_item, personal_assistant.contacts.data.values())
    )
    message = "Contacts found:\n" + "\n".join(
        [str(contact) for contact in matching_contacts]
    )
    return message


@cache_data
@wrong_input_handling
def change_contact(args):
    check_args(args, ValueError())

    contact = get_contact(personal_assistant, args[0])
    contact.edit_phone(args[1], args[-1])
    return "Contact updated."


@wrong_input_handling
def show_phone(args):
    check_args(args, NoValue())
    contact = get_contact(personal_assistant, args[0])
    found_phones = contact.list_str_rep(contact.phones)
    found_phones = "; ".join(found_phones)
    return f"{args[0]}'s phone numbers: {found_phones}"


@wrong_input_handling
def show_all():
    add_phone_message = 'Enter "add <name> <number>" to add a contact.'
    if not personal_assistant.contacts.data:
        return "No contacts found. " + add_phone_message
    separator = f"{'-' * 4}|{'-' * 22}|{'-' * 62}|"

    def compose_message(name: str, item: any):

        line = "{:>3} | {:^20} | {:^60} |\n".format("", name, item)
        return line

    all_records = []

    for i, record in enumerate(personal_assistant.contacts.data.values()):
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
    return "\n".join(all_records) + "\n" + separator


@cache_data
@wrong_input_handling
def add_bd(args):
    check_args(args, WrongDate())
    contact = get_contact(personal_assistant, args[0])
    contact.add_birthday(args[1])
    return "Birthday date added."


@wrong_input_handling
def show_birthday(args):
    check_args(args, NoValue())
    contact = get_contact(personal_assistant, args[0])
    bd = contact.birthday
    if bd:
        bd = str(bd)
        return f"{args[0]}'s birthday: {bd}"
    return "No associated birthday date found."


@wrong_input_handling
def birthdays_num_days(args):
    if not args:
        days = 7
    else:
        try:
            days = int(args[0])

        except Exception:
            raise WrongInfoException(
                "Please provide a single valid digit for the number of days."
            )
    birthdays = personal_assistant.contacts.birthdays_num_days(days)
    return "\n".join(birthdays)


@cache_data
@wrong_input_handling
def remove_number(args):
    check_args(args, WrongInfoException())
    contact = get_contact(personal_assistant, args[0])
    contact.remove_phone(args[-1])
    return f"The number was deleted from {args[0]}'s list of phone numbers."


@cache_data
@wrong_input_handling
def del_contact(args):
    check_args(args, NoValue())
    personal_assistant.contacts.delete(args[0])
    return "The contact was deleted."


@wrong_input_handling
def num_records():
    message = f"The Contacts has {personal_assistant.contacts.size} entries. "
    if not personal_assistant.contacts.size:
        return message + 'Enter "add <name> <number>" to add a contact.'
    else:
        return message + 'Type "all" to list all of them.'


@cache_data
@wrong_input_handling
def add_email(args):
    check_args(args, WrongEmail())
    contact = get_contact(personal_assistant.contacts, args[0])
    contact.add_email(args[1])
    return f"Email address {args[1]} added successfully to contact {args[0]}."


@cache_data
@wrong_input_handling
def change_email(args):
    if len(args) == 2:
        raise NoValue("Please provide a name, and old + new email addresses.")
    else:
        check_args(args, WrongEmail())
    contact = get_contact(personal_assistant.contacts, args[0])
    contact.change_email(args[1], args[2])
    return f"Email address updated successfully for contact {args[0]}."


@wrong_input_handling
def show_email(args):
    check_args(args, NoValue())
    contact = get_contact(personal_assistant.contacts, args[0])
    found_emails = contact.list_str_rep(contact.emails)
    if found_emails:
        found_emails = "; ".join(found_emails)
        return f"{args[0]}'s emails: {found_emails}"
    else:
        return "No emails found."


@cache_data
@wrong_input_handling
def delete_email(args):
    check_args(args, WrongEmail())
    contact = get_contact(personal_assistant.contacts, args[0])
    contact.delete_email(args[1])
    return "The email address was deleted."


@cache_data
@wrong_input_handling
def add_address(args):
    try:
        address = pre_check_addr(args)
    except IndexError:
        raise WrongAddress("Please provide both a name and address.")
    contact = personal_assistant.contacts.find(args[0])
    contact.add_address(address)
    return f"Address was added successfully to contact {args[0]}."


@cache_data
@wrong_input_handling
def change_address(args):
    try:
        address = pre_check_addr(args)
    except IndexError:
        raise WrongAddress("Please provide both a name and address.")
    contact = get_contact(personal_assistant, args[0])
    contact.change_address(address)
    return f"Address updated successfully for contact {args[0]}."


@wrong_input_handling
def show_address(args):
    check_args(args, NoValue())
    contact = get_contact(personal_assistant, args[0])
    add = contact.address
    if add:
        add = str(add)
        return f"{args[0]}'s address: {add}"
    return "No associated address found."


@cache_data
@wrong_input_handling
def delete_address(args=None):
    if not args:
        raise NoValue("No name was provided. Try again.")
    contact = get_contact(personal_assistant.contacts, args[0])
    contact.delete_address()
    return "The address was deleted."


@cache_data
@wrong_input_handling
def add_note():
    return personal_assistant.notes.add_note()


@cache_data
@wrong_input_handling
def remove_note():
    note_name = input("Enter the name of the note to delete: ")
    return personal_assistant.notes.remove_note(note_name)


@wrong_input_handling
def show_notes():
    return personal_assistant.notes.get_all_notes()


@cache_data
@wrong_input_handling
def edit_note():
    note_name = input("Enter the name of the note you want to edit: ")
    new_text = input("Enter the new text for the note: ")
    return personal_assistant.notes.edit_note(note_name, new_text)


@wrong_input_handling
def search_note():
    search_term = input("Enter search query: ")
    return personal_assistant.notes.search_note(search_term)
