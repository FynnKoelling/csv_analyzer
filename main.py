import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

st.title("CSV Analyzer")

csv_file = st.file_uploader("Upload CSV file", type={"csv", "txt"})

st.markdown('***')

if csv_file is not None:

    df = pd.read_csv(csv_file)

    st.header('Full data')

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.dataframe(df)

    st.markdown('***')

    st.header('Select column to analyze')

    column_names = list(df.columns.values)

    column = st.selectbox('', column_names)

    column_data = df[column]

    st.markdown('***')

    st.header('Unique value counts')

    value_counts = column_data.value_counts().rename_axis('Value').reset_index(name='Count')

    fig = px.bar(value_counts, x='Value', y='Count')

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(value_counts)

    st.markdown('***')

    st.header('Select values that indicate missing or wrong data')

    values = st.multiselect('', value_counts['Value'].to_list())

    good_values = value_counts.loc[~value_counts['Value'].isin(values)]
    bad_values = value_counts.loc[value_counts['Value'].isin(values)]
    count_good = good_values['Count'].sum()
    count_bad = bad_values['Count'].sum()

    pie_df = {'Classification': ['Usable Values', 'Not Usable Values'], 'Value': [count_good, count_bad]}

    fig = px.pie(pie_df, values='Value', names='Classification')

    st.plotly_chart(fig, use_container_width=True)

    col_df_1, col_df_2, col_df_3 = st.columns([1, 1, 1])

    with col_df_1:
        st.subheader('Usable Values')
        st.dataframe(good_values)
    with col_df_2:
        st.subheader('Not Usable Values')
        st.dataframe(bad_values)
