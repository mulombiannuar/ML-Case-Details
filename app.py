import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from case_details import *
from untils import generate_mapping, display_case_summary, create_case_tabs

st.set_page_config(page_title="Interactive Case Overview", page_icon=":bar_chart:", layout='wide')
st.title("Interactive Case Overview")

#st.write(get_activity_court_documents(1697996))

# generate years from 2000 to the current year
years = list(range(2000, datetime.now().year + 1))

# fetch heads and create a mapping
heads_data = get_heads()
head_mapping = {head["head_name"]: head["head_id"] for head in heads_data}
head_options = list(head_mapping.keys())

# initialize session state to store search results
if "search_results" not in st.session_state:
    st.session_state.search_results = None

with st.sidebar:
    st.subheader("Search Case Details")

    # selectbox for Court Heads
    head_name = st.selectbox(
        label="Court Heads",
        options=head_options,
        index=None,
        placeholder="Select court head...",
    )

    if head_name:
        head_id = head_mapping.get(head_name)  # get head_id

        # fetch stations based on selected head_id
        stations_data = get_head_stations(head_id)
        station_mapping = {station["unit_name"]: station["unit_id"] for station in stations_data}
        station_options = list(station_mapping.keys())

        # selectbox for Head Stations
        unit_name = st.selectbox(
            label="Head Stations",
            options=station_options,
            index=None,
            placeholder="Select head station...",
        )

        if unit_name:
            unit_id = station_mapping.get(unit_name)

            # fetch divisions based on selected unit_id
            divisions_data = get_unit_divisions(unit_id)
            division_mapping = {division["division_name"]: division["unit_division_id"] for division in divisions_data}
            division_options = list(division_mapping.keys())

            # selectbox for Unit Divisions
            division_name = st.selectbox(
                label="Unit Divisions",
                options=division_options,
                index=None,
                placeholder="Select unit division...",
            )

            if division_name:
                unit_division_id = division_mapping.get(division_name)

                # fetch unit division case categories
                case_categories_data = get_unit_division_case_categories(unit_division_id)
                case_categories_mapping, case_categories_options = generate_mapping(
                    data_list=case_categories_data,  
                    key_name="category_name", 
                    value_name="category_id"
                )

                # selectbox for Case Categories
                category_name = st.selectbox(
                    label="Case Categories",
                    options=case_categories_options,
                    index=None,
                    placeholder="Select case category...",
                )

                # input for Case Number
                case_number = st.text_input(
                    label="Case Number", 
                    placeholder="Enter case number e.g E103",
                )

                # selectbox for Case Year
                case_year = st.selectbox(
                    label="Select Year",
                    options=years,
                    index=len(years) - 1,
                )

                # button to search cases 
                if st.button("Search Cases"):
                    with st.spinner("Searching cases...."):
                        if case_number and category_name and division_name and case_year:
                            category_id = case_categories_mapping.get(category_name)

                            # call the search function
                            case_details_search = search_case_number(
                                case_number=case_number,
                                category_id=category_id,
                                unit_division_id=unit_division_id,
                                case_year=case_year
                            )

                            # store search results in session state
                            st.session_state.search_results = case_details_search

                        else:
                            st.error("Please complete all required fields before searching.")



# display search results in the main area
if "search_results" in st.session_state and st.session_state.search_results is not None:
    case_details_search = st.session_state.search_results

    if case_details_search:
        st.subheader("Search Results")
        st.success(f"Found {len(case_details_search)} case(s) matching your criteria.")

        # convert data to DataFrame
        case_df = pd.DataFrame(case_details_search)

        # select columns to display
        columns_to_display = ["case_id", "case_year", "case_code", "case_index", "number_on_file", "citation", "case_status_desc", "filing_date"]
        st.dataframe(case_df[columns_to_display], use_container_width=True)

        # create a dictionary mapping number_on_file to case_id
        case_mapping = dict(zip(case_df["number_on_file"], case_df["case_id"]))

        st.divider()
        
        # select box for choosing a case
        selected_number = st.selectbox("Select a Case", options=list(case_mapping.keys()))

        # button to fetch case details
        if st.button("Get Case Details"):
            selected_case_id = case_mapping[selected_number]
            case_details = get_case_details_by_id(selected_case_id)
            st.divider()
            st.subheader(f'Case Number : {case_details[0]["number_on_file"]}')
            create_case_tabs(selected_case_id)

    else:
        st.warning("No matching case found. Please check your inputs.")