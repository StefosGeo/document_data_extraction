import csv
import os

from document_parser.documents import PDFDocument
from document_parser.extractor import DataExtractor


def parse_documents():
    """
    Parses all documents in the data folder.
    Store the results in a csv file.
    """

    document_folder = "data/"
    documents_paths = os.listdir(document_folder)

    # Define the name of the CSV file to save the results
    csv_filename = "output/results.csv"

    # Open CSV file for writing
    with open(csv_filename, 'w', newline='') as csvfile:
        # We'll write the header only once, based on the keys of the first document parsed
        first_run = True

        for document_path in documents_paths:
            document = PDFDocument(document_folder + document_path)
            parser = DataExtractor(document)
            results = parser.qa()

            # Write header if it's the first document parsed
            if first_run:
                csv_writer = csv.DictWriter(csvfile, fieldnames=results.keys())
                csv_writer.writeheader()
                first_run = False

            csv_writer.writerow(results)

    print(f"Results have been saved to {csv_filename}")


if __name__ == "__main__":
    parse_documents()