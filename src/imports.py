# === CORE ===
import os
import re
from pathlib import Path

# === DATA HANDLING ===
import pandas as pd
import numpy as np
from pathlib import Path

# === OCR & IMAGE PROCESSING ===
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
import cv2

# === NLP PREPROCESSING (PORTUGUESE) ===
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer  # Portuguese stemmer
from gensim.models import Phrases  # For MWEs

# Load Portuguese NLP models
nlp_pt = spacy.load("pt_core_news_sm")  # or 'pt_core_news_lg'
stemmer_pt = RSLPStemmer()

# === LEXICAL SENTIMENT ===
from collections import defaultdict
from unidecode import unidecode  # For accent normalization

# === MACHINE LEARNING ===
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# === VISUALIZATION ===
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

# === DEEP LEARNING (OPTIONAL) ===
# import tensorflow as tf
# from transformers import BertTokenizer, TFBertForSequenceClassification



