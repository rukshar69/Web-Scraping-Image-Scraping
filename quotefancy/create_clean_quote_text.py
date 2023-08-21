import json; import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

def create_dataframe_quotefancy(json_file_path):
    # Load the JSON file into a list of dictionaries
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

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
    
    return temp_df

quote_df = create_dataframe_quotefancy('quotes.json')

# Create a text string containing all the quotes
all_quotes_text = ' '.join(quote_df['Quote'])

# Remove commas and quotation marks
#all_quotes_text = re.sub('[,",]', '', all_quotes_text)

# Tokenize the text into words
words = nltk.word_tokenize(all_quotes_text)

# Remove common words (stop words)
stop_words = set(stopwords.words('english'))
filtered_words = [re.sub(r'[^A-Za-z]', '', word) for word in words if word.lower() not in stop_words]
# Generate the word cloud
filtered_text = ' '.join(filtered_words)

print(filtered_text)
filtered_text_dict = {'filtered_text': filtered_text}
with open('quote_filtered_text.json', 'w') as json_file:
    json.dump(filtered_text_dict, json_file)