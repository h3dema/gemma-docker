import os

import gradio as gr

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings  # to be deprecated
from langchain_community.llms import Ollama

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_ollama import OllamaLLM as Ollama

DB_PATH = "/workspace/.db"
PDF_PATH = "/workspace/pdfs"

os.environ["TRANSFORMERS_VERBOSITY"] = "error"


def load_pdfs():
    docs = []
    for root, _, files in os.walk(PDF_PATH):
        for file in files:
            if file.endswith(".pdf"):
                loader = PyPDFLoader(os.path.join(root, file))
                docs.extend(loader.load())
    return docs

def build_db():
    docs = load_pdfs()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    # vectordb.persist()
    return vectordb

def load_db():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

def ask(query, history):
    if history is None:
        history = []

    docs = vectordb.similarity_search(query, k=4)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
    Context:
    {context}

    Question:
    {query}
    """

    answer = llm.invoke(prompt)
    history.extend(
        [
            {"role": "user", "content": [{"type": "text", "text": query}]},
            {"role": "assistant", "content": [{"type": "text", "text": answer}]}
        ]
    )
    import pdb; pdb.set_trace()
    # returns 2 values: one for the chatbot display, and one for the state to be passed back into the next call
    return history, history


if __name__ == "__main__":

    # Decide whether to rebuild DB
    if os.environ.get("LOAD_PDFS", "false").lower() == "true":
        vectordb = build_db()
    else:
        vectordb = load_db()

    llm = Ollama(model="gemma4:e4b")

    demo = gr.Interface(
        fn=ask,
        inputs=[
            gr.Textbox(label="Ask"),
            gr.State([])
        ],
        outputs=[
            gr.Chatbot(),
            gr.State()
        ],
        title="Local Gemma 4 PDF Assistant"
    )

    demo.launch(server_name="0.0.0.0", server_port=80)