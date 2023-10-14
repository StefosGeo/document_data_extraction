# PDF Data Extractor

This tool automatically parses PDF files and  leverages OpenAI and Langchain to extract structured data from them.
The Document scraper is skipped for now, since it is not the main focus of the project.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Future Work](#future-work)
- [License](#license)


## Features

- **Data Extraction**: Utilize the power of OpenAPI and Langchain to process and extract structured data from the scraped PDFs.

## Prerequisites

- [Python](https://www.python.org/downloads/)
- Additional libraries and dependencies (refer to the `requirements.txt`).
- Docker

## Installation

1. Clone this repository:
   ```bash
   git clone git@github.com:StefosGeo/document_data_extraction.git
   ```
   
2. Rename the `.env.example` file to `.env` and fill in the required fields.


3. Build the Docker image:
   ```bash
    docker build -t document_data_extraction .
    ```
   
4. Run the Docker container:
   ```bash
    docker run -it document_data_extraction
    ```
   

## Usage

* Add the PDF files you want to extract data from in the `data` folder.
* Run using the above instructions.
* The extracted data will be saved in the `output` folder in CSV format.


## Future Work
- [ ] Add a sanitization step to the extracted data.
- [ ] Handle more file formats.
- [ ] Store extracted data in a database.
- [ ] Add a web interface for the tool.
- [ ] Better exception handling.
- [ ] Add tests.

## License

#### MIT License