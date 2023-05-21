from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

def main ():
    # load env secret
    load_dotenv()
    
    st.set_page_config(page_title = "Ask PDF")
    st.header("Ask PDF")
    # upload pdf
    pdf = st.file_uploader("Upload your PDF here", type = ["pdf"])

    # extract text from pdf
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # split text into chunks\
        splitter = CharacterTextSplitter(
            separator= "\n",
            chunk_size = 1000,
            chunk_overlap  = 0,
            length_function = len
        )
        chunks = splitter.split_text(text=text)

        # st.write(chunks)
        
        # create embeddings 
        embeddings = OpenAIEmbeddings()
        db = FAISS.from_texts(chunks, embedding=embeddings)

        question = st.text_input("input a question about the pdf: ")
        if question:
            # find top k relevant docs 
            docs = db.similarity_search(question, k = 4)
            #st.write(docs)
            llm = OpenAI(verbose=True)
            chain = load_qa_chain(llm=llm, chain_type="stuff", verbose=True)
            response = chain.run(input_documents = docs, question=question)

            st.write(response)


if __name__ == '__main__':
    main()