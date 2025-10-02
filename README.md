# 🔍 AI RAG Chatbot

This is a sophisticated AI-powered chatbot that uses the Retrieval-Augmented Generation (RAG) architecture to answer questions based on a provided set of documents. It is built with Python, Flask, and the LangChain library, featuring a simple web interface for interaction.

## ✨ Features

- **Conversational Interface**: Remembers previous parts of the conversation to provide context-aware answers.
- **Retrieval-Augmented Generation (RAG)**: Provides answers based on information found in your own documents, reducing hallucinations and providing factual responses.
- **Web UI**: A clean and simple web interface for asking questions and viewing responses.
- **Powered by Open Source**: Utilizes Hugging Face for powerful language models and FAISS for efficient vector storage.
- **Containerized**: Comes with a `Dockerfile` for easy setup and deployment.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **AI/ML**: LangChain, Hugging Face Transformers, FAISS
- **Frontend**: HTML, CSS
- **Containerization**: Docker

## 📂 Project Structure

The project is organized into several directories, each with a specific purpose:

```
rag_chatbot/
├── app/
│   ├── __init__.py
│   ├── application.py          # Main Flask application, handles routing and UI
│   ├── common/                 # Shared utilities
│   │   ├── custom_exception.py # Custom exception handling
│   │   └── logger.py           # Standardized logging setup
│   ├── components/             # Core components of the RAG pipeline
│   │   ├── data_loader.py      # Loads documents from the data directory
│   │   ├── embeddings.py       # Generates embeddings for text
│   │   ├── llm.py              # Loads the language model from Hugging Face
│   │   ├── retriever.py        # Sets up the conversational retrieval chain
│   │   └── vector_store.py     # Creates and loads the FAISS vector store
│   ├── config/
│   │   └── config.py           # Project configuration (paths, model names, etc.)
│   └── templates/
│       └── index.html          # Frontend HTML and CSS
├── data/                       # Place your source documents here (e.g., PDFs)
├── logs/                       # Application logs are stored here
├── vectorstore/                # Stores the generated FAISS vector index
├── Dockerfile                  # For building the Docker container
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Getting Started

There are two ways to set up and run this project: using Docker (recommended) or setting it up locally.

### Prerequisites

- **Hugging Face API Token**: You will need a Hugging Face account and an API token with at least `read` permissions. You can get one from [Hugging Face Account Settings](https://huggingface.co/settings/tokens).

### 1. Docker Setup (Recommended)

1.  **Clone the Repository**

    ```sh
    git clone <your-repo-url>
    cd rag_chatbot
    ```

2.  **Create an Environment File**
    Create a file named `.env` in the project root and add your Hugging Face token:

    ```
    HF_TOKEN="your_hugging_face_api_token"
    ```

3.  **Add Your Data**
    Place the documents you want the chatbot to use (e.g., `.pdf` files) into the `data/` directory.

4.  **Build and Run the Ingestion Service**
    Before starting the chatbot, you need to process your documents and create a vector store.

    ```sh
    # Build an image specifically for ingestion
    docker build -t rag-ingestion -f Dockerfile.ingest .

    # Run the ingestion container. This will load docs, create embeddings, and save the store.
    docker run --rm -v ./vectorstore:/app/vectorstore -v ./data:/app/data rag-ingestion
    ```

5.  **Build and Run the Chatbot Application**

    ```sh
    # Build the main application image
    docker build -t rag-chatbot .

    # Run the application container
    docker run -p 5000:5000 --env-file .env -v ./vectorstore:/app/vectorstore rag-chatbot
    ```

6.  **Access the Chatbot**
    Open your browser and navigate to `http://localhost:5000`.

### 2. Local Setup

1.  **Clone the Repository**

    ```sh
    git clone <your-repo-url>
    cd rag_chatbot
    ```

2.  **Create a Virtual Environment**

    ```sh
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**

    ```sh
    pip install -r requirements.txt
    ```

4.  **Set Environment Variable**
    Create a file named `.env` in the project root and add your token:

    ```
    HF_TOKEN="your_hugging_face_api_token"
    ```

5.  **Add Your Data**
    Place your documents into the `data/` directory.

6.  **Generate the Vector Store**
    Run the following command from the project root to process your documents and create the FAISS index. This only needs to be done once, or whenever you update the documents in the `data` folder.

    ```sh
    python -c "from app.components.vector_store import create_vector_store; create_vector_store()"
    ```

7.  **Run the Application**

    ```sh
    flask run --host=0.0.0.0
    ```

8.  **Access the Chatbot**
    Open your browser and navigate to `http://localhost:5000`.

## ⚙️ How It Works: The RAG Pipeline

This application uses a Retrieval-Augmented Generation (RAG) pipeline to provide answers.

1.  **Data Ingestion (Offline Step)**:

    - Documents in the `/data` directory are loaded and split into smaller, manageable chunks.
    - A sentence-transformer model generates a vector embedding for each chunk, converting the text into a numerical representation.
    - These embeddings are stored in a FAISS vector index in the `/vectorstore` directory for fast similarity searches.

2.  **Inference (Online Step)**:
    - When you ask a question, the same sentence-transformer model converts your question into a vector embedding.
    - This question vector is used to search the FAISS index for the most similar document chunks (i.e., the most relevant information).
    - The retrieved document chunks and your original question are combined into a prompt.
    - This combined prompt is sent to a large language model (`mistralai/Mistral-7B-Instruct-v0.3`) from Hugging Face.
    - The language model generates a final, human-readable answer based on the context provided by the retrieved documents.
    - The chat history is maintained to allow for follow-up questions.
