import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

st.title("CSV Analyzer")

tab_csv, tab_plot = st.tabs(["CSV", "Plot"])

with tab_csv:

    csv_file = st.file_uploader("Upload CSV file", type={"csv", "txt"})

    st.markdown('***')

    if csv_file is not None:

        df = pd.read_csv(csv_file)

        # Convert objects types to string
        for column in df:
            if df[column].dtypes == 'object':
                df[column] = df[column].astype(str)

        st.header('Full data')

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.dataframe(df)

        st.markdown('***')

        if 'cntry' in df.columns:
            st.header('Select countries')
            st.text('Gets applied to ALL plots incl. heatmap on the other site!')
            chosen_countries = st.multiselect('', sorted(df['cntry'].unique()))
            if chosen_countries:
                df = df.loc[df['cntry'].isin(chosen_countries)]

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

    with tab_plot:

        st.subheader('Select two non-numerical variables to plot')

        if csv_file is not None:

            x = st.selectbox('Select x column', column_names)
            y = st.selectbox('Select y column', column_names)

            if x == y:
                st.text('Select different columns!')
            else:
                plot_df = df[[x, y]]

                values_x = st.multiselect('Select bad x-values', sorted(plot_df[x].unique()))

                plot_df = plot_df.loc[~plot_df[x].isin(values_x)]

                values_y = st.multiselect('Select bad y-values', sorted(plot_df[y].unique()))

                plot_df = plot_df.loc[~plot_df[y].isin(values_y)]

                test = plot_df.groupby(by=[x, y], as_index=False).size()

                data = list()

                x_values = test[x].unique()
                y_values = test[y].unique()

                for y_val in y_values:
                    tmp = list()
                    for x_val in x_values:
                        cell = test.loc[(test[x] == x_val) & (test[y] == y_val)]['size'].values
                        if cell.size == 0:
                            cell = 0
                        else:
                            cell = cell[0]
                        tmp.append(cell)
                    data.append(tmp)

                x_lab = [str(i) for i in x_values]
                y_lab = [str(i) for i in y_values]

                fig = px.imshow(data,
                                labels=dict(x=x, y=y, color="Count"),
                                x=x_lab,
                                y=y_lab,
                                text_auto=True, aspect="auto")

                st.plotly_chart(fig, use_container_width=True)

