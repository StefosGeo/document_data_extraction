import os
import csv
import logging

from document_parser.documents import PDFDocument
from document_parser.extractor import DataExtractor

# Configuration
DOCUMENT_FOLDER = "data/"
CSV_FILENAME = "output/results.csv"

logging.basicConfig(level=logging.INFO)


def parse_documents():
    """
    Parses all documents in the data folder.
    Store the results in a csv file.
    """

    if not os.path.exists(DOCUMENT_FOLDER):
        logging.error(f"Folder {DOCUMENT_FOLDER} does not exist.")
        return

    documents_paths = [file for file in os.listdir(DOCUMENT_FOLDER) if file.endswith('.pdf')]

    with open(CSV_FILENAME, 'w', newline='') as csvfile:
        first_run = True

        for document_path in documents_paths:
            try:
                document = PDFDocument(os.path.join(DOCUMENT_FOLDER, document_path))
                extractor = DataExtractor(document)
                results = extractor.qa()

                if first_run:
                    csv_writer = csv.DictWriter(csvfile, fieldnames=results.keys())
                    csv_writer.writeheader()
                    first_run = False

                csv_writer.writerow(results)
            except Exception as e:
                logging.error(f"Error processing {document_path}: {e}")

    logging.info(f"Total cost ($): {extractor.total_cost}")
    logging.info(f"Results have been saved to {CSV_FILENAME}")


if __name__ == "__main__":
    parse_documents()
