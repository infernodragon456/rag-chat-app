import os
from app.components.pdf_loader import load_pdf_files, create_text_chunks
from app.components.vector_store import load_vector_store, create_vector_store
from app.config.config import DB_FAISS_PATH

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def process_and_store_pdfs():
    try:
        logger.info(f"Making the vectorstore")
        documents = load_pdf_files()
        chunks = create_text_chunks(documents)
        create_vector_store(chunks)
        logger.info(f"Vectorstore created")
    except Exception as e:
        error_message = CustomException("Error processing and storing PDFs",e)
        logger.error(str(error_message))
        raise error_message
    
if __name__ == "__main__":
    process_and_store_pdfs()
