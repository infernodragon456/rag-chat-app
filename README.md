# Document-Aware RAG Chatbot 🤖

A versatile RAG (Retrieval Augmented Generation) chatbot that can intelligently interact with any document or knowledge base you provide. Feed it PDFs, text files, or other documents, and it will use that information to provide accurate, context-aware responses. Currently demonstrated with the GALE Encyclopedia of Medicine, but can be adapted for any domain:

- Legal documents
- Technical documentation
- Research papers
- Business reports
- Educational materials
- And more!

## Technical Stack 🛠

- **Mistral-7B LLM**: For natural language understanding and generation
- **FAISS Vector Store**: For efficient similarity search
- **LangChain**: For building the RAG pipeline
- **Flask/Streamlit**: For the web interface

## Local Deployment (Quick Start) 🚀

### 1. Clone and Setup

```bash
git clone https://github.com/infernodragon456/rag-chat-app.git
cd rag-chat-app

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -e .
```

### 2. Environment Setup

Create a `.env` file in the root directory:
```
HF_TOKEN=your_huggingface_token
```

Get your HuggingFace token from [HuggingFace](https://huggingface.co/settings/tokens)

### 3. Prepare Your Documents

1. Place your documents in the `data/` directory
2. Supported formats include PDF and text files
3. The system will automatically process and index your documents

### 4. Run Locally

```bash
streamlit run app/streamlit_app.py
```

Visit `http://localhost:8501` in your browser to interact with the chatbot.

## Production Deployment 🌐

### Prerequisites

- Docker Desktop installed and running
- AWS account with necessary permissions
- Jenkins setup capability

### 1. Jenkins Setup

1. Build Jenkins container:
```bash
cd custom_jenkins
docker build -t jenkins-dind .
docker run -d \
  --name jenkins-dind \
  --privileged \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  jenkins-dind
```

2. Get Jenkins password:
```bash
docker logs jenkins-dind
```

3. Access Jenkins at `http://localhost:8080`

### 2. AWS Setup

1. Create IAM User with permissions:
   - `AmazonEC2ContainerRegistryFullAccess`
   - `AWSAppRunnerFullAccess`

2. Create ECR Repository:
   - Go to AWS Console → ECR → Create Repository
   - Note the repository URI

### 3. Jenkins Pipeline Configuration

1. Add GitHub credentials to Jenkins:
   - Generate GitHub token with `repo` and `admin:repo_hook` scopes
   - Add token to Jenkins credentials

2. Add AWS credentials to Jenkins:
   - Add AWS access key and secret to Jenkins credentials

3. Create Pipeline:
   - Create new Pipeline job in Jenkins
   - Configure GitHub webhook
   - Use provided Jenkinsfile

### 4. Deploy to AWS App Runner

1. Go to AWS App Runner console
2. Create service using ECR image
3. Configure:
   - CPU/Memory
   - Environment variables
   - Auto-deployment settings

### 5. Run Pipeline

1. Push code to GitHub
2. Pipeline will automatically:
   - Build Docker image
   - Run security scans with Trivy
   - Push to ECR
   - Deploy to App Runner

Your app will be accessible via the App Runner URL provided by AWS.

## Customization 🎨

You can customize various aspects of the chatbot:

- Change the chunk size and overlap in `config.py` for different document types
- Modify the prompt template to better suit your use case
- Adjust the LLM parameters (temperature, max tokens) for different response styles
- Configure the vector store settings for different performance characteristics

## Contributing 🤝

Feel free to open issues and pull requests for improvements!

## License 📄

[MIT License](LICENSE)