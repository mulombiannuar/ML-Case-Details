import pandas as pd
import streamlit as st
from case_details import get_case_details_by_id, get_case_parties, get_case_activities, get_activity_court_documents

# generate mapping
def generate_mapping(data_list, key_name, value_name):
    """
    Generate a mapping dictionary and a list of keys from a list of dictionaries.

    :param data_list: List of dictionaries containing the data
    :param key_name: Key to be used as the dictionary key
    :param value_name: Key to be used as the dictionary value
    :return: A tuple containing (mapping dictionary, list of keys)
    """
    mapping = {item[key_name]: item[value_name] for item in data_list}
    keys_list = list(mapping.keys())
    return mapping, keys_list


# display case summary
def display_case_summary(case_details):
    if case_details:
        case_df = pd.DataFrame(case_details).T  # Transpose to have keys as row headers
        st.dataframe(case_df, use_container_width=True)  # Display as a table with full width
    else:
        st.warning("No case details available.")
        

# display case parties
def display_case_parties(case_parties):
    if case_parties:
        case_df = pd.DataFrame(case_parties)
        st.dataframe(case_df, use_container_width=True)  
    else:
        st.warning("No case parties available.")
        

# display case activities
def display_case_activities(case_activities):
    if case_activities:
        case_df = pd.DataFrame(case_activities)
        st.dataframe(case_df, use_container_width=True)  
    else:
        st.warning("No case activities available.")


# display case activities
def display_court_documents(court_documents):
    if court_documents:
        case_df = pd.DataFrame(court_documents)
        st.dataframe(case_df, use_container_width=True)  
    else:
        st.warning("No court documents available.")       


# function to create case details tabs
def create_case_tabs(case_id: int):
    
    tab_summary, tab_parties, tab_activities, tab_decisions, tab_documents = st.tabs(
        ["Case Summary", "Case Parties", "Case Activities", "Court Decisions", "Case Documents"]
    )
    
    case_details = get_case_details_by_id(case_id)
    case_parties = get_case_parties(case_id)
    case_activities = get_case_activities(case_id)
    court_documents = get_activity_court_documents(case_id)

    with tab_summary:
        st.subheader("Case Summary")
        display_case_summary(case_details) 
    
    with tab_parties:
        st.subheader("Case Parties")
        display_case_parties(case_parties)

    with tab_activities:
        st.subheader("Case Activities")
        display_case_activities(case_activities)
    
    with tab_decisions:
        st.subheader("Court Decisions")
        display_court_documents(court_documents)
    
    with tab_documents:
        st.subheader("Case Documents")
        # Add logic to display case documents