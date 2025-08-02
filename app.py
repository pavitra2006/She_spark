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
    st.markdown(f"""
        <div style='background-color:var(--secondary-background-color);color:var(--text-color);padding:10px;border-radius:8px'>
            <b>{answer}</b>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.header("Extract Topics from PDFs")
if st.button("Show Topics"):
    if pdf_texts:
        if len(pdf_texts) == 1:
            prompt = f"Extract and list the main topics from the following academic text:\n{pdf_texts[0]}"
        else:
            prompt = (
                f"Extract and list the main topics from each of the following academic PDFs separately. "
                f"Label the topics for each PDF as PDF1, PDF2, etc.\n"
                + "\n---\n".join([f"PDF{i+1}:\n{text}" for i, text in enumerate(pdf_texts)])
            )
        topics = ask_gemini(prompt)
        st.success("**Extracted Topics:**")
        st.markdown(f"""
            <div style='background-color:var(--secondary-background-color);color:var(--text-color);padding:10px;border-radius:8px'>
                {topics}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No content available. Please upload PDFs first.")


st.markdown("---")
st.header("Summarize PDF Content")
if st.button("Summarize PDF"):
    if pdf_texts:
        if len(pdf_texts) == 1:
            summary = ask_gemini(f"Summarize the following PDF content for a student:\n{pdf_texts[0]}")
        else:
            prompt = (
                f"Summarize the content of each of the following PDFs separately. "
                f"Label the summary for each PDF as PDF1, PDF2, etc.\n"
                + "\n---\n".join([f"PDF{i+1}:\n{text}" for i, text in enumerate(pdf_texts)])
            )
            summary = ask_gemini(prompt)
        st.success("**Summary:**")
        st.markdown(f"""
            <div style='background-color:var(--secondary-background-color);color:var(--text-color);padding:10px;border-radius:8px'>
                {summary}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No PDF uploaded.")


st.markdown("---")
st.header("Generate Questions from PDF Content")
num_questions = st.number_input("How many questions to generate?", min_value=1, max_value=50, value=10)
question_type = st.selectbox("Select question type", ["Short Answer", "Essay", "Multiple Choice"])
if st.button("Generate Questions from PDF"):
    if pdf_texts:
        context = "\n".join(pdf_texts)
        if question_type == "Short Answer":
            prompt = (
                f"Generate {num_questions} short answer questions from the following PDF content. "
                f"Format as a numbered list.\n{context}"
            )
        elif question_type == "Essay":
            prompt = (
                f"Generate {num_questions} essay questions from the following PDF content. "
                f"Format as a numbered list.\n{context}"
            )
        else:  # Multiple Choice
            prompt = (
                f"Generate {num_questions} multiple choice questions (MCQs) from the following PDF content. "
<<<<<<< HEAD
                f"For each question, list the 4 options one by one in a new line, and indicate the correct answer at the end. Format example:\n"
                f"1. Question text\nA. Option 1\nB. Option 2\nC. Option 3\nD. Option 4\nCorrect Answer: <option letter>\n"
=======
                f"For each question, list the question followed by options A, B, C, D (each on a new line, in order), then indicate the correct answer on a new line as 'Answer: <option letter>'. Format as:\n"
                f"1. Question text\nA. Option 1\nB. Option 2\nC. Option 3\nD. Option 4\nAnswer: <option letter>\n...\n"
>>>>>>> a2d4bcb (updated the feature)
                f"Use this format for all questions.\n{context}"
            )
        questions = ask_gemini(prompt)
        st.info(f"**Generated {question_type} Questions ({num_questions}):**")
        st.markdown(f"""
            <div style='background-color:var(--secondary-background-color);color:var(--text-color);padding:10px;border-radius:8px'>
                <pre style='background: none; color: inherit; font-family: inherit; font-size: inherit; margin: 0; padding: 0;'>{questions}</pre>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No PDF uploaded.")

st.markdown("---")
st.header("Extract Common Information from Multiple PDFs")
if st.button("Extract Common Info from PDFs"):
    if len(pdf_texts) >= 2:
        context = "\n".join(pdf_texts)
        prompt = (
            f"Compare the following PDF contents and extract the main topics, facts, or information that are common to all. "
            f"For each common item, mention which content belongs to which PDF (e.g., PDF1, PDF2, ...). Highlight the commonalities clearly.\n{context}"
        )
        common_info = ask_gemini(prompt)
        st.info("**Common Information Across PDFs:**")
        st.markdown(f"""
            <div style='background-color:var(--secondary-background-color);color:var(--text-color);padding:10px;border-radius:8px'>
                {common_info}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Please upload at least two PDFs to extract common information.")

st.markdown("---")
st.header("Suggest References for PDF Content")
if st.button("Get References from PDF"):
    if pdf_texts:
        context = "\n".join(pdf_texts)
        prompt = f"Suggest authoritative websites or books for the following PDF content:\n{context}"
        references = ask_gemini(prompt)
        if "429" in str(references):
            st.warning("Gemini API quota exceeded. Please wait a minute and try again, or reduce the size of your PDF. See https://ai.google.dev/gemini-api/docs/rate-limits for details.")
        else:
            st.success("**References:**")
            st.markdown(f"""
                <div style='background-color:var(--secondary-background-color);color:var(--text-color);padding:10px;border-radius:8px'>
                    {references}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No PDF uploaded.")
