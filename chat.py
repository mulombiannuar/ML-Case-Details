import streamlit as st
from case_details import *
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from html_templates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from langchain_community.embeddings import OllamaEmbeddings

st.set_page_config(page_title="Chat with Court Case", page_icon=":bar_chart:", layout='wide')
st.title("Chat with Court Case")

# function to get chunk of texts
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=500,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


# function to create vector store
def get_vectorstore(text_chunks):
    embeddings = OllamaEmbeddings(model="gemma3")  # you can change to another model
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


# initialize session state to store search results
if "search_results" not in st.session_state:
    st.session_state.search_results = None
  
    
with st.sidebar:
    st.subheader("Search Case Details")

    # input for case ID
    case_id = st.number_input(label="Enter Case ID", value=1697996, help="Enter case ID e.g 1697996")
    
    # button to search case 
    if st.button("Search Case"):
        with st.spinner("Searching case...."):
            if case_id:
                # call the search function
                case_details_search = get_case_details_by_id(case_id)

                # check if search results are empty
                if not case_details_search:
                    st.warning("No case details found. Please try a different case ID.")
                else:
                    # store search results in session state
                    case_details = get_case_details(case_id)
                    st.session_state.search_results = case_details
            else:
                st.error("Please complete all required fields before searching.")
                

# display search results in the main area
if "search_results" in st.session_state and st.session_state.search_results is not None:
    case_details_search = st.session_state.search_results

    if case_details_search:
        st.subheader("Case Search Results")
        st.success(f"Found Case Number {case_details_search['case_summary'][0]['case_number']} matching your criteria.")

        # get cleaned case text
        cleaned_case_text = clean_case_details_for_embedding(case_details_search)
        
        # get the text chunks
        text_chunks = get_text_chunks(cleaned_case_text)
        
        st.write(text_chunks)

