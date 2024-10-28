# data_extraction.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Load URLs from Input.xlsx
input_file = pd.read_excel('../data/Input.xlsx')
urls = input_file['URL'].tolist()

# Ensure outputs directory exists
output_dir = '../outputs'
os.makedirs(output_dir, exist_ok=True)

def extract_article_text(url, article_id):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check if the request was successful

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the title and text content
        title = soup.find('title').get_text() if soup.find('title') else "No Title Found"
        text = " ".join([p.get_text() for p in soup.find_all('p')])
        
        # Save extracted text to a file
        output_file_path = os.path.join(output_dir, "{}.txt".format(article_id))
        with open(output_file_path, 'w') as file:
            file.write("{}\n\n{}".format(title, text))
        
        print("Extracted and saved: {}".format(article_id))
    
    except requests.RequestException as e:
        print("Request error for {} ({}): {}".format(article_id, url, e))
    except Exception as e:
        print("Error extracting {}: {}".format(article_id, e))

# Loop through URLs and save each article's content
for i, url in enumerate(urls):
    extract_article_text(url, "Article_{}".format(i + 1))
