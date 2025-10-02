import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

from app.config.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP

logger = get_logger(__name__)

def load_pdf_files():
    try:
        if not os.path.exists(DATA_PATH):
            raise CustomException("Data path does not exist")
        logger.info(f"loading files from {DATA_PATH}")

        loader = DirectoryLoader(DATA_PATH, glob="*.pdf", recursive=True, show_progress=True, loader_cls=PyPDFLoader)
        documents = loader.load()

        if not documents:
            logger.info("No documents found")
        else:
            logger.info(f"loaded {len(documents)} documents")
        
        return documents
    except Exception as e:
        raise CustomException(e) from e

def create_text_chunks(documents):
    try:
        if not documents:
            raise CustomException("No documents found")
        logger.info(f"creating text chunks for {len(documents)} documents")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        text_chunks = text_splitter.split_documents(documents)

        logger.info(f"created {len(text_chunks)} text chunks")
        return text_chunks
    except Exception as e:
        raise CustomException(e) from e