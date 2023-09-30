## Whatsapp Analysis

# Importing the libraries
# Data manipulation
import pandas as pd
# Data visualization
import matplotlib.pyplot as plt
# Data visualization (based on matplotlib)
import seaborn as sns
# For regular expressions
import regex 
# For splitting strings
import re
# Word cloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# For emoji support
import emoji
# For counting most common words in a list of strings
from collections import Counter
# For numerical analysis
import numpy as np
# For creating a network graph
import networkx as nx

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

# Let's copy our data into a new DataFrame so we don't modify the original data
df = chat_data.copy()


# Replace NaN values with empty strings in columns 'sender message', 'Column3', and 'Column4'
df["sender message"].fillna("", inplace=True)
df["Column3"].fillna("", inplace=True)
df["Column4"].fillna("", inplace=True)

# Merge sender message, Column3, and Column4 columns into a single column named Message
df["Message"] = (
    df["sender message"]
    + " "
    + df["Column3"].astype(str)
    + " "
    + df["Column4"].astype(str)
)

# Drop the sender message, Column3, and Column4 columns
df.drop(columns=["sender message", "Column3", "Column4"], inplace=True)



# Display the first 5 rows of the chat data
df.head(5)


## Data Cleaning

# Remove rows that contain only missing values
df.dropna(how="all", inplace=True)


## Analysis

# Let's see total messages sent
total_messages = df.shape[0]
print("Total messages sent:", total_messages)

# Count the number of media messages by checking if 'Message' contains '<Media omitted>'
num_media_messages = df[df["Message"].str.contains
                        ("<Media omitted>")].shape[0]
num_media_messages


# Total users join and left the groups
# Count the number of times someone joined the group using the invite link
join_message_count = df[df["sender name"].str.contains(" joined using this group's invite link")].shape[0]

# Count the number of times someone left the group
leave_message_count = df[df["sender name"].str.contains(" left")].shape[0]

# Print the counts
print("Total join messages:", join_message_count)
print("Total leave messages:", leave_message_count)



## Extract emojis from messages
# Function to extract emojis from a text message
def extract_emojis(text):
    # Define a regular expression pattern to match emojis
    emoji_pattern = re.compile(
        r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
        r"\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF"
        r"\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF"
        r"\U0001FB00-\U0001FBFF\U0001FC00-\U0001FCFF\U0001FD00-\U0001FDFF"
        r"\U0001FE00-\U0001FEFF\U0001FF00-\U0001FFFF]+",
        flags=re.UNICODE,
    )
    emojis = emoji_pattern.findall(text)
    return emojis


# Apply the extract_emojis function to the 'Message' column and create a new column 'Emojis'
df["Emojis"] = df["Message"].apply(extract_emojis)

# Count the total number of emojis
total_emojis = sum(df["Emojis"].str.len())

# Print the total number of emojis
print(total_emojis)



## Top 10 frequent emojis used in the chat
# Function to extract emojis from a text message
def extract_emojis(text):
    # Define a regular expression pattern to match emojis
    emoji_pattern = re.compile(
        r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
        r"\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF"
        r"\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF"
        r"\U0001FB00-\U0001FBFF\U0001FC00-\U0001FCFF\U0001FD00-\U0001FDFF"
        r"\U0001FE00-\U0001FEFF\U0001FF00-\U0001FFFF]+",
        flags=re.UNICODE,
    )
    emojis = emoji_pattern.findall(text)
    return emojis


# Apply the extract_emojis function to the 'Message' column and create a new column 'Emojis'
df["Emojis"] = df["Message"].apply(extract_emojis)

# Count the total number of emojis
emojis = sum(df["Emojis"].str.len())

# Count the frequency of each emoji
emoji_counts = Counter([emoji for sublist in df["Emojis"]
                       for emoji in sublist])

# Get the top 10 emojis
top_10_emojis = emoji_counts.most_common(10)

# Create a DataFrame to display the top 10 emojis and their frequencies
top_10_df = pd.DataFrame(top_10_emojis, columns=["Emoji", "Frequency"])

# Set the index to start from 1
top_10_df.index = range(1, len(top_10_df) + 1)

# Display the DataFrame
top_10_df


## URL Links
URLPATTERN = r"(https://\S+)"
df["urlcount"] = df.Message.apply(
    lambda x: regex.findall(URLPATTERN, x)).str.len()
links = np.sum(df.urlcount)

links



## World Cloud of most common words
# Join all messages into a single text
text = " ".join(message for message in df["Message"])

# Calculate the total number of words in all the messages
total_words = len(text)
print("There are {} words in all the messages.".format(total_words))

# Define stopwords
stopwords = set(STOPWORDS)

# Generate a WordCloud image
wordcloud = WordCloud(stopwords=stopwords,
                      background_color="white").generate(text)

# Display the WordCloud image
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()



## Total Deleted Messages
# Count the number of deleted messages using a regex pattern
deleted_messages_count = df[
    df["Message"].str.contains(
        r"^\s*This message was deleted\s*$", case=False, regex=True
    )
].shape[0]

# Print the count of deleted messages
print("Total deleted messages:", deleted_messages_count)



## Top 10 active users in the group
# Find the top 10 most active users in the group chat
top_10_active_users = df["sender name"].value_counts().head(10)

# Convert the Series to a DataFrame and reset the index
top_10_active_users_df = top_10_active_users.reset_index()

# Rename the columns to be more descriptive
top_10_active_users_df.columns = ["Sender", "Message Count"]

# Print the top 10 most active users
top_10_active_users_df



## Keyword Search in messages
## This is a User-defined function
# Step 1: Combine all the chat messages into a single text
chat_text = " ".join(df["Message"])

# Step 2: Tokenize the text into words
chat_words = chat_text.split()

# Step 3: Convert all words to lowercase to ensure case-insensitive matching
chat_words = [word.lower() for word in chat_words]

# Step 4: Count the frequency of each word using Counter
word_counts = Counter(chat_words)

# Step 5: Sort the words by frequency in descending order
sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)


# Create a list to store the top keywords and their frequencies
top_keywords_list = []

# Change 10 to the desired number of top keywords
top_keywords_count = 10

# Add the top keywords and their frequencies to the list
for word, count in sorted_words[:top_keywords_count]:
    top_keywords_list.append({"Keyword": word, "Frequency": count})

# Create a DataFrame from the list
top_keywords_df = pd.DataFrame(top_keywords_list)

# Print the DataFrame
top_keywords_df


## Top 3 most common words used in the chat
# Let's conduct a keyword search to find the most common words used in the chat

# Step 1: Combine all the chat messages into a single text
chat_text = " ".join(df["Message"])

# Step 2: Tokenize the text into words
chat_words = chat_text.split()

# Step 3: Convert all words to lowercase to ensure case-insensitive matching
chat_words = [word.lower() for word in chat_words]

# Step 4: Define the keywords you want to search for
# Replace with your desired keywords
search_keywords = ["accenture", "joining", "date"]

# Step 5: Initialize a dictionary to count the frequency of each keyword
keyword_counts = {keyword: 0 for keyword in search_keywords}

# Step 6: Count the frequency of each keyword in the text
for word in chat_words:
    if word in keyword_counts:
        keyword_counts[word] += 1

# Step 7: Sort the keywords by frequency in descending order
sorted_keywords = sorted(keyword_counts.items(),
                         key=lambda x: x[1], reverse=True)

# Step 8: Print the most common keywords and their frequencies
for keyword, count in sorted_keywords:
    print(f"{keyword}: {count}")



