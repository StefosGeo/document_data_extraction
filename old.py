import json
import os
import re
from enum import Enum
import nltk
from langchain import OpenAI
from nltk import word_tokenize
from PyPDF2 import PdfReader
import logging
import langchain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.cache import InMemoryCache
import tiktoken
from langchain.callbacks import get_openai_callback


api_key = "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"
os.environ["OPENAI_API_KEY"] = api_key

langchain.llm_cache = InMemoryCache()
nltk.download('punkt')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Query(Enum):
    AREA = "Ποσα τ.μ (τετραγωνικα μετρα) ειναι το διαμερισμα/ακινητο?"
    LOCATION = "Σε ποια οδο (τοποθεσια) βρισκεται το διαμερισμα/ακινητο? Βρες οδο και αριθμό, απαντησε σε μορφη: οδος|αριθμος"
    FLOOR = "Σε ποιον όροφο ειναι το διαμερισμα/ακινητο? Δωσε την απαντηση σε αριθμο"
    CONSTRUCTION_YEAR = "Ποιο ειναι το ετος κατασκευής του διαμερισματος/ακινητου?"
    OWNERSHIP_PERCENTAGE = "Τι ποσοστό ιδοκτησίας του διαμερισματος/ακινητου διατίθεται?"


def read_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        raw_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                raw_text += text
    return raw_text


# Split text into chunks
def split_text(text):
    text_splitter = CharacterTextSplitter(separator=".", chunk_size=6000, chunk_overlap=400, length_function=len)
    return text_splitter.split_text(text)


# Perform similarity search using FAISS
def perform_similarity_search(texts, embeddings):
    docsearch = FAISS.from_texts(texts, embeddings)
    return docsearch


# Perform question answering using the chat model
def perform_question_answering(chain, docs, question):
    return chain.run(input_documents=docs, question=question)


def remove_extra_spaces_and_paragraphs(text):
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove extra blank lines and paragraphs
    text = re.sub(r'\n\s*\n', '\n\n', text)

    return text


def main():
    # Set up API key
    if api_key is None:
        logger.error("API key not found. Please set OPENAI_API_KEY environment variable.")
        return

    # Set up OpenAI models
    embeddings = OpenAIEmbeddings()
    chain = load_qa_chain(ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0), chain_type="stuff")
    # chain = load_qa_chain(OpenAI(model_name="gpt-4-32k", temperature=0), chain_type="stuff")

    # Read and process the PDF file
    pdf_file = "data/ektimisi4.pdf"
    raw_text = read_pdf(pdf_file)
    raw_text = remove_extra_spaces_and_paragraphs(raw_text)
    tokens = word_tokenize(raw_text)
    token_count = len(tokens)
    print("Number of tokens:", token_count)
    encoding = tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(raw_text)
    print("Number of tokens:", len(tokens))
    texts = split_text(raw_text)
    results = {}
    extra_query = " Give the answer in json format. example {out: 45}"
    # Perform similarity search and question answering for each query
    docsearch = FAISS.from_texts(texts, embeddings)
    total_tokens = 0
    total_cost = 0
    for query in Query:
        with get_openai_callback() as cb:
            # Perform similarity search
            docs = docsearch.similarity_search(query.value, k=2)
            logger.info(f"Query: {query.value}")
            question = query.value + extra_query
            logger.info(question)
            # Perform question answering
            response = chain.run(input_documents=docs, question=question)
            results.update({query.name: json.loads(response)["out"]})
            logger.info(f"[OpenAI] Total Tokens: {cb.total_tokens}")
            logger.info(f"[OpenAI] Prompt Tokens: {cb.prompt_tokens}")
            logger.info(f"[OpenAI] Completion Tokens: {cb.completion_tokens}")
            logger.info(f"[OpenAI] Total Cost (USD): ${cb.total_cost}")
            total_tokens += cb.total_tokens
            total_cost += cb.total_cost
    print(results)
    logger.info(f"Total Tokens: {total_tokens}.  Total Cost (USD): ${total_cost}")


if __name__ == "__main__":
    main()
