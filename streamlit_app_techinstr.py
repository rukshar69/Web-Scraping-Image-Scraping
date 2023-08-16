import streamlit as st; import pandas as pd
import json
import plotly.express as px
from PIL import Image

@st.cache_data()
def create_dataframe_from_json(json_file_path):
    # Load the JSON file into a list of dictionaries
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    # Initialize lists to store extracted data
    titles = []
    prices = []
    image_paths = []
    
    # Iterate through the list of dictionaries and extract data
    for item in data:
        titles.append(item['title'])
        prices.append(float(item['price']))
        images = item['images']
        image_path = images[0]['path']
        image_path = image_path.split('/')[-1]
        image_paths.append(image_path)
    
    # Create a pandas DataFrame
    df = pd.DataFrame({
        'Title': titles,
        'Price': prices,
        'Image_Path': image_paths
    })
    
    return df

df = create_dataframe_from_json('techinstr/products.json')
st.title('Techinstr Shopify Store Scrape Data Visualization')
st.header('A Glimpse of Data')
st.dataframe(df)

st.header('Price Distribution')
# Create a price distribution chart using Plotly
fig = px.histogram(df, x="Price", nbins=50, title="Price Distribution in Pound")
st.plotly_chart(fig)


 # Sort the DataFrame by Price in ascending order to get the cheapest products
cheapest_products = df.sort_values(by='Price', ascending=True).head(10)

# Sort the DataFrame by Price in descending order to get the most expensive products
most_expensive_products = df.sort_values(by='Price', ascending=False).head(10)

# Display the top 10 cheapest products
st.subheader("Top 10 Cheapest Products:")
st.dataframe(cheapest_products[['Title', 'Price']])

# Display the top 10 most expensive products
st.subheader("Top 10 Most Expensive Products:")
st.dataframe(most_expensive_products[['Title', 'Price']])

# Shuffle the dataframe to randomize the order
df = df.sample(frac=1).reset_index(drop=True)

# Select the first 9 random elements from the shuffled dataframe
random_images = df['Image_Path'].head(9).tolist()
image_paths = ['techinstr/product_images/thumbs/small/'+x for x in random_images]

# Set the title of your Streamlit app
st.header("Display 9 Random Images in a 3x3 Grid")
st.write('These are downsized thumbnail images(100x100). So, the quality is low. The original images(1000x1000) weren\'t uploaded \
         due to size-related issues')

# Create a 3x3 grid layout
for i in range(0, len(image_paths), 3):
    col1, col2, col3 = st.columns(3)

    with col1:
        if i < len(image_paths):
            image = Image.open(image_paths[i])
            st.image(image, caption=random_images[i], use_column_width=True)

    with col2:
        if i + 1 < len(image_paths):
            image = Image.open(image_paths[i + 1])
            st.image(image, caption=random_images[i+1], use_column_width=True)

    with col3:
        if i + 2 < len(image_paths):
            image = Image.open(image_paths[i + 2])
            st.image(image, caption=random_images[i+2], use_column_width=True)

