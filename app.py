import streamlit as st
import pandas as pd
import numpy as np
import time
from case_details import *

st.set_page_config(page_title="Interactive Case Overview", page_icon=":bar_chart:")
st.title("Interactive Case Overview")

st.subheader("Heads")
heads = get_heads()
df = pd.DataFrame(heads)  
st.dataframe(data=df, width=1000, height=500) 

st.divider()
    
st.subheader("Head Stations")
head_id = "7"
stations = get_head_stations(head_id)
df = pd.DataFrame(stations)  
st.dataframe(data=df, width=1000, height=500) 

st.divider()

st.subheader("Case Details")
case_id = "1697996"
case_details = get_case_details_by_id(case_id)
st.write(case_details)

st.divider()

st.subheader("Case Parties")
case_parties = get_case_parties(case_id)
df = pd.DataFrame(case_parties)
st.dataframe(data=df, width=1000)

st.divider()

st.subheader("Case Activities")
case_activities = get_case_activities(case_id)
st.write(case_activities)
# df = pd.DataFrame(case_activities)
# st.dataframe(data=df, width=1000)

st.divider()

activity_id = 16841483
st.subheader('Activity Outcome')
activity_outcome = get_activity_outcome(activity_id)
st.write(activity_outcome)