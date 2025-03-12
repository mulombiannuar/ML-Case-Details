import streamlit as st
import pandas as pd
import numpy as np
import time
from case_details import *

st.set_page_config(page_title="Interactive Case Overview", page_icon=":bar_chart:")
st.title("Interactive Case Overview")

head_id = "6"
stations = get_head_stations(head_id)
df = pd.DataFrame(stations)  
st.dataframe(data=df, width=1000, height=500) 

case_id = "1697996"
case_details = get_case_details_by_id(case_id)
st.write(case_details)

