from collections import UserList
from itertools import groupby, chain, repeat, cycle

from personal_assistant.src.notes.note import Note


class Notes(UserList):
    def __init__(self):
        super().__init__()

    def add_note(self):
        name = input("Enter note name: ")
        tags = input("Enter note tags (comma-separated): ").split(",")
        text = input("Enter note text: ")

        note = Note(name.strip(), [tag.strip() for tag in tags], text.strip())
        self.data.append(note)
        return "Note added successfully."

    def get_all_notes(self):
        if not self.data:
            return "No notes found."

        return "\nAll Notes:\n" + self._format_notes(self.data)

    def remove_note(self, name):
        matching_notes = [note for note in self.data if note.name == name]
        [self.data.remove(note) for note in matching_notes]

        if matching_notes:
            return f"{len(matching_notes)} notes with name '{name}' were removed successfully."
        else:
            return f"Note '{name}' not found in the Notes."

    def edit_note(self, name, new_text):
        matching_notes = [note for note in self.data if note.name == name]

        if matching_notes:
            matching_notes[0].text = new_text
            return f"Note '{name}' edited successfully."
        else:
            return f"Note '{name}' not found in the Notes."

    def search_note(self, query: str):
        name = query.split("name=")[-1].split(";")[0] if "name=" in query else None
        tag = query.split("tag=")[-1].split(";")[0] if "tag=" in query else None
        text = query.split("text=")[-1].split(";")[0] if "text=" in query else None

        def name_matches(note: Note):
            return note.name == name if name else True

        def tag_matches(note: Note):
            return tag in note.tags if tag else True

        def text_matches(note: Note):
            return text in note.text if text else True

        def matches(note):
            return name_matches(note) and tag_matches(note) and text_matches(note)

        matching_notes = list(filter(matches, self.data))

        return (
            "\nMatching Notes:\n" + self._format_notes(matching_notes)
            if matching_notes
            else "No matching notes found."
        )

    @staticmethod
    def _format_notes(notes):
        pattern = "{:>3} | {:^10} | {:<70} |\n"
        separator = f"{'-' * 4}|{'-' * 12}|{'-' * 72}|"

        def compose_row(name: str, item: any):

            max_length = 70

            if len(item) > max_length:
                c = cycle(chain(repeat(0, max_length), repeat(1, max_length)))
                first, *others = [
                    "".join(g) for _, g in groupby(item, lambda x: next(c))
                ]
                first_line = pattern.format("", name, first)
                other_lines = "".join(pattern.format("", "", o) for o in others)
                return first_line + other_lines

            return pattern.format("", name, item)

        table = []

        for i, note in enumerate(notes, start=1):
            table.append(
                separator + "\n" + pattern.format(i, "Name", note.name) + separator
            )

            tags = ", ".join(note.tags) if note.tags else "-"
            text = note.text if note.text else "-"

            row = compose_row("Tags", tags)
            row += compose_row("Text", text).rstrip("\n")

            table.append(row)

        return "\n".join(table) + "\n" + separator
