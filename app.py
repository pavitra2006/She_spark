StudyMate/
├── app.py                 (New File)
├── requirements.txt       (New File)
├── .env                  (New File)
├── config.py             (New File)
├── src/                  (New Folder)
│   ├── _init_.py       (New File)
│   ├── pdf_processor.py  (New File)
│   ├── text_chunker.py   (New File)
│   ├── embeddings.py     (New File)
│   ├── vector_store.py   (New File)
│   ├── llm_client.py     (New File)
│   └── qa_system.py      (New File)
└── README.md             (New File)# app.py

from src.qa_system import QASystem
import sys

def main():
    qa = QASystem()
    if len(sys.argv) < 3:
        print("Usage: python app.py <pdf_path> <question>")
        return
    pdf_path = sys.argv[1]
    question = sys.argv[2]
    qa.ingest_pdf(pdf_path)
    answer = qa.answer_question(question)
    print(f"Answer: {answer}")

# if __name__ == "__main__":
#     main()
