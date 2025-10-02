from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface.chat_models import ChatHuggingFace
from app.config.config import HF_TOKEN, HUGGINGFACE_REPO_ID

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def load_llm(huggingface_repo_id: str = HUGGINGFACE_REPO_ID, huggingface_api_token: str = HF_TOKEN):
    try: 
        logger.info(f"Loading LLM")
        llm = HuggingFaceEndpoint(
            repo_id=huggingface_repo_id, 
            huggingfacehub_api_token=huggingface_api_token,
            temperature=0.3,
            max_new_tokens=512,
            )
        chat_model = ChatHuggingFace(llm=llm)
        logger.info(f"LLM loaded")
        return chat_model
    except Exception as e:
        error_message = CustomException("Error loading LLM",e)
        logger.error(str(error_message))
        raise error_message
    
if __name__ == "__main__":
    load_llm()