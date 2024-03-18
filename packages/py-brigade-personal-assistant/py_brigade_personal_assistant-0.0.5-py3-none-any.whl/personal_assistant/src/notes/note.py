class Note:
    def __init__(self, name, tags, text):
        self.name = name
        self.tags = tags
        self.text = text

    def __str__(self):
        return f"Name: {self.name}\nTags: {self.tags}\nText: {self.text}\n"
