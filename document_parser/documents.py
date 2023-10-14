import abc
import re

from PyPDF2 import PdfReader


class Document(abc.ABC):

    def __init__(self, document: str, language: str = "gr") -> None:
        """
        Defines a document to be read and cleaned.
        :param document: The file path to the document
        """
        self._document = document
        self.language = language
        self._raw_text = None

    @property
    def text(self):
        return self._raw_text

    @abc.abstractmethod
    def read(self):
        return self

    def clean(self):
        self._raw_text = self._remove_extra_spaces(self._raw_text)
        self._raw_text = self._remove_extra_paragraphs(self._raw_text)
        return self

    @staticmethod
    def _remove_extra_spaces(text: str) -> str:
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        return text

    @staticmethod
    def _remove_extra_paragraphs(text: str) -> str:
        # Remove extra blank lines and paragraphs
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text


class PDFDocument(Document):

    def read(self):
        with open(self._document, "rb") as file:
            reader = PdfReader(file)
            raw_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    raw_text += text
        self._raw_text = raw_text
        return self

