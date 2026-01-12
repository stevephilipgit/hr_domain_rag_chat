# Enterprise HR Domain RAG Chatbot (FastAPI + React + Local LLM)

An end-to-end **Retrieval-Augmented Generation (RAG)** system built for answering **enterprise HR policy questions** using a domain-specific PDF.  
The system demonstrates **intent-aware querying, grounded responses, and conversational context handling**, with a clean separation between frontend, backend, and LLM layers.

---

## 🔍 Problem Statement

Enterprise policy documents (HR handbooks, company policies, SOPs) are:
- Long and hard to search
- Interpreted inconsistently
- Not conversational

This project solves that by enabling:
- Natural language Q&A over HR policy PDFs
- Grounded, non-hallucinated answers
- Context-aware follow-up questions (e.g., *“Explain them”*)

---

## 🧠 Solution Overview

This system uses **Retrieval-Augmented Generation (RAG)** combined with:
- Rule-based **intent classification**
- Strict **prompt guardrails**
- **Local LLM inference** for privacy and cost efficiency

The chatbot answers **only from the provided document**, ensuring enterprise-safe responses.

---

## 🧱 System Architecture (Layered Design)

### 1️⃣ Frontend Layer (React)
- Chat-based UI
- Markdown-rendered responses
- Source citations (PDF + page numbers)
- Typing animation for better UX

### 2️⃣ API Layer (FastAPI)
- `/chat` endpoint
- Session-based memory
- Intent routing
- Context compaction

### 3️⃣ RAG Layer
- PDF ingestion
- Chunking & embeddings
- Vector similarity search (FAISS)
- Context injection into prompts

### 4️⃣ LLM Layer
- **Gemma 1B** via **Ollama**
- Runs locally (CPU)
- Zero external API dependency

---

## 🧬 Architecture Flow
User (Browser)
↓
React Chat UI
↓
FastAPI /chat API
↓
Intent Detection
↓
Query Rewriting (if follow-up)
↓
FAISS Vector Search
↓
Relevant PDF Chunks
↓
Prompt + Context
↓
Local LLM (Gemma via Ollama)
↓
Grounded Answer + Sources
↓
React UI (Markdown + Sources)

---

## 📄 Document Used (Knowledge Source)

- **Company HR Policy PDF**
- Stored at:  data/pdfs/company_policy.pdf


This document includes:
- Code of Conduct
- Workplace policies
- Leave & benefits
- Security & compliance guidelines

> ⚠️ The chatbot **does not answer anything outside this document**.

---

🔁 Retrieval-Augmented Generation (RAG) – Explained

The RAG pipeline works as follows:

- PDF is split into semantic chunks
- Each chunk is converted into vector embeddings
- User query is embedded and compared using **FAISS**
- Top relevant chunks are retrieved
- Retrieved text is injected into a controlled prompt
- LLM generates an answer **only from retrieved context**

Why RAG?
- Prevents hallucinations
- Keeps answers document-grounded
- Enables updates by simply changing PDFs

--------------------------------------------------------------------------------------------

🎯 Intent-Aware Query Handling

The system uses **rule-based intent classification** to apply the correct prompt behavior.

### Supported intents include:
- Reporting / Contact queries
- Policy summaries
- Definitions
- Procedures
- Leave & time-off
- Compensation & benefits
- Eligibility
- Consequences
- General queries
- Greetings (non-RAG)

Each intent maps to a **strict prompt template** to ensure compliance.

---------------------------------------------------------------------------------

🧠 Context Awareness (Multi-turn Chat)

The chatbot supports **contextual follow-ups** such as:

> User: *What are the company policies?*  
> User: *Explain them*

This is handled using:
- Topic tracking
- Follow-up query rewriting
- Context compaction (no full chat history passed)

------------------------------------------------------------------------------------
 🛠️ Tools & Libraries Used

### Backend
- **Python**
- **FastAPI**
- **LangChain**
- **FAISS**
- **HuggingFace Sentence Transformers**
- **Ollama**
- **Gemma 1B**

### Frontend
- **React**
- **React Markdown**
- **CSS animations**

### Other
- **Git & GitHub**
- **Virtual Environments**
- **REST APIs**

--------------------------------------------------------------------------------------------

## 🔐 Local LLM Choice (Why Gemma + Ollama?)

- Runs completely **offline**
- No API costs
- Suitable for **enterprise privacy**
- Easy to swap with cloud LLMs in production

> In production, the LLM layer can be replaced with OpenAI, Azure OpenAI, or other managed APIs.

--------------------------------------------------------------------------------------------

## 🌐 Deployment Strategy

 Current Mode
- **Local LLM (Gemma)**
- Backend + UI runnable locally
- Cloud deployment runs in **demo mode**

 Demo Mode (Cloud-safe)
- UI & API are publicly accessible
- LLM responses are disabled with clear messaging
- Architecture remains visible and testable

------------------------------------------------------------------------------------------------

## 🎥 Demo & Media

### 📸 Screenshots
_Add screenshots of:_
- Chat UI
- Source citation
- Typing animation

### 🎬 Demo Video
_Record a short video showing:_
- Asking HR questions
- Follow-up queries
- Source-based answer
- 


---

## 🧪 Example Queries

- What is the Employee Code of Conduct?
- Whom should I contact in case of harassment?
- Explain the leave policy
- What are the workplace rules?
- Explain them (follow-up)

---

## 📌 Applications

- Internal HR chat assistants
- Policy compliance tools
- Enterprise knowledge bases
- Onboarding support systems
- Secure document Q&A systems

---

## 🚀 Future Enhancements

- Entity-aware follow-up expansion
- Cloud LLM integration
- Authentication & RBAC
- Multi-document support
- Analytics & feedback loop

---

## 👨‍💻 Author

**Steve Philip**  
AI / ML | GenAI | RAG Systems  
GitHub: https://github.com/stevephilipgit

---

## 📜 License

This project is for educational and portfolio purposes.



