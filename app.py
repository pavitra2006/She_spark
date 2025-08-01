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

st.markdown("---")
st.header("Ask a Question")
question = st.text_input("Enter your question about the uploaded PDFs")
if st.button("Get Answer") and question:
    context = "\n".join(pdf_texts)
    prompt = f"Answer this question based on the following context from uploaded PDFs:\n{context}\nQuestion: {question}"
    answer = ask_gemini(prompt)
    st.info("**Answer:**")
    st.markdown(f"<div style='background-color:#e6f7ff;padding:10px;border-radius:8px'><b>{answer}</b></div>", unsafe_allow_html=True)

st.markdown("---")
st.header("Extract Topics from PDFs")
if st.button("Show Topics"):
    if pdf_texts:
        prompt = f"Extract and list the main topics from the following academic text:\n{chr(10).join(pdf_texts)}"
        topics = ask_gemini(prompt)
        st.success("**Extracted Topics:**")
        st.markdown(f"<div style='background-color:#f6ffed;padding:10px;border-radius:8px'>{topics}</div>", unsafe_allow_html=True)
    else:
        st.warning("No content available. Please upload PDFs first.")


st.markdown("---")
st.header("Summarize PDF Content")
if st.button("Summarize PDF"):
    if pdf_texts:
        context = "\n".join(pdf_texts)
        summary = ask_gemini(f"Summarize the following PDF content for a student:\n{context}")
        st.success("**Summary:**")
        st.markdown(f"<div style='background-color:#fffbe6;padding:10px;border-radius:8px'>{summary}</div>", unsafe_allow_html=True)
    else:
        st.warning("No PDF uploaded.")


st.markdown("---")
st.header("Generate Questions from PDF Content")
num_questions = st.number_input("How many questions to generate?", min_value=1, max_value=50, value=10)
if st.button("Generate Questions from PDF"):
    if pdf_texts:
        context = "\n".join(pdf_texts)
        prompt = (
            f"Generate {num_questions} exam-style questions from the following PDF content. "
            f"Format as a numbered list.\n{context}"
        )
        questions = ask_gemini(prompt)
        st.info(f"**Generated Questions ({num_questions}):**")
        st.markdown(f"<div style='background-color:#e6f7ff;padding:10px;border-radius:8px'>{questions}</div>", unsafe_allow_html=True)
    else:
        st.warning("No PDF uploaded.")

st.markdown("---")
st.header("Suggest References for PDF Content")
if st.button("Get References from PDF"):
    if pdf_texts:
        context = "\n".join(pdf_texts)
        prompt = f"Suggest authoritative websites or books for the following PDF content:\n{context}"
        references = ask_gemini(prompt)
        st.success("**References:**")
        st.markdown(f"<div style='background-color:#f6ffed;padding:10px;border-radius:8px'>{references}</div>", unsafe_allow_html=True)
    else:
        st.warning("No PDF uploaded.")
