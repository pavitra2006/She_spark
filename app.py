# app.py
import streamlit as st
from src.gemini_client import ask_gemini

st.set_page_config(page_title="StudyMate Academic Assistant", layout="wide")
st.title("📚 StudyMate: AI-Powered Academic Assistant")

tab1, tab2 = st.tabs(["Main Features", "Google Form MCQ Preview"])

with tab1:
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

    st.header("Summarize PDF Content")
    if st.button("Summarize PDF"):
        if pdf_texts:
            context = "\n".join(pdf_texts)
            summary = ask_gemini(f"Summarize the following PDF content for a student:\n{context}")
            st.write(f"Summary: {summary}")
        else:
            st.write("No PDF uploaded.")

    st.header("Suggest References for PDF Content")
    if st.button("Get References from PDF"):
        if pdf_texts:
            context = "\n".join(pdf_texts)
            prompt = f"Suggest authoritative websites or books for the following PDF content:\n{context}"
            references = ask_gemini(prompt)
            st.write(references)
        else:
            st.write("No PDF uploaded.")

    st.header("Generate Diagrams for PDF Topics")
    concept = st.text_input("Enter a concept from the PDF for image/diagram generation")
    if st.button("Generate Image for Concept") and concept:
        image_prompt = f"Generate a diagram or image for the concept: {concept} from the following PDF content:\n{chr(10).join(pdf_texts)}"
        image_desc = ask_gemini(image_prompt)
        st.write(f"Image/Diagram description: {image_desc}")

    st.header("Generate MCQ Questions for Google Form from PDF")
    mcq_topic = st.text_input("Enter topic or concept from PDF for MCQ generation")
    num_mcq = st.slider("Number of MCQs to generate", min_value=1, max_value=50, value=10)
    if st.button("Generate MCQs") and mcq_topic:
        context = "\n".join(pdf_texts)
        mcq_prompt = (
            f"From the following PDF content, generate {num_mcq} multiple choice questions (MCQs) for the topic '{mcq_topic}'. "
            f"Format each question with 4 options and indicate the correct answer.\n{context}"
        )
        mcq_questions = ask_gemini(mcq_prompt)
        st.session_state['mcq_questions'] = mcq_questions
        st.write(mcq_questions)

with tab2:
    st.header("Google Form MCQ Preview")
    if 'mcq_questions' in st.session_state:
        st.write(st.session_state['mcq_questions'])
    else:
        st.write("No MCQs generated yet. Use the MCQ generator in the Main Features tab.")

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


st.header("Summarize PDF Content")
if st.button("Summarize PDF"):
    if pdf_texts:
        context = "\n".join(pdf_texts)
        summary = ask_gemini(f"Summarize the following PDF content for a student:\n{context}")
        st.write(f"Summary: {summary}")
    else:
        st.write("No PDF uploaded.")


st.header("Suggest References for PDF Content")
if st.button("Get References from PDF"):
    if pdf_texts:
        context = "\n".join(pdf_texts)
        prompt = f"Suggest authoritative websites or books for the following PDF content:\n{context}"
        references = ask_gemini(prompt)
        st.write(references)
    else:
        st.write("No PDF uploaded.")


st.header("Generate Diagrams for PDF Topics")
if st.button("Generate Diagrams from PDF"):
    if pdf_texts:
        context = "\n".join(pdf_texts)
        diagram_prompt = f"For the following PDF content, generate a flowchart or diagram description for each main topic:\n{context}"
        diagram_desc = ask_gemini(diagram_prompt)
        st.write(f"Diagram descriptions: {diagram_desc}")
    else:
        st.write("No PDF uploaded.")
st.header("Generate Viva Questions (Google Form) from PDF")
if st.button("Generate Viva Questions Google Form"):
    if pdf_texts:
        context = "\n".join(pdf_texts)
        viva_prompt = (
            f"From the following PDF content, generate up to 50 viva questions suitable for a Google Form. "
            f"Format the output as a list of questions, and provide a Google Form creation link template if possible.\n{context}"
        )
        viva_questions = ask_gemini(viva_prompt)
        st.write(viva_questions)
    else:
        st.write("No PDF uploaded.")

st.header("Find Common Topics Across PDFs")
if st.button("Show Common Topics") and uploaded_files:
    if pdf_texts:
        prompt = f"Find and list common topics across these academic texts:\n{chr(10).join(pdf_texts)}"
        common_topics = ask_gemini(prompt)
        st.write(common_topics)
    else:
        st.write("No content available. Please upload PDFs first.")
