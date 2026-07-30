# 🛍️ Smart Product Review Analyzer

A Streamlit web application that analyzes customer product reviews 
using NLP-based sentiment analysis, with support for multilingual 
input, feature-level tagging, and side-by-side product comparison.

## Features
- Sentiment classification (Positive/Neutral/Negative) using TextBlob 
  polarity scoring
- Automatic language detection and translation to English for 
  multilingual reviews
- Feature-based tagging (Camera, Price, Battery, Design, Performance)
- Compares up to 2 products simultaneously with weighted scoring and 
  average star ratings
- Interactive Matplotlib visualizations for sentiment and feature 
  distribution

## Tech Stack
- Python
- Streamlit (web interface)
- TextBlob (sentiment analysis)
- langdetect + googletrans (language detection & translation)
- pandas, matplotlib (data handling & visualization)

## How to Run
1. Clone this repository
