import streamlit as st; import pandas as pd
import json
import plotly.express as px
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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


@st.cache_data()
def create_dataframe_of_books(json_file_path):
    # Load the JSON file into a list of dictionaries
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Initialize lists to store extracted data
    titles = []
    prices = []
    in_stocks = []
    ratings = []
    genres = []
    image_paths = []
    
    # Iterate through the list of dictionaries and extract data
    for item in data:
        titles.append(item['title'])
        prices.append(float(item['price']))
        in_stocks.append(item['availability'])
        ratings.append(item['rating'])
        genres.append(item['genre'][0])
        images = item['images']
        image_path = images[0]['path']
        #image_path = image_path.split('/')[-1]
        image_paths.append(image_path)
    
    # Create a pandas DataFrame
    books_df = pd.DataFrame({
        'Title': titles,
        'Price': prices,
        'In_Stock':in_stocks,
        'Rating':ratings,
        'Genre':genres,
        'Image_Path': image_paths
    })
    
    return books_df

@st.cache_data()
def create_dataframe_quotefancy(json_file_path, json_path_filtered_text):
    # Load the JSON file into a list of dictionaries
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    with open(json_path_filtered_text, 'r') as json_file:
        filtered_data = json.load(json_file)

    # Initialize lists to store extracted data
    quotes = []
    authors = []
    upvotes = []
    downvotes = []
    image_paths = []
    
    # Iterate through the list of dictionaries and extract data
    for item in data:
        quotes.append(item['quote'])
        authors.append(item['author'])
        upvotes.append(item['upvotes'])
        downvotes.append(item['downvotes'])
        images = item['images']
        image_path = images[0]['path']
        #image_path = image_path.split('/')[-1]
        image_paths.append(image_path)
    
    # Create a pandas DataFrame
    temp_df = pd.DataFrame({
        'Quote': quotes,
        'Author': authors,
        'Upvotes':upvotes,
        'Downvotes':downvotes,
        'Image_Path': image_paths
    })
    
    return temp_df, filtered_data

st.sidebar.title('Web Scraping: Image Scraping')
# Create a sidebar with a radio button selection
selected_option = st.sidebar.radio("Select an option:", ["Books to Scrape", "Techinstr Shopify", "Quote Fancy" ])

