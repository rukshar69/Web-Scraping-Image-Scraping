import streamlit as st; import pandas as pd
import ast

@st.cache_data()
def load_data(csv_file):
    data = pd.read_csv(csv_file)
    # # Convert the 'images' column from string to dictionary
    # data['images'] = data['images'].apply(ast.literal_eval)

    # # Extract the 'path' values from the 'images' dictionary and create a new column
    # data['path'] = data['images'].apply(lambda x: x.get('path'))

    # # Drop the original 'images' column
    # data.drop(columns=['images'], inplace=True)
    return data 

df = load_data('techinstr/products.csv')
st.write(df.info())