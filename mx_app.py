# Import libraries
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# Page title
st.set_page_config(page_title='Interactive Music Explorer', page_icon='🎶')
st.title('🎶 Interactive Music Explorer')

# App description - Explain functionalities in an expander box
with st.expander('About this app'):
    st.markdown('**What can this app do?**')
    st.info('This app shows the use of Pandas for data wrangling, Altair for chart creation, and an editable dataframe for data interaction.')
    st.markdown('**How to use the app?**')
    st.warning('To engage with the app, 1. Select genres of your interest in the drop-down selection box and then 2. Select the year range from the slider widget. As a result, this will generate an updated editable DataFrame and line plot.')

# Question header
st.subheader('Which Music Genre is Most Popular Over Time?')

# Load data - Read CSV into a Pandas DataFrame
df = pd.read_csv('music_genres_summary.csv')
df.year = df.year.astype('int')

# Genres selection - Create dropdown menu for genre selection
genres_list = df.genre.unique()
genres_selection = st.multiselect('Select genres', genres_list, ['Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Classical'])

# Year selection - Create slider for year range selection
year_list = df.year.unique()
year_selection = st.slider('Select year range', min(year_list), max(year_list), (2000, 2020))
year_selection_list = list(np.arange(year_selection[0], year_selection[1]+1))

# Subset data - Filter DataFrame based on selections
df_selection = df[df.genre.isin(genres_selection) & df['year'].isin(year_selection_list)]
reshaped_df = df_selection.pivot_table(index='year', columns='genre', values='popularity', aggfunc='sum', fill_value=0)
reshaped_df = reshaped_df.sort_values(by='year', ascending=False)

# Editable DataFrame - Allow users to make live edits to the DataFrame
df_editor = st.data_editor(reshaped_df, height=212, use_container_width=True,
                            column_config={"year": st.column_config.TextColumn("Year")},
                            num_rows="dynamic")

# Data preparation - Prepare data for charting
df_chart = pd.melt(df_editor.reset_index(), id_vars='year', var_name='genre', value_name='popularity')

# Display line chart
chart = alt.Chart(df_chart).mark_line().encode(
            x=alt.X('year:N', title='Year'),
            y=alt.Y('popularity:Q', title='Popularity'),
            color='genre:N'
            ).properties(height=320)
st.altair_chart(chart, use_container_width=True)
