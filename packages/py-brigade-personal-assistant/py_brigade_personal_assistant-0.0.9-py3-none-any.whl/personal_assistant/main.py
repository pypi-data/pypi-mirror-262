import personal_assistant.src.messages as messages
from personal_assistant.commands import (
    exit_assistant,
)
from personal_assistant.menus import contacts_menu, notes_menu
from personal_assistant.utils.utils import parser


def main():
    print(messages.welcome_message)

    while True:
        user_input = input(">> ")
        command = parser(user_input)

        if command in ["exit", "close"]:
            exit_assistant()

        elif command == "help":
            print(messages.main_help_center)

        elif command == "contacts":
            contacts_menu()

        elif command == "notes":
            notes_menu()

        elif not command:
            pass

        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
