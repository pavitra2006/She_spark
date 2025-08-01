# StudyMate/
# ├── app.py                 (New File)
# ├── requirements.txt       (New File)
# ├── .env                  (New File)
# ├── config.py             (New File)
# ├── src/                  (New Folder)
# │   ├── _init_.py       (New File)
# │   ├── pdf_processor.py  (New File)
# │   ├── text_chunker.py   (New File)
# │   ├── embeddings.py     (New File)
# │   ├── vector_store.py   (New File)
# │   ├── llm_client.py     (New File)

# │   └── qa_system.py      (New File)
# └── README.md             (New File)# app.py

import streamlit as st
from src.qa_system import QASystem
from src.gemini_client import ask_gemini

st.set_page_config(page_title="StudyMate Academic Assistant", layout="wide")
st.title("📚 StudyMate: AI-Powered Academic Assistant")

qa = QASystem()

uploaded_files = st.file_uploader("Upload one or more PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with open(f"/tmp/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        qa.ingest_pdf(f"/tmp/{uploaded_file.name}")
    st.success(f"Uploaded and processed {len(uploaded_files)} PDF(s)")

st.header("Ask a Question")
question = st.text_input("Enter your question about the uploaded PDFs")
if st.button("Get Answer") and question:
    context = qa.vector_store.texts if hasattr(qa, 'vector_store') else []
    prompt = f"Answer this question based on the following context from uploaded PDFs:\n{context}\nQuestion: {question}"
    answer = ask_gemini(prompt)
    st.markdown(f"**Answer:** {answer}")

st.header("Extract Topics from PDFs")
if st.button("Show Topics"):
    if hasattr(qa, 'vector_store') and qa.vector_store.texts:
        prompt = f"Extract and list the main topics from the following academic text:\n{qa.vector_store.texts}"
        topics = ask_gemini(prompt)
        st.write(topics)
    else:
        st.write("No content available. Please upload PDFs first.")

st.header("Summarize Paragraphs")
paragraphs = st.text_area("Paste paragraphs to summarize")
if st.button("Summarize") and paragraphs:
    summary = ask_gemini(f"Summarize the following text for a student:\n{paragraphs}")
    st.write(f"Summary: {summary}")

st.header("Suggest References")
reference_query = st.text_input("Enter a topic for references")
if st.button("Get References") and reference_query:
    prompt = f"Suggest authoritative websites or books for the topic: {reference_query}"
    references = ask_gemini(prompt)
    st.write(references)

st.header("Generate Diagram (Flowchart)")
diagram_text = st.text_area("Enter paragraph for diagram generation")
if st.button("Generate Diagram") and diagram_text:
    diagram_prompt = f"Describe a flowchart for the following process or concept:\n{diagram_text}"
    diagram_desc = ask_gemini(diagram_prompt)
    st.write(f"Flowchart description: {diagram_desc}")

st.header("Find Common Topics Across PDFs")
if st.button("Show Common Topics") and uploaded_files:
    if hasattr(qa, 'vector_store') and qa.vector_store.texts:
        prompt = f"Find and list common topics across these academic texts:\n{qa.vector_store.texts}"
        common_topics = ask_gemini(prompt)
        st.write(common_topics)
    else:
        st.write("No content available. Please upload PDFs first.")
