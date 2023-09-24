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

