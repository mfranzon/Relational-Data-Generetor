import streamlit as st
import pandas as pd
from generate import mock_db
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

from sdv import load_demo

metadata, tables = load_demo(metadata=True)


st.title("Relational Data Generator")


dataset = st.selectbox(
        'Load a database',
        ('...','demo_sdv'))

if dataset == 'demo_sdv':
    s_table = st.selectbox(
        'Select table',
        ('users','sessions', 'transactions'))
    df_tables = pd.DataFrame.from_dict(tables[s_table])
    st.dataframe(df_tables.head())

with st.form("gen-data"):


    rows = st.slider('How many new rows you want?', 
                 0, 150, 20)

    submitted = st.form_submit_button("Generate")
    
    if submitted:
        res = mock_db(metadata, tables, num_rows=rows)
        for table in res:
            profile = ProfileReport(res[table].loc[:, ~res[table].columns.str.endswith('id')],
                       title=f'{table}')
            st_profile_report(profile)
        
