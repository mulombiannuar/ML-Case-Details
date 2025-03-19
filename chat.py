import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from case_details import *
import json

st.set_page_config(page_title="Chat with Court Case", page_icon=":bar_chart:", layout='wide')
st.title("Chat with Court Case")

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

        st.write(clean_case_details_for_embedding(case_details_search))

