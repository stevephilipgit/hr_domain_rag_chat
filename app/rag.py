# app/rag.py

import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from app.ingest import load_and_split_pdf

# --------------------------------------------------
# PATHS
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH = os.path.join(BASE_DIR, "data", "pdfs", "company_policy.pdf")
VECTOR_DB_PATH = os.path.join(BASE_DIR, "embeddings", "faiss_index")

# --------------------------------------------------
# INTENT CLASSIFIER
# --------------------------------------------------
def detect_intent(question: str) -> str:
    q = question.lower().strip()

    if q in ["hi", "hello", "hey", "good morning", "good evening"]:
        return "GREETING"

    if any(w in q for w in ["who", "whom", "contact", "report", "inform", "reach out"]):
        return "REPORTING"

    if any(w in q for w in ["code of conduct", "policy", "handbook", "guidelines", "rules"]):
        return "POLICY_SUMMARY"

    if any(w in q for w in ["what is", "define", "meaning"]):
        return "DEFINITION"

    if any(w in q for w in ["how", "process", "steps", "procedure", "apply"]):
        return "PROCEDURES"

    if any(w in q for w in ["leave", "pto", "sick", "holiday", "vacation", "time off", "working hours"]):
        return "LEAVE_AND_TIME_OFF"

    if any(w in q for w in ["salary", "pay", "compensation", "bonus", "raise", "overtime"]):
        return "COMPENSATION_AND_BENEFITS"

    if any(w in q for w in ["training", "development", "onboarding", "promotion", "performance"]):
        return "TRAINING_AND_DEVELOPMENT"

    if any(w in q for w in ["remote", "work from home", "dress code", "office policy", "work environment"]):
        return "WORK_ENVIRONMENT_AND_POLICIES"

    if any(w in q for w in ["eligible", "eligibility", "entitled", "qualify"]):
        return "ELIGIBILITY"

    if any(w in q for w in ["punishment", "disciplinary", "consequence", "penalty", "termination"]):
        return "CONSEQUENCES"

    return "GENERAL"

# --------------------------------------------------
# BASE RULES (ANTI-HALLUCINATION)
# --------------------------------------------------
BASE_RULES = """
Rules:
- Use ONLY the provided context.
- Do NOT add examples, placeholders, links, or assumptions.
- Do NOT invent roles, policies, or procedures.
"""

# --------------------------------------------------
# PROMPTS
# --------------------------------------------------
REPORTING_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=BASE_RULES + """
The question asks who to contact or report to.

Mention a PERSON, ROLE, or DEPARTMENT ONLY if explicitly stated.
If not stated, say:
"Reporting authority is not specified in the document. You may consult HR or management for guidance."

Context:
{context}

Question:
{question}

Answer:
"""
)

POLICY_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=BASE_RULES + """
Provide a concise policy summary.
Use bullet points ONLY for items explicitly mentioned.

Context:
{context}

Question:
{question}

Answer:
"""
)

DEFINITION_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=BASE_RULES + """
Provide a short definition strictly from the context.

Context:
{context}

Question:
{question}

Answer:
"""
)

PROCEDURES_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=BASE_RULES + """
Explain the procedure step by step if available.
If not clearly defined, say:
"The procedure is not explicitly described in the document."

Context:
{context}

Question:
{question}

Answer:
"""
)

LEAVE_AND_TIME_OFF_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=BASE_RULES + """
Explain leave or working hours.
Mention duration, type, and conditions ONLY if stated.
If missing, say:
"This information is not specified in the document."

Context:
{context}

Question:
{question}

Answer:
"""
)

COMPENSATION_AND_BENEFITS_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=BASE_RULES + """
Explain compensation or benefits factually.
Avoid assumptions or legal interpretation.

Context:
{context}

Question:
{question}

Answer:
"""
)

TRAINING_AND_DEVELOPMENT_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=BASE_RULES + """
Summarize training or development opportunities if stated.

Context:
{context}

Question:
{question}

Answer:
"""
)

WORK_ENVIRONMENT_AND_POLICIES_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=BASE_RULES + """
Explain workplace expectations or policies.

Context:
{context}

Question:
{question}

Answer:
"""
)

ELIGIBILITY_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=BASE_RULES + """
State eligibility conditions using if/then style if provided.
If not specified, say:
"Eligibility criteria are not specified in the document."

Context:
{context}

Question:
{question}

Answer:
"""
)

CONSEQUENCE_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=BASE_RULES + """
Explain consequences or disciplinary action strictly from the context.

Context:
{context}

Question:
{question}

Answer:
"""
)

GENERAL_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=BASE_RULES + """
Answer clearly using the context.
If not found, say:
"Not found in documents."

Context:
{context}

Question:
{question}

Answer:
"""
)

INTENT_PROMPT_MAP = {
    "REPORTING": REPORTING_PROMPT,
    "POLICY_SUMMARY": POLICY_PROMPT,
    "DEFINITION": DEFINITION_PROMPT,
    "PROCEDURES": PROCEDURES_PROMPT,
    "LEAVE_AND_TIME_OFF": LEAVE_AND_TIME_OFF_PROMPT,
    "COMPENSATION_AND_BENEFITS": COMPENSATION_AND_BENEFITS_PROMPT,
    "TRAINING_AND_DEVELOPMENT": TRAINING_AND_DEVELOPMENT_PROMPT,
    "WORK_ENVIRONMENT_AND_POLICIES": WORK_ENVIRONMENT_AND_POLICIES_PROMPT,
    "ELIGIBILITY": ELIGIBILITY_PROMPT,
    "CONSEQUENCES": CONSEQUENCE_PROMPT,
    "GENERAL": GENERAL_PROMPT
}

# --------------------------------------------------
# VECTOR STORE
# --------------------------------------------------
def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if os.path.exists(VECTOR_DB_PATH):
        return FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    docs = load_and_split_pdf(PDF_PATH)
    vs = FAISS.from_documents(docs, embeddings)
    vs.save_local(VECTOR_DB_PATH)
    return vs

# --------------------------------------------------
# RAG PIPELINE (WITH MEMORY)
# --------------------------------------------------
def ask_question(question: str, memory: dict | None = None):
    intent = detect_intent(question)

    # GREETING SHORT-CIRCUIT
    if intent == "GREETING":
        return {
            "intent": intent,
            "answer": "Hello! I can help you with company policies, procedures, and HR-related questions.",
            "sources": []
        }

    # FOLLOW-UP HANDLING
    if memory and memory.get("topic") and len(question.split()) < 6:
        question = f"For {memory['topic']}, {question}"

    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "fetch_k": 20, "lambda_mult": 0.5}
    )

    docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs)

    llm = Ollama(model="gemma3:1b", temperature=0)
    prompt = INTENT_PROMPT_MAP[intent].format(
        context=context,
        question=question
    )

    answer = llm.invoke(prompt)

    # TOPIC TRACKING
    if memory is not None and intent in ["POLICY_SUMMARY", "REPORTING", "PROCEDURES"]:
        memory["topic"] = question

    # Deduplicate sources
    seen, sources = set(), []
    for d in docs:
        key = (d.metadata.get("source"), d.metadata.get("page"))
        if key not in seen:
            seen.add(key)
            sources.append({
                "source": d.metadata.get("source"),
                "page": d.metadata.get("page")
            })

    return {
        "intent": intent,
        "answer": answer.strip(),
        "sources": sources
    }
