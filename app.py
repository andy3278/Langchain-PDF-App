from dotenv import load_dotenv
import streamlit as st



def main ():
    # load env secret
    load_dotenv()
    
    st.set_page_config(page_title = "Ask PDF")
    st.header("Ask PDF")

    pdf = st.file_uploader("Upload your PDF here", type = ["pdf"])
    


if __name__ == '__main__':
    main()