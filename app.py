import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from case_details import *

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Interactive Case Overview", page_icon=":bar_chart:", layout='wide')
st.title("Interactive Case Overview")

# Generate years from 1926 to the current year
years = list(range(1926, datetime.now().year + 1))

# Fetch heads and create a mapping
heads_data = get_heads()
head_mapping = {head["head_name"]: head["head_id"] for head in heads_data}
head_options = list(head_mapping.keys())

# Initialize session state to store search results
if "search_results" not in st.session_state:
    st.session_state.search_results = None

with st.sidebar:
    st.subheader("Search Case Details")

    # First selectbox for Court Heads
    head_name = st.selectbox(
        label="Court Heads",
        options=head_options,
        index=None,
        placeholder="Select court head...",
    )

    if head_name:
        head_id = head_mapping.get(head_name)  # Get head_id

        # Fetch stations based on selected head_id
        stations_data = get_head_stations(head_id)
        station_mapping = {station["unit_name"]: station["unit_id"] for station in stations_data}
        station_options = list(station_mapping.keys())

        # Second selectbox for Head Stations
        unit_name = st.selectbox(
            label="Head Stations",
            options=station_options,
            index=None,
            placeholder="Select head station...",
        )

        if unit_name:
            unit_id = station_mapping.get(unit_name)

            # Fetch divisions based on selected unit_id
            divisions_data = get_unit_divisions(unit_id)
            division_mapping = {division["division_name"]: division["unit_division_id"] for division in divisions_data}
            division_options = list(division_mapping.keys())

            # Third selectbox for Unit Divisions
            division_name = st.selectbox(
                label="Unit Divisions",
                options=division_options,
                index=None,
                placeholder="Select unit division...",
            )

            if division_name:
                unit_division_id = division_mapping.get(division_name)

                # Fetch unit division case categories
                case_categories_data = get_unit_division_case_categories(unit_division_id)
                case_categories_mapping = {category["category_name"]: category["category_id"] for category in case_categories_data}
                case_categories_options = list(case_categories_mapping.keys())

                # Selectbox for Case Categories
                category_name = st.selectbox(
                    label="Case Categories",
                    options=case_categories_options,
                    index=None,
                    placeholder="Select case category...",
                )

                # Input for Case Number
                case_number = st.text_input(
                    label="Case Number", 
                    placeholder="Enter case number e.g E103",
                )

                # Selectbox for Case Year
                case_year = st.selectbox(
                    label="Select Year",
                    options=years,
                    index=len(years) - 1,
                )

    # Button to search case (remains in sidebar)
    if st.button("Search Case"):
        with st.spinner("Searching case...."):
            if case_number and category_name and division_name and case_year:
                category_id = case_categories_mapping.get(category_name)

                # Call the search function
                case_details_search = search_case_number(
                    case_number=case_number,
                    category_id=category_id,
                    unit_division_id=unit_division_id,
                    case_year=case_year
                )

                # Store search results in session state
                st.session_state.search_results = case_details_search

            else:
                st.error("Please complete all required fields before searching.")

# Display search results in the main area
if "search_results" in st.session_state and st.session_state.search_results is not None:
    case_details_search = st.session_state.search_results

    if case_details_search:
        st.subheader("Search Results")
        st.success(f"Found {len(case_details_search)} case(s) matching your criteria.")

        # Convert data to DataFrame
        case_df = pd.DataFrame(case_details_search)

        # Select columns to display
        columns_to_display = ["case_id", "case_year", "case_code", "case_index", "number_on_file", "citation", "case_status_desc", "filing_date"]
        st.dataframe(case_df[columns_to_display], use_container_width=True)

        # Create a dictionary mapping number_on_file to case_id
        case_mapping = dict(zip(case_df["number_on_file"], case_df["case_id"]))

        # Select box for choosing a case
        selected_number = st.selectbox("Select a Case", options=list(case_mapping.keys()))

        # Button to fetch case details
        if st.button("Get Case Details"):
            selected_case_id = case_mapping[selected_number]
            case_details = get_case_details(selected_case_id)
            st.write(case_details)

    else:
        st.warning("No matching case found. Please check your inputs.")