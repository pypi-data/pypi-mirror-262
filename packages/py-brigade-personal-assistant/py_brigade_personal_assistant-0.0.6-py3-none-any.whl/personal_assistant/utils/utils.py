from personal_assistant.src.personal_assistant import personal_assistant


def parser(user_input):
    if user_input == "":
        return None, "Please start with a valid command."

    if user_input in (
        "contacts",
        "notes",
        "exit",
        "close",
        "help",
        "-",
        "back",
        "return",
        "show-phone",
        "num-contacts",
        "add-address",
        "change-address",
        "show-address",
        "delete-address",
    ):
        command = user_input
    else:
        command = personal_assistant.classifier.predict(user_input)
    # command, *args = user_input.split()
    # command = command.lower().strip()
    return command
