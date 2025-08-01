# app.py
import streamlit as st
from src.gemini_client import ask_gemini

st.set_page_config(page_title="StudyMate Academic Assistant", layout="wide")
st.title("📚 StudyMate: AI-Powered Academic Assistant")

uploaded_files = st.file_uploader("Upload one or more PDF files", type=["pdf"], accept_multiple_files=True)
pdf_texts = []
if uploaded_files:
    import fitz  # PyMuPDF
    for uploaded_file in uploaded_files:
        with open(f"/tmp/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        doc = fitz.open(f"/tmp/{uploaded_file.name}")
        text = "\n".join([page.get_text() for page in doc])
        pdf_texts.append(text)
    st.success(f"Uploaded and processed {len(uploaded_files)} PDF(s)")

st.header("Ask a Question")
question = st.text_input("Enter your question about the uploaded PDFs")
if st.button("Get Answer") and question:
    context = "\n".join(pdf_texts)
    prompt = f"Answer this question based on the following context from uploaded PDFs:\n{context}\nQuestion: {question}"
    answer = ask_gemini(prompt)
    st.markdown(f"**Answer:** {answer}")

st.header("Extract Topics from PDFs")
if st.button("Show Topics"):
    if pdf_texts:
        prompt = f"Extract and list the main topics from the following academic text:\n{chr(10).join(pdf_texts)}"
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
    if pdf_texts:
        prompt = f"Find and list common topics across these academic texts:\n{chr(10).join(pdf_texts)}"
        common_topics = ask_gemini(prompt)
        st.write(common_topics)
    else:
        st.write("No content available. Please upload PDFs first.")
