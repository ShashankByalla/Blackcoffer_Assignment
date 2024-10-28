# text_analysis.py

import pandas as pd
import os
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import re

# Load positive and negative words from text files
def load_words(file_path):
    with open(file_path, 'r', encoding='ISO-8859-1') as file:  # Changed encoding here
        return [line.strip() for line in file.readlines()]

pos_words = load_words('../data/MasterDictionary/positive-words.txt')
neg_words = load_words('../data/MasterDictionary/negative-words.txt')
stop_words = set(stopwords.words('english'))

# Analysis functions
def get_sentiment_score(text):
    words = word_tokenize(text.lower())
    positive_score = sum(1 for word in words if word in pos_words)
    negative_score = sum(1 for word in words if word in neg_words)
    return positive_score, negative_score

def calculate_polarity(positive, negative):
    return (positive - negative) / (positive + negative + 0.000001)  # Avoid division by zero

def calculate_subjectivity(positive, negative, word_count):
    return (positive + negative) / (word_count + 0.000001)

def calculate_avg_sentence_length(text):
    sentences = sent_tokenize(text)
    return sum(len(sent.split()) for sent in sentences) / len(sentences) if sentences else 0

def calculate_percentage_complex_words(text):
    words = word_tokenize(text.lower())
    complex_words = sum(1 for word in words if len(re.findall('[aeiou]', word)) > 2)  # Simple check for complex words
    return (complex_words / len(words)) * 100 if words else 0

# Loop through extracted text files and analyze each
data = []
for file in os.listdir('../outputs'):
    if file.endswith('.txt'):
        with open(f"../outputs/{file}", 'r', encoding='ISO-8859-1') as f:  # Changed encoding here as well
            text = f.read()
            pos_score, neg_score = get_sentiment_score(text)
            polarity = calculate_polarity(pos_score, neg_score)
            subjectivity = calculate_subjectivity(pos_score, neg_score, len(text.split()))
            avg_sentence_len = calculate_avg_sentence_length(text)
            percent_complex_words = calculate_percentage_complex_words(text)
            
            # Collect data for output
            data.append([
                file, pos_score, neg_score, polarity, subjectivity, avg_sentence_len,
                percent_complex_words
            ])

# Convert results to DataFrame and save as Excel file
output_df = pd.DataFrame(data, columns=[
    'URL_ID', 'POSITIVE_SCORE', 'NEGATIVE_SCORE', 'POLARITY_SCORE', 
    'SUBJECTIVITY_SCORE', 'AVG_SENTENCE_LENGTH', 'PERCENTAGE_OF_COMPLEX_WORDS'
])
output_df.to_excel('../outputs/analysis_output.xlsx', index=False)
print("Text analysis completed and saved to analysis_output.xlsx")
