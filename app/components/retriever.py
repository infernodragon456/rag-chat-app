from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate

from app.components.llm import load_llm
from app.components.vector_store import load_vector_store
from app.config.config import HUGGINGFACE_REPO_ID, HF_TOKEN, CUSTOM_PROMPT_TEMPLATE

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
logger = get_logger(__name__)

def set_custom_prompt(template: str = CUSTOM_PROMPT_TEMPLATE, input_variables: list = ["context", "question"]):
    try:
        prompt = PromptTemplate(template=template, input_variables=input_variables)
        return prompt
    except Exception as e:
        error_message = CustomException("Error setting custom prompt",e)
        logger.error(str(error_message))
        raise error_message

def create_qa_chain():
    try:
        logger.info(f"loading vector store")
        db = load_vector_store()
        if not db:
            raise CustomException("No vector store found")
        logger.info(f"loading llm")
        llm = load_llm()
        if not llm:
            raise CustomException("No llm found")
        logger.info(f"creating conversational qa chain")
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=db.as_retriever(search_kwargs={"k": 1}),
            return_source_documents=False,
            verbose=False
        )
        logger.info(f"conversational qa chain created")
        return qa_chain
    except Exception as e:
        error_message = CustomException("Error creating qa chain",e)
        logger.error(str(error_message))
        raise error_message
    
