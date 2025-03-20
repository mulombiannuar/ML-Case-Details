import streamlit as st
from case_details import *
from PyPDF2 import PdfReader
import pdfplumber # Best for Scanned PDFs
from pdf2image import convert_from_path
import pytesseract
import os
import unicodedata
import re

st.set_page_config(
    page_title="Case Parties Documents", 
    page_icon=":bar_chart:", 
    layout='wide'
)

# function to get case document texts
def get_case_document_texts(file_id :int, pdf_path: str):
     document_text = get_case_document_file_texts(file_id)
     
     if document_text is not None:
        return document_text
     else:
        return get_case_document_pdf_texts(file_id, pdf_path)
    
#function to clean extracted text
def clean_extracted_text(text: str) -> str:
    """Cleans extracted text by removing unwanted characters, fixing spacing, and normalizing text."""
    text = unicodedata.normalize("NFKC", text)  # Normalize Unicode characters
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces/newlines with a single space
    text = re.sub(r"[^a-zA-Z0-9.,;:!?()'\s]", "", text)  # Remove special characters (except punctuation)
    text = text.strip()  # Remove leading and trailing spaces
    return text
    

# function to extract text from scanned PDFs
def ocr_pdf_text(pdf_path):
    text = ""
    images = convert_from_path(pdf_path)
    for image in images:
        #text += pytesseract.image_to_string(image)
        raw_text = pytesseract.image_to_string(image)
        text += clean_extracted_text(raw_text) + " " 
    return text

# modify get_pdf_text to use OCR for scanned PDFs
def get_case_document_pdf_texts(file_id, pdf_path: str):
    """Extracts text from a PDF, cleans it, and saves it to the database."""
    
    if os.path.exists(pdf_path):
        try:
            # try extracting text directly first
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                if text.strip():  # If text is found, return it
                    return text
            # if no text is found, fall back to OCR
            pdf_text = ocr_pdf_text(pdf_path)
            
            # save content to table
            save_case_document_texts(file_id, pdf_text)
            
            # return pdf texts
            return pdf_text
        except Exception as e:
            st.error(f"Error processing PDF of File ID : {file_id} with Error : {e}")
            return ""
    return ""


# display case parties
def display_case_parties_documents(case_parties, case_id:int):
    pdf_path = '/var/www/html/cts/uploads'
    if case_parties:
        for party in case_parties:
            
            cleaned_text = ""
            cleaned_text += f"Case Documents for {party['party_name']} :\n\n\n"
            
            case_party_documents = get_case_party_documents_filed(case_id, party['uacc_id'])
            if case_party_documents:
                with st.spinner("Extracting texts from documents. Please wait...."):
                    for doc in case_party_documents:
                        cleaned_text += f"Case Document Type Name: {doc['file_type_name']}\n\n"
                        
                        document_path = f"{pdf_path}/{doc['document_file_name']}"
                        pdf_extracted_text = get_case_document_texts(doc['file_id'],  document_path)
                        cleaned_text += f"Document Content: {pdf_extracted_text}\n\n\n" 
                        
                        cleaned_text += "\n"
                st.write(cleaned_text) 
    else:
        st.warning("No case parties available.")


def main():
    
    # initialize session state to store search results
    if "search_results" not in st.session_state:
        st.session_state.search_results = None
        
    st.header("Case Parties Documents")
    
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
                        case_parties = get_case_parties(case_id)
                        st.session_state.search_results = {'case_parties' : case_parties, 'case_details' : case_details_search}
                else:
                    st.error("Please complete all required fields before searching.")
                    
    
    # display search results in the main area
    if "search_results" in st.session_state and st.session_state.search_results is not None:
        case_details_search = st.session_state.search_results

        if case_details_search:
            st.subheader("Case Search Results")
            st.success(f"Found Case Number {case_details_search['case_details'][0]['case_number']} matching your criteria.")
            
            st.write("### Case Parties Documents Texts")
            display_case_parties_documents(
                case_parties=case_details_search['case_parties'], 
                case_id=case_details_search['case_details'][0]['case_id']
            )
            
if __name__ == '__main__':
    main()        