# Display content based on the selected option
if selected_option == "Books to Scrape":
    st.title("Books To Scrape Data Visualization")
    st.write('The data of 1000 books is scraped from [bookstoscrape](http://books.toscrape.com/)')
    st.header('A Glimpse of the Data')
    books_df = create_dataframe_of_books('bookstoscrape/books.json')
    st.dataframe(books_df)

    #Price, Ratings, and In_Stock Distribution
    if True:
        st.header('Price, Ratings, and In_Stock Distribution')

        # Sidebar: Genre selection
        selected_genre = st.selectbox("Select a genre:", ['All'] +list( books_df['Genre'].unique()))

        # Filter the DataFrame based on selected genre
        if selected_genre == 'All':
            filtered_df = books_df
        else:
            filtered_df = books_df[books_df['Genre'] == selected_genre]

        st.subheader(f'Selected Genre: {selected_genre}, Total books: {filtered_df.shape[0]}')

        if True: #Showing various plots
            # Plotly Price Distribution Plot
            fig = px.histogram(filtered_df, x='Price', nbins=50, title=f'Price(in Pounds) Distribution for {selected_genre} Books')
            #st.plotly_chart(fig)

            # Plotly Box Plot for Price Distribution
            if selected_genre != 'All':
                box_fig = px.box(filtered_df, x='Genre', y='Price',
                                title=f'Box Plot: Price Distribution for {selected_genre} Books')
                box_fig.update_layout(xaxis_title='Genre', yaxis_title='Price')
            else:
                box_fig = px.box(filtered_df, y='Price',
                                title=f'Box Plot: Price Distribution for {selected_genre} Books')
                box_fig.update_layout(xaxis_title='Genre', yaxis_title='Price')

            # Display both plots
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig)
            col2.plotly_chart(box_fig)


            # Plotly In_Stock Distribution Plot
            fig = px.histogram(filtered_df, x='In_Stock', nbins=50, title=f'In_Stock Distribution for {selected_genre} Books')
            st.plotly_chart(fig)

            # Calculate rating distribution percentages
            rating_percentage = filtered_df['Rating'].value_counts(normalize=True).sort_index() * 100

            # Plotly Bar Chart for Rating Distribution
            fig = px.bar(x=rating_percentage.index, y=rating_percentage.values,
                        labels={'x': 'Rating', 'y': 'Percentage'},
                        title=f'Rating Distribution for {selected_genre} Books')
            fig.update_xaxes(type='category')
            st.plotly_chart(fig)

        if True: #Showing top 10 books
            st.header(f'Top 10 Lists for {selected_genre} Books')
            if len(filtered_df) < 5:
                st.warning("There are not enough books in this genre for the top 5 analysis.")
            else:
                top_expensive = filtered_df.nlargest(5, 'Price')
                top_cheapest = filtered_df.nsmallest(5, 'Price')
                top_rated = filtered_df.nlargest(5, 'Rating')
                lowest_rated = filtered_df.nsmallest(5, 'Rating')

                # Display Top 5 Most Expensive Books (if available)
                st.write('**Top 5 Most Expensive Books**')
                st.table(top_expensive[['Title', 'Price', 'Rating', 'In_Stock']])

                # Display Top 5 Cheapest Books (if available)
                st.write('**Top 5 Cheapest Books**')
                st.table(top_cheapest[['Title', 'Price', 'Rating', 'In_Stock']])

                # Display Top 5 Highest Rated Books (if available)
                st.write('**Top 5 Highest Rated Books**')
                st.table(top_rated[['Title', 'Price', 'Rating', 'In_Stock']])

                # Display Top 5 Lowest Rated Books (if available)
                st.write('**Top 5 Lowest Rated Books**')
                st.table(lowest_rated[['Title', 'Price', 'Rating', 'In_Stock']])
    
        if True: #Showing Scatter plot
            st.header(f'Showing Scatter Plot and Correlation Heatmap for Price vs Rating for {selected_genre} Books')
            # Plotly Scatter Plot for Price vs. Rating
            if selected_genre != 'All':
                scatter_fig = px.scatter(filtered_df, x='Price', y='Rating', color='Genre',
                                title=f'Scatter Plot: Price vs. Rating for {selected_genre} Books')
                scatter_fig.update_layout(xaxis_title='Price', yaxis_title='Rating')
                #st.plotly_chart(fig)
            else:
                scatter_fig = px.scatter(filtered_df, x='Price', y='Rating',
                                title=f'Scatter Plot: Price vs. Rating for {selected_genre} Books')
                scatter_fig.update_layout(xaxis_title='Price', yaxis_title='Rating')
                #st.plotly_chart(fig)
            # Calculate the correlation matrix
            correlation_matrix = filtered_df[['Price', 'Rating']].corr()

            # Plotly Correlation Heatmap
            corr_fig = px.imshow(correlation_matrix, 
                            title='Correlation Heatmap for Price and Rating')
            #st.plotly_chart(corr_fig)
            # Display both plots
            col1, col2 = st.columns(2)
            col1.plotly_chart(scatter_fig)
            col2.plotly_chart(corr_fig)

        #Show Book Cover
        if True:
            st.header('Show Book Cover')
            # Sidebar: Book title selection
            selected_title = st.selectbox("Select a book title:", filtered_df['Title'])
            # Get the book information for the selected title
            book_info = filtered_df[filtered_df['Title'] == selected_title].iloc[0]

            # Get the image path for the selected title
            image_path = filtered_df[filtered_df['Title'] == selected_title]['Image_Path'].values[0]

            image = Image.open('bookstoscrape/book_images/'+ image_path)
            image_resized = image.resize((300, 400))  # Resize to desired dimensions
            #st.image(image_resized, caption=selected_title, use_column_width=True)

            # Display book cover image in the left column
            left_column, right_column = st.columns(2)
            left_column.image(image_resized, caption=selected_title, use_column_width=True)

            # Display book information in the right column
            right_column.write(f"**Title:** {book_info['Title']}")
            right_column.write(f"**Price:** £{book_info['Price']}")
            right_column.write(f"**Genre:** {book_info['Genre']}")
            right_column.write(f"**Rating:** {book_info['Rating']}")
            right_column.write(f"**Stock:** {book_info['In_Stock']}")

    #Pie chart for genre dist.
    if True:
        st.header('Genre Distribution')
        # Calculate genre distribution percentages
        genre_percentage = books_df['Genre'].value_counts(normalize=True) * 100

        st.table(genre_percentage)

        # Plotly Bar Chart
        fig = px.bar(x=genre_percentage.index, y=genre_percentage.values, title='Genre Distribution (%)')
        fig.update_layout(yaxis_title='Percentage')
        st.plotly_chart(fig)


