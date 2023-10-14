import os
import unittest
from document_parser.documents import PDFDocument


class DocumentTests(unittest.TestCase):

    def test_remove_extra_spaces(self):
        text = "This   is    a   test   text.  "
        expected_text = "This is a test text. "
        doc = PDFDocument("dummy_path")  # Note: This dummy path will not be used in this test
        cleaned_text = doc._remove_extra_spaces(text)
        self.assertEqual(cleaned_text, expected_text)

    def test_remove_extra_paragraphs(self):
        text = "Paragraph 1.\n\n\nParagraph 2.\n\n\n\nParagraph 3."
        expected_text = "Paragraph 1.\n\nParagraph 2.\n\nParagraph 3."
        doc = PDFDocument("dummy_path")  # Note: This dummy path will not be used in this test
        cleaned_text = doc._remove_extra_paragraphs(text)
        self.assertEqual(cleaned_text, expected_text)


class PDFDocumentTests(unittest.TestCase):

    def setUp(self):
        self.test_data_folder = "tests/test_data"
        self.sample_pdf = os.path.join(self.test_data_folder, "property1.pdf")

    def test_read(self):
        # Test if the PDFDocument can read a sample PDF without errors
        pdf_doc = PDFDocument(self.sample_pdf)
        pdf_doc.read()
        self.assertIsNotNone(pdf_doc.text)


if __name__ == "__main__":
    unittest.main()
