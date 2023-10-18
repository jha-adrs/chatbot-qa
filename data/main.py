import time
import requests
import os
import pandas as pd
import tiktoken
import openai
import csv
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up the cl100k_base tokenizer
tokenizer = tiktoken.get_encoding("cl100k_base")

# Load scraped data from CSV
df = pd.read_csv('processed/scraped.csv', index_col=0)
df.columns = ['title', 'text']
print("starting split intio chunks")
# Function to split the text into chunks of a maximum number of tokens
def split_into_chunks(text, max_tokens=500):
    # Split the text into sentences
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    current_chunk_tokens = 0
    
    for sentence in sentences:
        sentence_tokens = len(tokenizer.encode(" " + sentence))
        
        if current_chunk_tokens + sentence_tokens <= max_tokens:
            current_chunk += sentence + ". "
            current_chunk_tokens += sentence_tokens
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
            current_chunk_tokens = sentence_tokens
    
    # Add the last chunk
    chunks.append(current_chunk.strip())
    return chunks

# Create a list to store the chunks
chunks = []
print("starting loop through dataframe iterrows")
# Loop through the dataframe and split text into chunks
for _, row in df.iterrows():
    if row['text'] is not None:
        chunks.extend(split_into_chunks(row['text']))

# Create a dataframe with chunks
df_chunks = pd.DataFrame(chunks, columns=['text'])

# Function to get embeddings from OpenAI API
def get_embeddings(text):
    response = openai.Embedding.create(input=text, engine='text-embedding-ada-002')
    return response['data'][0]['embedding']

# Create a list to store embeddings
embeddings = []

print("starting iterrows again")
iterations = 0
# Loop through the chunks and get embeddings from OpenAI API
for _, row in df_chunks.iterrows():
    iterations += 1
    print("Current: ",iterations, end='\r')
    embeddings.append(get_embeddings(row['text']))
    # Pause for 22 seconds to comply with the rate limit
    time.sleep(22)
print("finished iterrows again", iterations)
# Add embeddings to the dataframe
df_chunks['embeddings'] = embeddings

# Save chunks and embeddings to CSV
df_chunks.to_csv('processed/embeddings.csv', index=False)

# Connect to the database and create a cursor
conn_string = os.getenv('DATABASE_URL')
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

print("starting database insertion")
# Loop through the dataframe and insert rows into the database
for _, row in df_chunks.iterrows():
    text = row['text']
    n_tokens = len(tokenizer.encode(text))
    embeddings = list(row['embeddings'])

    # Insert the row into the table
    insert_query = f"INSERT INTO documents (text, n_tokens, embeddings) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (text, n_tokens, embeddings))

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()