elif selected_option == "Techinstr Shopify":
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

elif selected_option == "Quote Fancy":
    st.title("Scraped Quotes Visualization")
    st.write('The data of **top 100 quotes** is scraped from [quotefancy](https://quotefancy.com/motivational-quotes)')
    st.header('A Glimpse of the Data')
    quote_df, filtered_quote_text = create_dataframe_quotefancy('quotefancy/quotes.json','quotefancy/quote_filtered_text.json')
    st.dataframe(quote_df)

    #SHOW QUOTE IMAGE
    if True:
        st.header('Select quote to view quote image')
        # Sidebar: Book title selection
        selected_quote = st.selectbox("Select a Quote:", quote_df['Quote'])
        # Get the book information for the selected title
        quote_info = quote_df[quote_df['Quote'] == selected_quote].iloc[0]

        # Get the image path for the selected title
        image_path = quote_df[quote_df['Quote'] == selected_quote]['Image_Path'].values[0]

        image = Image.open('quotefancy/downloads/'+ image_path)
        
        # Display book cover image in the left column
        st.image(image, caption=selected_quote, use_column_width=True)

        # Display book information in the right column
        st.write(f"**Quote:** {quote_info['Quote']}")
        st.write(f"**Author:** {quote_info['Author']}")
        st.write(f"**Upvotes:** {quote_info['Upvotes']}")
        st.write(f"**Downvotes:** {quote_info['Downvotes']}")
    #SHOW UPVOTE DISTRIBUTION
    if True:
        st.header('Upvotes Distribution')
        # Create a histogram of upvotes distribution using Plotly
        fig = px.histogram(quote_df, x='Upvotes', nbins=50, title='Distribution of Upvotes')
        st.plotly_chart(fig)

        # Create a box plot using Plotly
        fig = px.box(quote_df, y='Upvotes', title='Box Plot of Upvotes')
        st.plotly_chart(fig)
        st.write('Most upvotes are concentrated in the **2k-10k** region. Only a few have upvotes above 20k. There\'s \
                 only one quote that has above 75k upvotes. Overall a very *skewed* distribution of upvotes for top 100 quotes from quotefancy')

    #SHOW UPVOTES VS DOWNVOTES
    if True:
        # Streamlit app
        st.header("Upvotes vs Downvotes")

        # Create a scatter plot using Plotly
        fig = px.scatter(quote_df, x='Upvotes', y='Downvotes', trendline='ols', title='Upvotes vs Downvotes')
        st.plotly_chart(fig)
        st.write('There seems to be a linear relationship between upvotes and downvotes.')
    
    #SHOW Word Cloud of Most Frequent Words
    if True:
        # Streamlit app
        st.header("Word Cloud of Most Frequent Words From the Top 100 Quotes")

        # Create a text string containing all the quotes
        all_quotes_text = filtered_quote_text['filtered_text']
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_quotes_text)

        # Display the word cloud using Matplotlib
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

