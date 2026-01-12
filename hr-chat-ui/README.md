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

