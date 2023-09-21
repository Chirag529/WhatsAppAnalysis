## Whatsapp Sentiment Analysis

# Importing the libraries
# Data manipulation
import pandas as pd
# Data visualization
import matplotlib.pyplot as plt
# Data visualization (based on matplotlib)
import seaborn as sns
# For regular expressions
import regex
# Word cloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# For emoji support
import emoji
# For counting most common words in a list of strings
from collections import Counter

# Show every column in dataframe
pd.set_option('display.max_columns', None)




## Read the data from the Excel file into a DataFrame

# Define the file path to your WhatsApp chat Excel file
chat_excel_file_path = '../Sentiment_Analysis/dataset/1_Dec_Chat.xlsx'

# Read the WhatsApp chat data from the Excel file into a DataFrame
chat_data = pd.read_excel(chat_excel_file_path)

# Display the first 5 rows of the chat data
first_five_rows = chat_data.head(5)

# Print the first five rows to view the data
print(first_five_rows)



## Data Exploration