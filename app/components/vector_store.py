from langchain_community.vectorstores import FAISS
import os
from app.components.embeddings import get_embedding_model
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

from app.config.config import DB_FAISS_PATH
logger = get_logger(__name__)

def load_vector_store():
    try:
        embedding_model = get_embedding_model()
        if os.path.exists(DB_FAISS_PATH):
            logger.info(f"Loading vector store")
            return FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
        else:
            logger.warning(f"No vector store found")
    except Exception as e:
        error_message = CustomException("Error loading vector store",e)
        logger.error(str(error_message))
        raise error_message

def create_vector_store(text_chunks):
    try:
        if not text_chunks:
            raise CustomException("No text chunks found")
        logger.info(f"Creating vector store")
        embedding_model = get_embedding_model()

        db = FAISS.from_documents(text_chunks, embedding_model)
        logger.info(f"Vector store created")

        db.save_local(DB_FAISS_PATH)
        logger.info(f"Vector store saved")
        return db
    except Exception as e:
        error_message = CustomException("Error creating vector store",e)
        logger.error(str(error_message))
        raise error_message
    
    