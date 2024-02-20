import io
from .models import DiaryEntry


class EntryTxtGen:
    """
    Helper class that generated text files for the related diary views.
    """

    def __init__(self):
        self.entry = None
        self.diary = None
        self.fileBuffer = None

    def generate_entry(self, entry: DiaryEntry, file_buffer: io.BytesIO):
        self.entry = entry
        self.fileBuffer = file_buffer

        text = f"""{entry.created_by}'s Diary\n\n{entry.title}\n{entry.description}\n{entry.formatted_date()}"""

        bytes_text = bytes(text, "utf-8")

        file_buffer.write(bytes_text)

        return self.fileBuffer

    def generate_diary(self, diary: list, file_buffer: io.BytesIO):
        self.diary = diary
        self.fileBuffer = file_buffer

        first_entry: DiaryEntry = diary[0]

        text = f"""{first_entry.created_by}'s Diary\n\n"""

        for entry in diary:
            text += f"{entry.title}\n{entry.description}\n{entry.formatted_date()}\n\n"

        bytes_text = bytes(text, "utf-8")

        file_buffer.write(bytes_text)

        return self.fileBuffer
