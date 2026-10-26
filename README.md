# 💸 FinSaathi AI
### Your AI-Powered Financial Literacy Companion

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://finsaathi-ai-h6rrnqqbameargbappahgvk.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![IBM watsonx.ai](https://img.shields.io/badge/AI-IBM%20watsonx.ai-052FAD?logo=ibm&logoColor=white)](https://www.ibm.com/products/watsonx-ai)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

**FinSaathi AI** is an AI-powered financial literacy assistant designed to make financial concepts easier to understand. It aims to help users explore topics such as budgeting, saving, interest, digital payments, and financial fraud awareness through a conversational interface.

The project combines **Retrieval-Augmented Generation (RAG)** with IBM watsonx.ai and IBM Granite to provide responses informed by retrieved financial knowledge.

🚀 **Try the live application:** [FinSaathi AI](https://finsaathi-ai-h6rrnqqbameargbappahgvk.streamlit.app/)

---

## 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Project Objectives](#-project-objectives)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Configuration](#-environment-configuration)
- [Deployment](#-deployment)
- [Future Enhancements](#-future-enhancements)
- [Disclaimer](#-disclaimer)
- [Author](#-author)

## 🎯 Problem Statement

Financial concepts, digital banking practices, and online payment safety can be difficult for beginners to understand. People may also struggle to find clear explanations of unfamiliar financial terms and common digital-payment scams.

FinSaathi AI explores how generative AI and retrieval-based question answering can make financial education more accessible through a simple conversational experience.

## 🎯 Project Objectives

- Make basic financial concepts easier to understand.
- Explore the use of RAG for knowledge-grounded question answering.
- Integrate IBM watsonx.ai and IBM Granite into an AI application.
- Build an accessible web interface using Streamlit.
- Promote awareness of budgeting, saving, digital payments, and fraud prevention.

## ✨ Key Features

- **AI-powered question answering:** Ask questions about financial literacy in natural language.
- **Retrieval-Augmented Generation:** Retrieve relevant knowledge to support generated responses.
- **IBM Granite integration:** Use an IBM Granite model through IBM watsonx.ai.
- **Financial education:** Explore topics such as budgeting, saving, interest, and digital-payment safety.
- **Interactive web interface:** Access the application through a browser.
- **Cloud deployment:** Run the application using Streamlit Community Cloud.

*Feature availability and response quality depend on the current implementation, knowledge base, and configured IBM watsonx.ai service.*

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web application |
| IBM watsonx.ai | Access to foundation models |
| IBM Granite | Generative AI model |
| Retrieval-Augmented Generation (RAG) | Retrieve relevant knowledge for answers |
| PyPDF | Extract text from PDF documents |
| Pandas | Data processing |
| Scikit-learn | Machine-learning utilities and text similarity workflows, where implemented |
| python-dotenv | Local environment-variable management |
| GitHub | Source-code hosting |
| Streamlit Community Cloud | Application deployment |

## 🔄 How It Works

1. **User query:** The user asks a financial-literacy question.
2. **Knowledge retrieval:** The application searches its available financial knowledge base for relevant information.
3. **Context preparation:** Retrieved information is prepared as context for the language model.
4. **AI response generation:** IBM watsonx.ai is used to generate a response.
5. **Answer display:** The response is presented through the Streamlit interface.

### Architecture Overview

```text
          User
           |
           v
    Streamlit Interface
           |
           v
      User Question
           |
           v
    Knowledge Retrieval
           |
           v
   Relevant Context
           |
           v
 IBM watsonx.ai / Granite
           |
           v
    Generated Answer
           |
           v
     User Interface
```

## 📁 Project Structure

```text
FinSaathi-AI/
│
├── app.py
├── build_knowledge.py
├── test_watsonx.py
├── test_rag.py
├── requirements.txt
│
├── src/
│   ├── retriever.py
│   └── watsonx_client.py
│
├── data/
│   ├── financial_knowledge.json
│   ├── raw/
│   └── processed/
│       └── chunks.json
│
├── .gitignore
└── README.md
```

*This structure reflects the project files used during development. Update it if your repository structure changes.*

## ⚙️ Getting Started

### Prerequisites

- Python installed on your computer
- Git
- An IBM Cloud account with access to the required watsonx.ai resources
- A watsonx.ai API key and project ID

### 1. Clone the repository

```bash
git clone https://github.com/ananya348/finsaathi-ai.git
cd finsaathi-ai
```

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root for local development:

```env
WATSONX_API_KEY=your_ibm_api_key
WATSONX_PROJECT_ID=your_watsonx_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

Use the correct regional endpoint for your IBM watsonx.ai deployment. Ensure the application reads these variable names.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL shown in your terminal, usually `http://localhost:8501`.

## ☁️ Deployment

FinSaathi AI is deployed using Streamlit Community Cloud.

**Live application:** [Launch FinSaathi AI](https://finsaathi-ai-h6rrnqqbameargbappahgvk.streamlit.app/)

For your own deployment:

1. Push the project code to a GitHub repository.
2. Connect the repository to Streamlit Community Cloud.
3. Select `app.py` as the application entry point.
4. Configure the required credentials in the app's **Secrets** settings.
5. Deploy the application.

Example Streamlit secrets configuration:

```toml
WATSONX_API_KEY = "your_ibm_api_key"
WATSONX_PROJECT_ID = "your_watsonx_project_id"
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
```

**Security note:** Never commit `.env`, API keys, access tokens, or other secrets to GitHub. Keep `.env` and `.venv/` excluded through `.gitignore`.

## 🚀 Future Enhancements

- Add guided budgeting and savings-planning tools.
- Expand the curated financial knowledge base.
- Improve retrieval relevance and answer evaluation.
- Add multilingual explanations for greater accessibility.
- Include more educational examples about UPI safety and digital-payment fraud.
- Add a feedback mechanism to evaluate helpfulness and identify incorrect answers.
- Introduce automated tests and monitoring for reliability.

## ⚠️ Disclaimer

FinSaathi AI is an educational project intended to support financial literacy. Its responses may be incomplete or inaccurate and should not be treated as personalized financial, investment, tax, or legal advice.

Always verify important financial information through official sources and consult a qualified professional when necessary.

## 👩‍💻 Author

**Ananya Das**

B.Tech in Computer Science Engineering — AI/ML specialization

GitHub: [@ananya348](https://github.com/ananya348)

---

⭐ If you find this project useful, consider starring the repository and sharing feedback.

*Built to explore the intersection of Generative AI, RAG, and accessible financial education.*
