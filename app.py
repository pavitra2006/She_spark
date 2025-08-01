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
# ...existing code...

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
    answer = qa.answer_question(question)
    st.markdown(f"**Answer:** {answer}")

st.header("Extract Topics from PDFs")
if st.button("Show Topics"):
    # Dummy implementation: In real code, extract topics using NLP
    st.write(["Topic 1", "Topic 2", "Topic 3"])  # Replace with actual topic extraction

st.header("Summarize Paragraphs")
paragraphs = st.text_area("Paste paragraphs to summarize")
if st.button("Summarize") and paragraphs:
    # Dummy implementation: In real code, use LLM for summarization
    st.write("Summary: ...")  # Replace with actual summary

st.header("Suggest References")
reference_query = st.text_input("Enter a topic for references")
if st.button("Get References") and reference_query:
    # Dummy implementation: In real code, use web search APIs
    st.write(["https://en.wikipedia.org/wiki/", "Book: Example Reference"])  # Replace with actual references

st.header("Generate Diagram (Flowchart)")
diagram_text = st.text_area("Enter paragraph for diagram generation")
if st.button("Generate Diagram") and diagram_text:
    # Dummy implementation: In real code, use diagram generation APIs
    st.image("https://via.placeholder.com/400x200?text=Flowchart")  # Replace with actual diagram

st.header("Find Common Topics Across PDFs")
if st.button("Show Common Topics") and uploaded_files:
    # Dummy implementation: In real code, compare topics across PDFs
    st.write(["Common Topic 1", "Common Topic 2"])  # Replace with actual common topics
