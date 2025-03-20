import streamlit as st
from case_details import *
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from html_templates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama

load_dotenv()
 
st.set_page_config(
    page_title="Chat with Court Case", 
    page_icon=":bar_chart:", 
    layout='wide'

)

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
    # embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    embeddings = OllamaEmbeddings(model="nomic-embed-text") 
    
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    
    return vectorstore


# function to get conversation chain
def get_conversation_chain(vectorstore):
    # llm = ChatOpenAI()
    llm = ChatOllama(model="gemma3:1b", temperature=0.5)
    #llm = HuggingFaceHub(repo_id="google/flan-t5-large", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True
    )

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    
    return conversation_chain


# function to handle user input
def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    # initialize session state to store search results
    if "search_results" not in st.session_state:
        st.session_state.search_results = None
        
    if "conversation" not in st.session_state:
            st.session_state.conversation = None

    if "chat_history" not in st.session_state:
            st.session_state.chat_history = None

    st.write(css, unsafe_allow_html=True)
    st.header("Chat with this case :books:")

        
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
            cleaned_case_text = clean_case_texts_for_embedding(case_details_search)
            
            # get the text chunks
            text_chunks = get_text_chunks(cleaned_case_text)
            
            # create vector store
            vectorstore = get_vectorstore(text_chunks)

            # create conversation chain
            st.session_state.conversation = get_conversation_chain(vectorstore)
            
            # get user question
            user_question = st.text_input(label="Ask a question about this case:", placeholder="e.g What is the case about?")
            if user_question:
                    handle_userinput(user_question)
            


if __name__ == '__main__':
    main()        