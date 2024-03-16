from personal_assistant.commands import (
    add_contact,
    find_contact,
    show_all,
    show_phone,
    change_contact,
    remove_number,
    add_bd,
    show_birthday,
    birthdays_num_days,
    del_contact,
    num_records,
    add_email,
    change_email,
    show_email,
    delete_email,
    add_address,
    change_address,
    show_address,
    delete_address,
    add_note,
    edit_note,
    remove_note,
    show_notes,
    search_note,
    exit_assistant,
)
from personal_assistant.src import messages
from personal_assistant.src.messages import (
    contacts_interface_title,
    notes_interface_title,
)
from personal_assistant.src.utils import parser


def contacts_menu():
    while True:
        user_input = input("How can I help you?\nEnter a command: contacts: ")
        command, *args, message = parser(user_input)

        if command in ("exit", "close"):
            exit_assistant()

        if command in ("back", "return", "-"):
            return

        elif command == "help":
            print(messages.contacts_help_center)

        elif command == "add":
            print(add_contact(args))

        elif command == "find":
            print(find_contact(args))

        elif command == "all":
            print(show_all())

        elif command == "show-phone":
            print(show_phone(args))

        elif command == "change":
            print(change_contact(args))

        elif command in ["remove-phone", "delete-phone"]:
            print(remove_number(args))

        elif command == "add-birthday":
            print(add_bd(args))

        elif command == "show-birthday":
            print(show_birthday(args))

        elif command == "birthdays":
            print(birthdays_num_days(args))

        elif command in ["delete", "remove"]:
            print(del_contact(args))

        elif command == "entries":
            print(num_records())

        elif command == "add-email":
            print(add_email(args))

        elif command == "change-email":
            print(change_email(args))

        elif command == "show-email":
            print(show_email(args))

        elif command == "delete-email":
            print(delete_email(args))

        elif command == "add-address":
            print(add_address(args))

        elif command == "change-address":
            print(change_address(args))

        elif command == "show-address":
            print(show_address(args))

        elif command == "delete-address":
            print(delete_address(args))

        elif not command:
            ...

        else:
            print("Invalid command. Please try again.")


def notes_menu():
    while True:
        user_input = input("How can I help you?\nEnter a command: notes: ")
        command, *args, message = parser(user_input)

        if command in ("exit", "close"):
            exit_assistant()

        if command in ("back", "return", "-"):
            return

        elif command == "help":
            print(messages.notes_help_center)

        elif command in ("add", "create", "touch"):
            print(add_note())

        elif command in ("edit", "upd", "update", "change", "ch"):
            print(edit_note())

        elif command in ("remove", "delete", "del", "rm"):
            print(remove_note())

        elif command in ("show", "all", "list", "ls"):
            print(show_notes())

        elif command in ("search", "seek", "find", "filter", "grep"):
            print(search_note())

        elif not command:
            ...

        else:
            print("Invalid command. Please try again.")
