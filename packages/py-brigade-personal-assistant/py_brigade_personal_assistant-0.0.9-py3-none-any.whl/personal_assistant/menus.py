from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

from personal_assistant.commands import (
    add_address,
    add_bd,
    add_contact,
    add_email,
    add_note,
    birthdays_num_days,
    change_address,
    change_contact,
    change_email,
    del_contact,
    delete_address,
    delete_email,
    edit_note,
    exit_assistant,
    find_contact,
    num_records,
    remove_note,
    remove_number,
    search_note,
    show_address,
    show_all,
    show_birthday,
    show_email,
    show_notes,
    show_phone,
)
from personal_assistant.src import messages
from personal_assistant.utils.utils import parser

contacts_commands = [
    "add",
    "delete",
    "remove",
    "find",
    "all",
    "num-contacts",
    "show-phone",
    "change-phone",
    "delete-phone",
    "remove-phone",
    "add-birthday",
    "show-birthday",
    "birthdays",
    "add-email",
    "change-email",
    "show-email",
    "delete-email",
    "add-address",
    "change-address",
    "show-address",
    "delete-address",
    "back",
    "return",
    "help",
    "-",
    "exit",
    "close",
]


def contacts_menu():
    while True:

        commands_completer = WordCompleter(contacts_commands)
        session = PromptSession(completer=commands_completer)
        user_input = session.prompt(
            "\nHow can I help you?\nEnter a command: contacts: "
        )
        command = parser(user_input)
        if command in ("exit", "close"):
            exit_assistant()

        if command in ("back", "return", "-"):
            return

        elif command == "help":
            print(messages.contacts_help_center)

        elif command in ("add-contact", "add-note"):
            print(add_contact())

        elif command in ("find-note", "find-contact"):
            print(find_contact())

        elif command in ("show-all", "show-all-notes"):
            print(show_all())

        elif command == "show-phone":  # no ML
            print(show_phone())

        elif command == "change-phone":
            print(change_contact())

        elif command == "remove-phone":
            print(remove_number())

        elif command == "add-birthday":
            print(add_bd())

        elif command == "show-birthday":
            print(show_birthday())

        elif command == "birthdays":
            print(birthdays_num_days())

        elif command == "delete-contact":
            print(del_contact())

        elif command == "num-contacts":  # no ML
            print(num_records())

        elif command == "add-email":
            print(add_email())

        elif command == "change-email":
            print(change_email())

        elif command == "show-email":
            print(show_email())

        elif command == "delete-email":
            print(delete_email())

        elif command == "add-address":  # no ML
            print(add_address())

        elif command == "change-address":  # no ML
            print(change_address())

        elif command == "show-address":  # no ML
            print(show_address())

        elif command == "delete-address":  # no ML
            print(delete_address())

        elif not command:
            ...

        else:
            print("Invalid command. Please try again.")


notes_commands = [
    "add",
    "create",
    "touch",
    "edit",
    "upd",
    "update",
    "change",
    "ch",
    "remove",
    "delete",
    "del",
    "rm",
    "show",
    "all",
    "list",
    "ls",
    "search",
    "seek",
    "find",
    "filter",
    "grep",
    "help" "back",
    "return",
    "-",
    "exit",
    "close",
]


def notes_menu():
    while True:
        commands_completer = WordCompleter(notes_commands)
        session = PromptSession(completer=commands_completer)
        user_input = session.prompt("\nHow can I help you?\nEnter a command: notes: ")
        command = parser(user_input)

        if command in ("exit", "close"):
            exit_assistant()

        if command in ("back", "return", "-"):
            return

        elif command == "help":
            print(messages.notes_help_center)

        elif command in ("add-note"):
            print(add_note())

        elif command in ("edit-note"):
            print(edit_note())

        elif command in ("delete-note"):
            print(remove_note())

        elif command in ("show-all", "show-all-notes"):
            print(show_notes())

        elif command in ("find-note"):
            print(search_note())

        elif not command:
            ...

        else:
            print("Invalid command. Please try again.")
