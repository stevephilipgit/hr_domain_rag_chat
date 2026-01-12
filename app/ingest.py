# app/ingest.py

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split_pdf(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)
    return chunks


if __name__ == "__main__":
    chunks = load_and_split_pdf("data/pdfs/company_policy.pdf")
    print(f"Loaded {len(chunks)} chunks")
